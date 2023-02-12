# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:29:37
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 11:45:03

import sys
import os

import whisper
import torch
import torch.nn.functional as F

from .alignment import perform_word_alignment
from .utils import (
    get_logit_filters,
    should_use_space,
    print_timestamped,
    round_confidence
)
from .vars import (
    HOP_LENGTH,
    SAMPLE_RATE
)

import string

import logging
logger = logging.getLogger()


_punctuation = "".join(c for c in string.punctuation if c not in ["-", "'"])


def _transcribe_timestamped_efficient(
    model,
    audio,
    remove_punctuation_from_words,
    compute_word_confidence,
    include_punctuation_in_confidence,
    refine_whisper_precision_nframes,
    plot_word_alignment,
    # Whisper specific options
    **whisper_options,
):
    """
    Timestamps a transcription created by the whisper engine.

    Args:
            model: 
            audio: 
            remove_punctuation_from_words: 
            compute_word_confidence: 
            include_punctuation_in_confidence: 
            refine_whisper_precision_nframes: 
            plot_word_alignment: 
    Returns:
            
    """

    # Get options
    sample_len = whisper_options["sample_len"]
    temperature = whisper_options["temperature"]
    no_speech_threshold = whisper_options["no_speech_threshold"]
    logprob_threshold = whisper_options["logprob_threshold"]
    verbose = whisper_options["verbose"]
    # Note: "on-the-fly" verbose is not implementable in the current state (we don't know the absolute position of the current chunk). See issue #18
    verbose_bugged = False
    whisper_options["verbose"] = None if whisper_options["verbose"] is True else whisper_options["verbose"]  # We will print intermediate results ourselves

    logit_filters = get_logit_filters(model, whisper_options)
    language = whisper_options["language"]
    tokenizer = whisper.tokenizer.get_tokenizer(model.is_multilingual, task=whisper_options["task"], language=language)

    max_sample_len = sample_len or model.dims.n_text_ctx // 2

    # Note: we cannot trust the token in the middle of tokenizer.sot_sequence which refers to the language
    #       (arbitrarily set to <|en|> if it's actually None/unknown)
    token_sot = tokenizer.sot
    token_eot = tokenizer.eot

    debug = logger.getEffectiveLevel() >= logging.DEBUG

    # The main outcome
    timestamped_word_segments = []  # list of timestamped word segments that have been collected so far
    # Main variables to be accumulated
    segment_tokens = [[]]              # list of lists of token indices that have been collected so far (one list per segment)
    segment_attweights = [[] for _ in range(len(model.decoder.blocks))]
                                    # attention weights on the last segments
    segment_avglogprobs = []        # average log probability for each segment (actually of the corresponding chunk, as computed by whisper)
    segment_logprobs = []           # token log probabilities for each segment
    # Variables related to options that can skip some segments
    sot_index = None                # index of the SOT token in the current set of processed tokens
    no_speech_prob = None           # no speech probability for the current 30 sec chunk
    chunk_logprobs = []             # log probabilities for the current 30 sec chunk
    chunk_tokens = []               # tokens for the current 30 sec chunk (list of Torch tensors)
    chunk_tokens_nosot = []         # tokens for the current 30 sec chunk, without the SOT tokens (list of indices)
    last_token_fallback = None      # last token to use as a fallback if the model gets stuck
    has_started = False             # whether we have started decoding
    mfcc = None                     # MFCC features for the current 30 sec chunk
    new_mfcc = None                 #
    num_inference_steps = 0         # number of inference steps performed so far (for debugging only)

    def reset(add_segment, keep_last_token):
        """ Reset the list of tokens for the current speech segment, and corresponding cross-attention weights """
        nonlocal segment_tokens, segment_attweights
        if add_segment:
            if keep_last_token:
                segment_tokens.append([segment_tokens[-1][-1]])
                segment_attweights = [w[-1:] for w in segment_attweights]
            else:
                segment_tokens.append([])
                segment_attweights = [[] for w in segment_attweights]
            segment_tokens[-2].pop(0)
            if debug:
                logger.debug(f"Added new segment: {tokenizer.decode_with_timestamps(segment_tokens[-2])}")
        elif len(segment_tokens[-1]) > 0:
            segment_tokens[-1] = []
            segment_attweights = [[] for w in segment_attweights]
        if debug:
            logger.debug(f"Reset last segment to: {tokenizer.decode_with_timestamps(segment_tokens[-1])}")

    saw_consecutive_timestamps = False
    def must_flush_segment(curr_tokens):
        """ Return whether or not the previously collected tokens must be used to add a new speech segment """

        nonlocal segment_tokens, saw_consecutive_timestamps, chunk_tokens_nosot
        if curr_tokens is not None and len(curr_tokens) == 1:
            is_timestamp = curr_tokens[0] >= tokenizer.timestamp_begin
            is_previous_timestamp = segment_tokens[-1][-1] >= tokenizer.timestamp_begin if len(segment_tokens[-1]) > 0 else False
            consecutive_timestamps = is_timestamp and is_previous_timestamp
            if consecutive_timestamps:
                saw_consecutive_timestamps = True
            if len(chunk_tokens_nosot) == max_sample_len - 2 and is_timestamp:
                consecutive_timestamps = True
            return consecutive_timestamps
        else: # Several tokens as a prompt or must flush last segments
            must_flush = not saw_consecutive_timestamps and len(segment_tokens[-1]) > 1
            logger.debug(f"New prompt: flushing = {must_flush}")
            if not must_flush:
                # Discard the end of the last transcription
                reset(False, True)
            saw_consecutive_timestamps = False
            return must_flush

    index_begin_30sec_chunck = 0
    def get_index_begin_30sec_chunck(curr_tokens):
        nonlocal index_begin_30sec_chunck

        if curr_tokens is None or len(curr_tokens) > 1:
            res = index_begin_30sec_chunck
            index_begin_30sec_chunck = len(segment_tokens)-1
            return res

    def may_flush_segment(curr_tokens = None):
        """ Add a speech segment with the new tokens if necessary.
            May also remove the last collected segments if filtered out by Whisper (no_speech_prob <= no_speech_threshold)
        """
        nonlocal segment_tokens, segment_attweights, timestamped_word_segments, has_started, no_speech_prob, chunk_tokens, chunk_tokens_nosot, chunk_logprobs, mfcc, new_mfcc, logit_filters, index_begin_30sec_chunck, last_token_fallback, num_inference_steps

        # Check if a new segment should be added
        unfinished_decoding = False
        if must_flush_segment(curr_tokens):

            if mfcc is None:
                mfcc = new_mfcc

            if debug:
                logger.debug(f"Adding segment {len(timestamped_word_segments)+1} at step {num_inference_steps}:\n\t{tokenizer.decode_with_timestamps(segment_tokens[-1])}")

            tokens = segment_tokens[-1][1:]
            # When the decoding hit the max limit (number of tokens) -- usually when the language model gets stuck --
            # then we have to recover the last token from what is send to the decoder
            unfinished_decoding = len(tokens) and tokens[-1] < tokenizer.timestamp_begin
            last_token_reliable = True

            if unfinished_decoding:
                logger.debug(f"WARNING: decoding hit the max limit for segment {segment_tokens} (It usually happens when the language model gets stuck)")
                # The last token chosen is in the prompt for the new chunk
                if curr_tokens is not None and curr_tokens[0] == tokenizer.sot_prev:
                    logger.debug("         Guess last token from the prompt for the new chunk")
                    last_token_fallback = curr_tokens[-4].item()
                # Fallback for the last segment, or without prompt: Assume greedy decoding
                else:
                    logger.debug(f"         Guess last token using probas (assuming greedy decoding)")
                    last_token_fallback = torch.argmax(chunk_logprobs[-1]).item()
                    last_token_reliable = (temperature == 0)
                if debug:
                    logger.debug(f"WARNING: also add last token: {tokenizer.decode_with_timestamps([last_token_fallback])}")

                tokens.append(last_token_fallback)
                segment_tokens[-1].append(last_token_fallback)
                attention_weights = [torch.cat(w, dim=-2) for w in segment_attweights]
                last_logprobs = chunk_logprobs[-1]
            else:
                attention_weights = [torch.cat(w[:-1], dim=-2) for w in segment_attweights]
                last_logprobs = chunk_logprobs[-2]

            # Check prediction of last token
            end_token = tokens[-1]
            if end_token >= tokenizer.timestamp_begin:
                start_token = tokens[0]
                assert start_token >= tokenizer.timestamp_begin
                # If Whisper prediction of the end is obviously wrong, we predict it again (constrained)
                if end_token <= start_token:
                    end_token = last_logprobs[start_token+1:].argmax() + start_token + 1
                    tokens[-1] = end_token

            ws = perform_word_alignment(
                tokens,
                attention_weights,
                tokenizer,
                use_space=should_use_space(language),
                remove_punctuation_from_words=remove_punctuation_from_words,
                refine_whisper_precision_nframes=refine_whisper_precision_nframes,
                unfinished_decoding=unfinished_decoding,
                mfcc=mfcc,
                plot=plot_word_alignment,
            )

            add_segment = len(ws) > 0
            if add_segment:
                timestamped_word_segments.append(ws)
            else:
                logger.debug(f"Not added!")
            reset(add_segment, curr_tokens is not None and len(curr_tokens) == 1)

        i_start = get_index_begin_30sec_chunck(curr_tokens)

        # All segments from previous 30sec chunck have been collected
        if (i_start is not None and has_started):

            mfcc = new_mfcc

            # Get word confidence and/or check if previous segments shoud have been skipped
            should_skip = False
            if compute_word_confidence or no_speech_threshold is not None:

                # no voice activity check
                should_skip = (no_speech_prob > no_speech_threshold) if (no_speech_threshold is not None) else False
                if compute_word_confidence or (should_skip and logprob_threshold is not None):
                    n = len(chunk_logprobs)
                    if n == len(chunk_tokens_nosot):
                        chunk_tokens_nosot = chunk_tokens_nosot[1:]
                    if unfinished_decoding:
                        assert last_token_fallback is not None
                        last_tokens = [last_token_fallback]
                        timestamped_word_segments[-1][-1]["avg_logprob_reliable"] = last_token_reliable
                        n += 1
                    elif len(chunk_tokens_nosot) >= max_sample_len - 3:
                        # there were segments in the 30sec chunck, and then the LM got stuck
                        last_tokens = [torch.argmax(chunk_logprobs[-1]).item()]
                        timestamped_word_segments[-1][-1]["avg_logprob_reliable"] = (temperature == 0)
                    else:
                        last_tokens = [tokenizer.eot]
                    chunck_indices = chunk_tokens_nosot + last_tokens
                    assert len(chunk_logprobs) == len(chunck_indices), f"{len(chunk_logprobs)} != {len(chunck_indices)}"
                    logprobs = torch.cat([logprob[i].unsqueeze(0) for (logprob, i) in zip(chunk_logprobs, chunck_indices)])
                    assert min([p.isfinite().item() for p in logprobs]), \
                        f"Got infinite logprob among ({len(logprobs)}) {[(i, tokenizer.decode_with_timestamps([i]), v.item()) for (i,v) in zip(chunck_indices, logprobs)]}"
                    sum_logprob = sum(logprobs)
                    avg_logprob = sum_logprob/n
                    # don't skip if the logprob is high enough, despite the no_speech_prob
                    if avg_logprob > logprob_threshold:
                        should_skip = False

                if should_skip:
                    logger.debug(f"Skipping last {len(segment_tokens)-1-i_start} segments (no_speech_prob {no_speech_prob} > {no_speech_threshold} and avg_logprob {avg_logprob} < {logprob_threshold})")
                    index_begin_30sec_chunck -= len(segment_tokens)-1-i_start
                    segment_tokens = segment_tokens[:i_start] + [segment_tokens[-1]]
                    timestamped_word_segments = timestamped_word_segments[:i_start]
                elif compute_word_confidence:
                    avg_logprob = avg_logprob.item()
                    i_token_end = -1
                    for i in range(i_start, len(segment_tokens)-1):
                        tokens = segment_tokens[i]
                        i_token_start = i_token_end + 1
                        i_token_end = i_token_start + len(tokens)
                        assert chunck_indices[i_token_start:i_token_end] == tokens, f"Inconsistent token list {tokenizer.decode_with_timestamps(chunck_indices[i_token_start:i_token_end])} != {tokenizer.decode_with_timestamps(tokens)}"
                        i_token_start += 1 # skip sos (start time)
                        if not unfinished_decoding:
                            i_token_end -= 1 # skip eos (end time)
                        segment_logprobs.append(logprobs[i_token_start:i_token_end])
                        segment_avglogprobs.append(avg_logprob)
                else:
                    for i in range(i_start, len(segment_tokens)-1):
                        segment_logprobs.append(None)
                        segment_avglogprobs.append(None)
            else:
                for i in range(i_start, len(segment_tokens)-1):
                    segment_logprobs.append(None)
                    segment_avglogprobs.append(None)

            if verbose_bugged and not should_skip:
                for segment in timestamped_word_segments[i_start:]:
                    for word in segment:
                        print_timestamped(word)

            # Reset counters
            chunk_tokens = []
            chunk_tokens_nosot = []
            chunk_logprobs = []
            no_speech_prob = None

    def hook_attention_weights(layer, ins, outs, index):
        nonlocal segment_attweights
        # In old version of whisper, output is a single tensor
        assert isinstance(outs, tuple) and len(outs) == 2, "whisper seems to be outdated, please update it (pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git)"
        w = outs[-1]
        # Only the last attention weights is useful
        if w.shape[-2] > 1:
            w = w[:, :, -1:, :]
        segment_attweights[index].append(w)

    def hook_mfcc(layer, ins, outs):
        nonlocal new_mfcc
        new_mfcc = ins[0]

    def hook_input_tokens(layer, ins, outs):
        nonlocal segment_tokens, sot_index, chunk_tokens, chunk_tokens_nosot, logit_filters, has_started, language, num_inference_steps
        num_inference_steps += 1

        curr_tokens = ins[0]
        assert curr_tokens.shape[0] == 1, "Batch decoding is not supported"
        curr_tokens = curr_tokens.squeeze(0)

        if len(curr_tokens) > 1 or curr_tokens[0] == tokenizer.sot:
            chunk_prompt = curr_tokens.tolist()
            if not has_started and language is None:
                if len(curr_tokens) == 1: # English model
                    language = "en"
                else:
                    language = tokenizer.decode(curr_tokens[1:2])[2:-2]
                whisper_options["language"] = language

                if verbose and not whisper_options["verbose"] and len(curr_tokens) > 1:
                    # Reproduce whisper verbose (2/2)
                    print(f"Detected language: {whisper.tokenizer.LANGUAGES[language].title()}")
                    sys.stdout.flush()

            logit_filters = get_logit_filters(model, whisper_options, prompt = chunk_prompt[1:-len(tokenizer.sot_sequence)])

        may_flush_segment(curr_tokens)

        # Keep the last token only
        segment_tokens[-1].append(curr_tokens[-1].item())

        # Get the index of the <|startoftranscript|> tokens (to get proba of silence later)
        if len(curr_tokens) > 1 or curr_tokens[0] == tokenizer.sot:
            has_started = True
            if no_speech_threshold is not None:
                sot_index = curr_tokens.tolist().index(tokenizer.sot)
        else:
            sot_index = None

        # Accumulate tokens
        if has_started:
            chunk_tokens.append(curr_tokens)
            if len(curr_tokens) == 1:
                chunk_tokens_nosot.append(curr_tokens[-1].item())
        else:
            if verbose and not whisper_options["verbose"]:
                # Reproduce whisper verbose (1/2)
                print("Detecting language using up to the first 30 seconds. Use `--language` to specify the language")

    embedding_weights = None
    def hook_output_logits(layer, ins, outs):
        nonlocal no_speech_prob, chunk_logprobs, segment_tokens, chunk_tokens, embedding_weights, has_started

        if embedding_weights is None:
            embedding_weights = torch.transpose(model.decoder.token_embedding.weight, 0, 1).to(outs[0].dtype)

        # Get the probability of silence
        if sot_index is not None:
            logits = (outs[0][sot_index,:] @ embedding_weights).float()
            logits = logits.softmax(dim=-1)
            no_speech_prob = logits[tokenizer.no_speech].item()

        # Get the log-probabilities of tokens (we don't know yet which one will be chosen)
        if has_started:
            logits = (outs[0][-1:,:] @ embedding_weights).float()
            tokens = torch.cat(chunk_tokens).unsqueeze(0)
            for logit_filter in logit_filters:
                logit_filter.apply(logits, tokens)
            logits = F.log_softmax(logits.squeeze(0), dim=-1)
            chunk_logprobs.append(logits)

    try:

        # Add hooks to the model, to get tokens and attention weights on the fly
        all_hooks = []
        all_hooks.append(model.encoder.conv1.register_forward_hook(hook_mfcc))
        all_hooks.append(model.decoder.token_embedding.register_forward_hook(hook_input_tokens))
        for i, block in enumerate(model.decoder.blocks):
            all_hooks.append(
                block.cross_attn.register_forward_hook(
                    lambda layer, ins, outs, index=i: hook_attention_weights(layer, ins, outs, index))
            )
        if compute_word_confidence or no_speech_threshold is not None:
            all_hooks.append(model.decoder.ln.register_forward_hook(hook_output_logits))

        transcription = model.transcribe(audio, **whisper_options)

    finally:

        # Remove hooks
        for hook in all_hooks:
            hook.remove()

    # Finalize (collect last segment)
    may_flush_segment()
    segment_tokens.pop(-1)

    token_special_idx = min(token_sot, token_eot)

    def filter_tokens(tokens):
        while len(tokens) and tokens[0] >= token_special_idx:
            tokens = tokens[1:]
        while len(tokens) and tokens[-1] >= token_special_idx:
            tokens = tokens[:-1]
        return tokens

    assert len(segment_tokens) == len(timestamped_word_segments), f"Inconsistent number of segments: tokens ({len(segment_tokens)}) != timestamped_word_segments ({len(timestamped_word_segments)})"
    assert len(segment_avglogprobs) == len(segment_tokens), f"Inconsistent number of segments: avg logprobs ({len(segment_avglogprobs)}) != tokens ({len(segment_tokens)})"
    assert len(segment_logprobs) == len(segment_tokens), f"Inconsistent number of segments: logprobs ({len(segment_logprobs)}) != tokens ({len(segment_tokens)})"

    whisper_segments = transcription["segments"]
    l1 = len(whisper_segments)
    l2 = len(timestamped_word_segments)
    if l1 != l2 and l1 != 0:
        logger.warning(f"Inconsistent number of segments: whisper_segments ({l1}) != timestamped_word_segments ({l2})")
    assert l1 == l2 or l1 == 0, f"Inconsistent number of segments: whisper_segments ({l1}) != timestamped_word_segments ({l2})"

    logger.debug("Compile results")
    words = []
    for i, (segment, timestamped_words, token, avglogprob, logprobs) in enumerate(zip(whisper_segments, timestamped_word_segments, segment_tokens, segment_avglogprobs, segment_logprobs)):
        timestamped_tokens = filter_tokens(token)
        whisper_tokens = filter_tokens(segment["tokens"])
        if timestamped_tokens != whisper_tokens:
            if len(timestamped_tokens) == len(whisper_tokens) + 1:
                logger.warn(f"An additional token was added on segment {i}")
            else:
                assert len(timestamped_tokens) < len(whisper_tokens) and timestamped_tokens == whisper_tokens[:len(timestamped_tokens)], \
                    f"Fatal Error: Got inconsistent text for segment {i}:\n({tokenizer.decode(timestamped_tokens)}) {timestamped_tokens}\n!=({len(whisper_tokens)}) \n{tokenizer.decode(whisper_tokens)}"
                logger.warn(f"Text had to be shortned on segment {i}:\n{tokenizer.decode(timestamped_tokens)}\n!=\n{tokenizer.decode(whisper_tokens)}")
            timestamped_words[-1]["avg_logprob_reliable"] = False

        offset = segment["seek"] * HOP_LENGTH / SAMPLE_RATE
        for timestamped_word in timestamped_words:
            timestamped_word["start"] += offset
            timestamped_word["end"] += offset
            timestamped_word["idx_segment"] = i

        if compute_word_confidence:
            if "avg_logprob_reliable" not in timestamped_words[-1] or timestamped_words[-1]["avg_logprob_reliable"]:
                if abs(segment["avg_logprob"] - avglogprob) >= 1e-2:
                    logger.warn(f"Recomputed different logprob for segment {i}: {avglogprob} != {segment['avg_logprob']}")
            if include_punctuation_in_confidence:
                segment["confidence"] = round_confidence(logprobs.mean().exp().item())
            else:
                logprobs_nopunc = []
            i_end = 0
            for timestamped_word in timestamped_words:
                i_start = i_end
                tokens = timestamped_word["tokens"]
                i_end += len(tokens)

                assert i_end <= len(logprobs), f"Fatal Error: Got out-of-bound index for segment {i}: {i_end} > {len(logprobs)}"
                if include_punctuation_in_confidence:
                    word_logprobs = logprobs[i_start:i_end]
                else:
                    tokens_str = [tokenizer.decode([t]) for t in tokens]
                    while len(tokens_str) > 1 and tokens_str[-1][-1] in _punctuation: # Note: look at the last character of token, to take into account "...", "!!", etc.
                        tokens_str = tokens_str[:-1]
                        tokens = tokens[:-1]
                    word_logprobs = logprobs[i_start:i_start + len(tokens)]
                    logprobs_nopunc.append(word_logprobs)

                timestamped_word["confidence"] = round_confidence(word_logprobs.mean().exp().item())

            if i_end != len(logprobs):
                logger.warn(f"Got inconsistent length for segment {i} ({len(logprobs)} != {i_end}). Some words have been ignored.")
            if not include_punctuation_in_confidence:
                logprobs_nopunc = torch.cat(logprobs_nopunc)
                segment["confidence"] = round_confidence(logprobs_nopunc.mean().exp().item())

        words.extend(timestamped_words)

    return transcription, words