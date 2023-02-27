# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:28:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 11:40:39


import sys
import os

import numpy as np
import torch
import dtw

# faster owing to https://github.com/openai/whisper/commit/f0083e7eb20d032390e42f6f6039947fa8669c93
from scipy.ndimage import median_filter

from .utils import (
    find_start_padding,
    split_tokens_on_spaces,
    split_tokens_on_unicode,
    round_timestamp

)
from .vars import (
    N_FRAMES,
    AUDIO_TIME_PER_TOKEN,
)

import logging
logger = logging.getLogger()


def perform_word_alignment(
    tokens,
    attention_weights,
    tokenizer,
    use_space=True,
    refine_whisper_precision_nframes=0,
    medfilt_width=9,
    qk_scale=1.0,
    most_top_layers=None,  # 6
    mfcc=None,
    plot=False,
    remove_punctuation_from_words=False,
    unfinished_decoding=False,
    debug=False,
):
    """
    Performs the word alignment on the given tokens and attention weights.

    A
    tokens: list of tokens (integers)
    attention_weights: list of attention weights (torch tensors)
    tokenizer: tokenizer used to tokenize the text
    use_space: whether to use spaces to split the tokens into words (should be true for all languages except Japanese, Chinese, ...)
    refine_whisper_precision_nframes: precision time

    Returns:
        A list of (word, start_time, end_time) tuples.
    """

    assert len(tokens) > 1, f"Got unexpected sequence of tokens of length \
        {len(tokens)} {tokenizer.decode_with_timestamps(tokens)}"
    start_token = tokens[0] - tokenizer.timestamp_begin
    end_token = tokens[-1] - tokenizer.timestamp_begin

    # Check start / end tokens
    if start_token < 0:
        raise RuntimeError(
            f"Missing start token in: {tokenizer.decode_with_timestamps(tokens)}")
    if len(tokens) == 1 or end_token < 0:
        # This can happens when Whisper is stucked as a Language Model
        if debug:
            logger.debug(
                f"Missing end token in {tokenizer.decode_with_timestamps(tokens)}"
            )
        end_token = N_FRAMES // 2
    if end_token == start_token and refine_whisper_precision_nframes == 0:
        if debug:
            logger.debug(
                f"Got empty segment in {tokenizer.decode_with_timestamps(tokens)}"
            )
        return []

    # Put some margin around the segment
    if refine_whisper_precision_nframes > 0:
        start_token = max(start_token - refine_whisper_precision_nframes, 0)
        end_token = min(
            end_token + refine_whisper_precision_nframes, N_FRAMES // 2)

    # Get the limit of audio duration
    max_duration = None
    if mfcc is not None:
        max_duration = find_start_padding(mfcc)
        if max_duration is not None:
            max_duration = max_duration // 2

    if end_token <= start_token:
        raise RuntimeError(
            f"Got segment with null or negative duration \
                {tokenizer.decode_with_timestamps(tokens)}: {start_token} {end_token}"
        )

    start_time = start_token * AUDIO_TIME_PER_TOKEN
    end_time = end_token * AUDIO_TIME_PER_TOKEN

    split_tokens = split_tokens_on_spaces if use_space else split_tokens_on_unicode
    words, word_tokens = split_tokens(
        tokens, tokenizer,
        remove_punctuation_from_words=remove_punctuation_from_words
    )

    for i, w in enumerate(attention_weights):
        assert w.shape[-2] == len(tokens),\
            f"Attention weights have wrong shape: {w.shape[-2]} (expected {len(tokens)})."
    weights = torch.cat(attention_weights)  # layers * heads * tokens * frames

    num_tokens = weights.shape[-2]
    num_frames = end_token - start_token
    if num_tokens > num_frames:
        logger.warning(
            f"Too much text ({num_tokens} tokens) for the given number of frames\
                 ({num_frames}) in: {tokenizer.decode_with_timestamps(tokens)}\
                    \nThe end of the text will be removed."
        )

        return perform_word_alignment(
            tokens[:num_frames-1] + [tokens[-1]],
            [torch.cat([w[:, :, :num_frames-1, :], w[:, :, -1:, :]], dim=-2)
                for w in attention_weights],
            tokenizer,
            use_space=use_space,
            refine_whisper_precision_nframes=refine_whisper_precision_nframes,
            medfilt_width=medfilt_width,
            qk_scale=qk_scale,
            most_top_layers=most_top_layers,
            mfcc=mfcc,
            plot=plot,
            remove_punctuation_from_words=remove_punctuation_from_words,
            unfinished_decoding=True,
            debug=debug,
        )

    assert end_token <= weights.shape[-1]
    assert len(tokens) == num_tokens

    weights = weights[:, :, :, start_token: end_token].cpu()

    weights = median_filter(weights, (1, 1, 1, medfilt_width))

    weights = torch.tensor(weights * qk_scale).softmax(dim=-1)
    # weights = weights.softmax(dim=-2)
    # TODO: Do we really need this?
    weights = weights / weights.norm(dim=-2, keepdim=True)

    if most_top_layers:
        weights = weights[-most_top_layers:]  # at most 6 top layers
    weights = weights.mean(axis=(0, 1))  # average over layers and heads
    weights = -weights.double().numpy()

    # Enforce the max duration
    if max_duration:
        if start_token >= max_duration:
            logger.warn(f"Got start time outside of audio boundary")
        else:
            weights[:-1, max_duration:] = 0

    # Similar as "symmetric1" but without the possibility to have the same timestamp for two tokens
    step_pattern = dtw.stepPattern.StepPattern(dtw.stepPattern._c(
        1, 1, 1, -1,
        1, 0, 0, 1,
        2, 0, 1, -1,
        2, 0, 0, 1,
    ))
    alignment = dtw.dtw(weights, step_pattern=step_pattern)

    if plot:
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker

        word_tokens_str = [[tokenizer.decode_with_timestamps(
            [ti]) for ti in t] for t in word_tokens]

        if mfcc is None:
            plt.figure(figsize=(16, 9), frameon=False)
        else:
            plt.subplots(2, 1, figsize=(16, 9), gridspec_kw={
                         'height_ratios': [3, 1]})
            plt.subplot(2, 1, 1, frameon=False)

        plt.imshow(-weights, aspect="auto")
        plt.plot(alignment.index2s, alignment.index1s, color="red")

        xticks = np.arange(0, weights.shape[1], 1 / AUDIO_TIME_PER_TOKEN)
        xticklabels = [round_timestamp(
            x) for x in xticks * AUDIO_TIME_PER_TOKEN + start_time]

        ylims = plt.gca().get_ylim()

        ax = plt.gca()
        ax.tick_params('both', length=0, width=0, which='minor', pad=6)

        ax.yaxis.set_ticks_position("left")
        ax.yaxis.set_label_position("left")
        ax.invert_yaxis()
        ax.set_ylim(ylims)

        major_ticks = [-0.5]
        minor_ticks = []
        current_y = 0

        for word, word_token in zip(words, word_tokens):
            minor_ticks.append(current_y + len(word_token) / 2 - 0.5)
            current_y += len(word_token)
            major_ticks.append(current_y - 0.5)

        words_with_subwords = ["|".join(s) for (
            w, s) in zip(words, word_tokens_str)]

        ax.yaxis.set_minor_locator(ticker.FixedLocator(minor_ticks))
        ax.yaxis.set_minor_formatter(
            ticker.FixedFormatter(words_with_subwords))
        ax.set_yticks(major_ticks)
        ax.yaxis.set_major_formatter(ticker.NullFormatter())
        for y in major_ticks:
            plt.axhline(y, color="black", linestyle="dashed")

        plt.ylabel("Words")

        if mfcc is not None:
            plt.xticks(xticks)
            plt.setp(plt.gca().get_xticklabels(), visible=False)

            xticks *= 2

            plt.subplot(2, 1, 2, frameon=False)
            plt.imshow(mfcc[0, :, start_token *
                       2: end_token * 2].cpu(), aspect="auto")
            plt.yticks([])
            plt.ylabel("MFCC")

        plt.xticks(xticks, xticklabels)
        plt.xlabel("Time (s)")

    jumps = np.diff(alignment.index1s)
    jumps = np.pad(jumps, (1, 0), constant_values=1)
    jumps = jumps.astype(bool)
    jumps = alignment.index2s[jumps]
    jump_times = jumps * AUDIO_TIME_PER_TOKEN
    jump_times = np.pad(jump_times, (0, 1),
                        constant_values=end_time - start_time)

    # display the word-level timestamps in a table
    word_boundaries = np.cumsum([len(t) for t in word_tokens])
    word_boundaries = np.pad(word_boundaries, (1, 0))
    begin_times = jump_times[word_boundaries[:-1]]
    end_times = jump_times[word_boundaries[1:]]

    # Ignore start / end tokens
    if not refine_whisper_precision_nframes:
        begin_times[1] = begin_times[0]
    if not refine_whisper_precision_nframes:
        end_times[-2] = end_times[-1]
    if unfinished_decoding:
        words = words[1:]
        word_tokens = word_tokens[1:]
        begin_times = begin_times[1:]
        end_times = end_times[1:]
    else:
        words = words[1:-1]
        word_tokens = word_tokens[1:-1]
        begin_times = begin_times[1:-1]
        end_times = end_times[1:-1]

    if plot:
        ymin = 1

        if mfcc is not None:
            for i, (begin, end) in enumerate(zip(begin_times, end_times)):
                for x in [begin, end,] if i == 0 else [end,]:
                    plt.axvline(x * 2 / AUDIO_TIME_PER_TOKEN,
                                color="red", linestyle="dotted")

            plt.subplot(2, 1, 1)

        for i, (w, ws, begin, end) in enumerate(zip(words, word_tokens, begin_times, end_times)):
            ymax = ymin + len(ws)
            plt.text(begin / AUDIO_TIME_PER_TOKEN, num_tokens,
                     w, ha="left", va="top", color="red")
            for x in [begin, end,] if i == 0 else [end,]:
                plt.axvline(x / AUDIO_TIME_PER_TOKEN, color="red", linestyle="dotted",
                            ymin=1-ymin/num_tokens,
                            ymax=0,  # 1-ymax/num_tokens,
                            )
            ymin = ymax

        plt.show()

    return [
        dict(
            text=word,
            start=round_timestamp(begin + start_time),
            end=round_timestamp(end + start_time),
            tokens=tokens,
        )
        for word, begin, end, tokens in zip(words, begin_times, end_times, word_tokens)
        if not word.startswith("<|")
    ]
