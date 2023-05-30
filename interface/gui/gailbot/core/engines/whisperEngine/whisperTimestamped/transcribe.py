# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:09:26
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 16:53:39

import sys
import os

import whisper
from whisper.utils import format_timestamp
from whisper.audio import N_FRAMES, HOP_LENGTH, SAMPLE_RATE # 3000, 160, 16000

import torch
import torch.nn.functional as F

import numpy as np
import dtw
from scipy.ndimage import median_filter

import string

from .transcribe_efficient import _transcribe_timestamped_efficient
from .transcribe_naive import _transcribe_timestamped_naive

from .utils import (
    ensure_increasing_positions,
    print_timestamped
)

from .vars import (
    SAMPLE_RATE,
    AUDIO_SAMPLES_PER_TOKEN,
    N_FRAMES,
    AUDIO_TIME_PER_TOKEN
)

from typing import Dict, List

import logging
logger = logging.getLogger()

#################### GLOBALS ##################


###############################################


USE_EFFICIENT_BY_DEFAULT = True



############################ PUBLIC ######################################

def transcribe_timestamped(
    # Main Whisper options
    model,
    audio,
    language=None,
    task="transcribe",

    # Additional options for word alignment
    remove_punctuation_from_words=False,
    compute_word_confidence=True,
    include_punctuation_in_confidence=False,
    refine_whisper_precision=0.5,
    min_word_duration=0.04,
    plot_word_alignment=False,

    # Reproducibility
    seed=1234,

    naive_approach=False,

    # Other Whisper options
    temperature=0.0 if USE_EFFICIENT_BY_DEFAULT else (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    best_of=None,
    beam_size=None,
    patience=None,
    length_penalty=None,
    compression_ratio_threshold=2.4,
    logprob_threshold=-1.0,
    no_speech_threshold=0.6,
    fp16=None,
    condition_on_previous_text=True,
    initial_prompt=None,
    suppress_tokens="-1",
    sample_len=None,
    verbose=False,
):
    """
    Transcribe an audio file using Whisper

    Parameters
    ----------
    model: Whisper
        The Whisper model instance.

    audio: Union[str, np.ndarray, torch.Tensor]
        The path to the audio file to open, or the audio waveform.

    language: str
        The language to use for the transcription. If None, the language is detected automatically.

    task: str
        The task to perform: either "transcribe" or "translate".

    remove_punctuation_from_words: bool
        If False, words will be glued with the next punctuation mark (if any).
        If True, there will be no punctuation mark in the `words[:]["text"]` list.
        It only affects these strings; This has no influence on the computation of the word confidence, whatever the value of `include_punctuation_in_confidence` is.

    compute_word_confidence: bool
        Whether to compute word confidence.
        If True, a finer confidence for each segment will be computed as well.

    include_punctuation_in_confidence: bool
        Whether to include proba of punctuation in the computation of the (previous) word confidence.

    refine_whisper_precision: float
        How much can we refine Whisper segment positions, in seconds. Must be a multiple of 0.02.

    min_word_duration: float
        Minimum duration of a word, in seconds. If a word is shorter than this, timestamps will be adjusted.

    plot_word_alignment: bool
        Whether to plot the word alignment for each segment. matplotlib must be installed to use this option.

    seed: int
        Random seed to use for temperature sampling, for the sake of reproducibility.
        Choose None for unpredictable randomness.

    naive_approach: bool
        Force the naive approach that consists in decoding twice the audio file, once to get the transcritpion and once with the decoded tokens to get the alignment.
        Note that this approach is used anyway when beam_size is not None and/or when the temperature is a list with more than one element.

    temperature: float
        Temperature for sampling.

    compression_ratio_threshold: float
        If the gzip compression ratio is above this value, treat as failed.

    logprob_threshold: float
        If the average log probability over sampled tokens is below this value, treat as failed.

    no_speech_threshold: float
        If the no_speech probability is higher than this value AND the average log probability
        over sampled tokens is below `logprob_threshold`, consider the segment as silent.

    condition_on_previous_text: bool
        if True, the previous output of the model is provided as a prompt for the next window;
        disabling may make the text inconsistent across windows, but the model becomes less prone to
        getting stuck in a failure loop, such as repetition looping or timestamps going out of sync.

    initial_prompt: str
        Optional text to provide as a prompt for the first window.

    suppress_tokens: str
        Comma-separated list of token ids to suppress during sampling;
        '-1' will suppress most special characters except common punctuations.

    verbose: bool
        Whether to display the text being decoded to the console. If True, displays all the details,
        If False, displays minimal details. If None, does not display anything

    Returns
    -------
    A dictionary containing the resulting text ("text") and segment-level details ("segments"), and
    the spoken language ("language"), which is detected when `decode_options["language"]` is None.
    """

    if seed is not None:
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    # Check input options
    assert refine_whisper_precision >= 0 and refine_whisper_precision / AUDIO_TIME_PER_TOKEN == round(refine_whisper_precision / AUDIO_TIME_PER_TOKEN), f"refine_whisper_precision must be a positive multiple of {AUDIO_TIME_PER_TOKEN}"
    refine_whisper_precision_nframes = round(refine_whisper_precision / AUDIO_TIME_PER_TOKEN)
    assert min_word_duration >= 0, f"min_word_duration must be a positive number"

    if isinstance(temperature, (list, tuple)) and len(temperature) == 1:
        temperature = temperature[0]
    if isinstance(temperature, (list, tuple)):
        # temperature fallback
        naive_approach = True
    elif temperature > 0 and best_of is not None and best_of > 1:
        naive_approach = True
    if beam_size is not None:
        # beam-search
        naive_approach = True

    # Input options
    if fp16 is None:
        fp16 = model.device != torch.device("cpu")

    # Safety check
    input_stride = N_FRAMES // model.dims.n_audio_ctx
    time_precision = input_stride * HOP_LENGTH / SAMPLE_RATE
    assert time_precision == AUDIO_TIME_PER_TOKEN

    alignment_options = dict(
            remove_punctuation_from_words=remove_punctuation_from_words,
            compute_word_confidence=compute_word_confidence,
            include_punctuation_in_confidence=include_punctuation_in_confidence,
            refine_whisper_precision_nframes=refine_whisper_precision_nframes,
            plot_word_alignment=plot_word_alignment,
    )
    whisper_options = dict(
            language=language,
            task=task,
            fp16=fp16,
            temperature=temperature,
            best_of=best_of,
            beam_size=beam_size,
            patience=patience,
            length_penalty=length_penalty,
            condition_on_previous_text=condition_on_previous_text,
            initial_prompt=initial_prompt,
            suppress_tokens=suppress_tokens,
            sample_len=sample_len,
            verbose=verbose,
    )
    other_options = dict(
        no_speech_threshold=no_speech_threshold,
        logprob_threshold=logprob_threshold,
        compression_ratio_threshold=compression_ratio_threshold,
    )

    if naive_approach:
        (transcription, words) = _transcribe_timestamped_naive(model, audio, min_word_duration=min_word_duration, **alignment_options, **whisper_options, **other_options)
    else:
        (transcription, words) = _transcribe_timestamped_efficient(model, audio, **alignment_options, **whisper_options, **other_options)

    # Refine word positions

    ensure_increasing_positions(words, min_duration=min_word_duration)

    whisper_segments = transcription["segments"]
    for word in words:
        if verbose and not naive_approach:
            print_timestamped(word)
        word.pop("tokens")
        if "avg_logprob_reliable" in word:
            word.pop("avg_logprob_reliable")
        idx_segment = word.pop("idx_segment")
        segment = whisper_segments[idx_segment]
        if "words" in segment:
            segment["words"].append(word)
        else:
            segment["words"] = [word]
            if refine_whisper_precision:
                segment["start"] = word["start"]
        if refine_whisper_precision:
            segment["end"] = word["end"]

    return transcription


