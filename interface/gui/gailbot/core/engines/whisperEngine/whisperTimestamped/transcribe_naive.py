# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:29:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-03-15 15:53:40

import sys
import os

import numpy as np
import whisper
import torch
import torch.nn.functional as F

from .alignment import perform_word_alignment
from .utils import (
    norm_language,
    should_use_space,
    print_timestamped,
    round_confidence,
    audio_minimum_padding
)
from .vars import (
    AUDIO_SAMPLES_PER_TOKEN,
    AUDIO_TIME_PER_TOKEN,
    SAMPLE_RATE,
    N_FRAMES
)

import string

import logging
logger = logging.getLogger()


_punctuation = "".join(c for c in string.punctuation if c not in ["-", "'"])



def _transcribe_timestamped_naive(
    model,
    audio,
    remove_punctuation_from_words,
    compute_word_confidence,
    include_punctuation_in_confidence,
    refine_whisper_precision_nframes,
    plot_word_alignment,
    min_word_duration,
    **whisper_options,
):
    verbose = whisper_options["verbose"]
    whisper_options["verbose"] = None if whisper_options["verbose"] is True else whisper_options["verbose"]  # We will print intermediate results ourselves
    language = whisper_options["language"]
    refine_whisper_precision_sec = refine_whisper_precision_nframes * AUDIO_TIME_PER_TOKEN

    if isinstance(audio, str):
        audio = whisper.load_audio(audio)
    if isinstance(audio, np.ndarray):
        audio = torch.Tensor(audio)
    else:
        assert isinstance(audio, torch.Tensor), f"Got unexpected audio of type {type(audio)}"

    audio = audio.to(model.device)
    audio_duration = audio.shape[-1] / SAMPLE_RATE

    if verbose and language is None and not whisper_options["verbose"]:
        # Reproduce whisper verbose (1/2)
        print("Detecting language using up to the first 30 seconds. Use `--language` to specify the language")

    transcription = model.transcribe(audio, **whisper_options)

    if verbose and language is None and not whisper_options["verbose"]:
        # Reproduce whisper verbose (2/2)
        print(f"Detected language: {whisper.tokenizer.LANGUAGES[transcription['language']].title()}")
        sys.stdout.flush()

    language = norm_language(transcription["language"])

    tokenizer = whisper.tokenizer.get_tokenizer(model.is_multilingual, task=whisper_options["task"], language=language)
    use_space = should_use_space(language)

    attention_weights = [[] for _ in range(len(model.decoder.blocks))]

    try:

        all_hooks = []

        # Hook the model
        for i, block in enumerate(model.decoder.blocks):
            all_hooks.append(
                block.cross_attn.register_forward_hook(
                    lambda layer, ins, outs, index=i: attention_weights.__setitem__(index, outs[-1])
                )
            )

        words = []
        previous_end = 0
        whisper_segments = transcription["segments"]
        for i_segment, segment in enumerate(whisper_segments):

            start = segment["start"]
            end = segment["end"]
            if end < start:
                # Whisper is wrong on the prediction of segment end
                end = min(audio_duration, start + 30.0)

            start_margin_min = start - refine_whisper_precision_sec
            start_margin_max = start + refine_whisper_precision_sec
            if start >= audio_duration - min_word_duration or (previous_end >= start_margin_min and previous_end <= start_margin_max):
                # Make start as accurate as possible (as the decoding will start with timestamp <|0|>)
                start = previous_end
            else:
                # Fallback
                start = start_margin_min

            if start > audio_duration - min_word_duration:
                # Skip last segment if too short
                logger.warn(f"Skipping segment outside of audio duration {audio_duration} (original: {segment['start']}-{segment['end']}, new: {start}-XXX)")
                continue

            end_margin_min = end - refine_whisper_precision_sec
            end_margin_max = end + refine_whisper_precision_sec
            if i_segment < len(whisper_segments) - 1:
                # Try to enforce:
                #   end + min_word_duration <= next start + refine_whisper_precision_sec
                end_margin_max2 = whisper_segments[i_segment + 1]["start"] + refine_whisper_precision_sec - min_word_duration
                if end_margin_max2 >= end_margin_min:
                    end_margin_max = min(end_margin_max2, end_margin_max)
            end = min(audio_duration, end_margin_max)

            if end < start + min_word_duration:
                logger.warn(f"Got super short segment (original from whisper: {segment['start']}-{segment['end']}, new: {start, end})")
                end = min(audio_duration, start + min_word_duration)
                if end <= start:
                    logger.warn(f"Skipping this short segment occuring too close to the end of the audio")
                    continue

            start_sample = min(round(start * SAMPLE_RATE), audio.shape[-1])
            end_sample = min(round(end * SAMPLE_RATE), audio.shape[-1])

            sub_audio = audio_minimum_padding(audio[start_sample:end_sample])

            mfcc = whisper.log_mel_spectrogram(sub_audio).to(model.device)
            mfcc = whisper.pad_or_trim(mfcc, N_FRAMES)
            mfcc = mfcc.unsqueeze(0)

            tokens = segment["tokens"]
            # assert len(tokens), "Got empty transcription!"
            if tokens:
                if tokens[0] == tokenizer.timestamp_begin:
                    tokens = tokens[1:]
                while tokens[-1] >= tokenizer.timestamp_begin:
                    tokens = tokens[:-1]
                    assert len(tokens), "Got transcription with only timestamps!"

                tokens = [
                        *tokenizer.sot_sequence,
                        tokenizer.timestamp_begin,
                    ] + tokens

                i_start = len(tokenizer.sot_sequence)

                with torch.no_grad():
                    logprobs = model(mfcc, torch.Tensor(tokens).int().to(model.device).unsqueeze(0))
                    logprobs = F.log_softmax(logprobs, dim=-1)

                tokens = tokens[i_start:] + [tokenizer.timestamp_begin + round((end_sample - start_sample) // AUDIO_SAMPLES_PER_TOKEN)]
                attention_weights = [w[:, :, i_start-1:, :] for w in attention_weights]

                ws = perform_word_alignment(
                    tokens,
                    attention_weights,
                    tokenizer,
                    use_space=use_space,
                    remove_punctuation_from_words=remove_punctuation_from_words,
                    refine_whisper_precision_nframes=refine_whisper_precision_nframes,
                    mfcc=mfcc,
                    plot=plot_word_alignment,
                )

                segment_logprobs = []
                for w in ws:

                    w["start"] = round(w["start"] + start, 2)
                    w["end"] = round(w["end"] + start, 2)

                    w.update({"idx_segment": i_segment})

                    if compute_word_confidence:
                        tokens = w["tokens"]
                        i_end = i_start + len(tokens)
                        if include_punctuation_in_confidence:
                            tokens_str = [tokenizer.decode([t]) for t in tokens]
                            while len(tokens_str) > 1 and tokens_str[-1][-1] in _punctuation: # Note: look at the last character of token, to take into account "...", "!!", etc.
                                tokens_str = tokens_str[:-1]
                                tokens = tokens[:-1]
                        word_logprobs = [logprobs[:, step, tok] for (step, tok) in zip(range(i_start, i_start + len(tokens)), tokens)]
                        i_start = i_end
                        word_logprobs = torch.cat(word_logprobs)
                        w.update({"confidence": round_confidence(word_logprobs.mean().exp().item())})
                        segment_logprobs.append(word_logprobs)

                    words.append(w)

                    if verbose:
                        print_timestamped(w)

                if len(segment_logprobs):
                    segment.update({"confidence": round_confidence(torch.cat(segment_logprobs).mean().exp().item())})

                if len(ws):
                    previous_end = ws[-1]["end"]
    finally:

        # Remove hooks
        for hook in all_hooks:
            hook.remove()

    return (transcription, words)