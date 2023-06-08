# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 09:30:06
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 16:51:56

import sys
import os

import whisper
from whisper.utils import format_timestamp

import torch
import csv

import string

import logging
logger = logging.getLogger()


# TODO: Test and document these functions.


#################################
# Whisper model specific utils.
# These are the utility functions that are required for the transcription
# process.
#################################


def audio_minimum_padding(audio):
    if audio.shape[-1] <= 200:
        return whisper.pad_or_trim(audio, 201)
    return audio


def should_use_space(language):
    return norm_language(language) not in ["zh", "ja", "th", "lo", "my"]

def norm_language(language):
    return whisper.tokenizer.TO_LANGUAGE_CODE.get(language.lower(), language)

def print_timestamped(w):
    line = f"[{format_timestamp(w['start'])} --> {format_timestamp(w['end'])}] {w['text']}\n"
    # compared to just `print(line)`, this replaces any character not representable using
    # the system default encoding with an '?', avoiding UnicodeEncodeError.
    sys.stdout.buffer.write(line.encode(sys.getdefaultencoding(), errors="replace"))
    sys.stdout.flush()


def get_logit_filters(model, whisper_options, prompt = None):
    decoding_options = get_decoding_options(whisper_options)
    if "initial_prompt" in decoding_options:
        prompt0 = decoding_options.pop("initial_prompt")
        if prompt is None:
            prompt = prompt0
    if prompt is not None:
        decoding_options["prompt"] = prompt
    decoding_options = whisper.DecodingOptions(
        without_timestamps=False,
        max_initial_timestamp=1.0,
        prefix=None,
        suppress_blank=True,
        **decoding_options
    )

    # This performs some checks on the options
    decoding_task = whisper.decoding.DecodingTask(model, decoding_options)
    return decoding_task.logit_filters

def get_decoding_options(whisper_options):
    return dict([(k,v) for (k,v) in whisper_options.items()
        if k not in [
            "no_speech_threshold",
            "logprob_threshold",
            "compression_ratio_threshold",
            "condition_on_previous_text",
            "verbose",
        ]
    ])


def find_start_padding(mfcc):
    """ Return start of padding given the mfcc, or None if there is no padding """
    last_mfcc = mfcc[0, :, -1]
    if torch.min(last_mfcc) == torch.max(last_mfcc) == 0:
        candidate_index = mfcc.shape[-1] - 2
        while candidate_index > 0:
            candidate = mfcc[0, :, candidate_index]
            if not torch.equal(candidate, last_mfcc):
                return candidate_index + 1
            candidate_index -= 1
        return 0 # WTF!?

def round_confidence(x):
    return round(x, 3)

def round_timestamp(x):
    return round(x, 2)

_punctuation = "".join(c for c in string.punctuation if c not in ["-", "'"])

def split_tokens_on_unicode(
    tokens: list,
    tokenizer,
    tokens_as_string=False,
    remove_punctuation_from_words=False,
    isolate_punctuations=False
):
    words = []
    word_tokens = []
    current_tokens = []

    for token in tokens:
        current_tokens.append(token)
        decoded = tokenizer.decode_with_timestamps(current_tokens)
        if "\ufffd" not in decoded:
            punctuation = not isolate_punctuations and \
                (decoded.strip() and decoded.strip() in _punctuation)
            if punctuation:
                if len(words) == 0:
                    words = [""]
                    word_tokens = [[]]
                if not remove_punctuation_from_words:
                    words[-1] += decoded
                if tokens_as_string:
                    word_tokens[-1].append(decoded.strip())
                else:
                    word_tokens[-1].extend(current_tokens)
            else:
                words.append(decoded)
                word_tokens.append(
                    [decoded.strip()] if tokens_as_string else current_tokens)
            current_tokens = []

    return words, word_tokens


def split_tokens_on_spaces(
    tokens: torch.Tensor,
    tokenizer,
    tokens_as_string=False,
    remove_punctuation_from_words=False
):
    subwords, subword_tokens_list = split_tokens_on_unicode(
        tokens, tokenizer,
        tokens_as_string=tokens_as_string,
        remove_punctuation_from_words=remove_punctuation_from_words
    )
    words = []
    word_tokens = []

    for i, (subword, subword_tokens) in enumerate(zip(subwords, subword_tokens_list)):
        special = (subword_tokens[0].startswith("<|")) if tokens_as_string else (subword_tokens[0] >= tokenizer.eot)
        previous_special = i > 0 and (subword_tokens_list[i-1][0].startswith("<|")) if tokens_as_string else (subword_tokens_list[i-1][0] >= tokenizer.eot)
        with_space = subword.startswith(" ")
        punctuation = subword.strip() in _punctuation
        if special or (with_space and not punctuation) or previous_special:
            words.append(subword.strip())
            word_tokens.append(subword_tokens)
        else:
            words[-1] = words[-1] + subword.strip()
            word_tokens[-1].extend(subword_tokens)

    return words, word_tokens

def ensure_increasing_positions(segments, min_duration=0):
    """
    Ensure that "start" and "end" come in increasing order
    """
    has_modified_backward = False
    previous_end = 0
    for i, seg in enumerate(segments):
        if seg["start"] < previous_end:
            assert i > 0
            new_start = round_timestamp((previous_end + seg["start"]) / 2)
            if new_start < segments[i-1]["start"] + min_duration:
                new_start = previous_end
            else:
                segments[i-1]["end"] = new_start
                has_modified_backward = True
            seg["start"] = new_start
        if seg["end"] <= seg["start"] + min_duration:
            seg["end"] = seg["start"] + min_duration
        previous_end = seg["end"]
    if has_modified_backward:
        return ensure_increasing_positions(segments, min_duration)

    previous_end = 0
    for seg in segments:
        seg["start"] = round_timestamp(seg["start"])
        seg["end"] = round_timestamp(seg["end"])
        assert seg["start"] >= previous_end, f"Got segment {seg} coming before the previous finishes ({previous_end})"
        assert seg["end"] > seg["start"], f"Got segment {seg} with end <= start"
        previous_end = seg["end"]

    return segments

def supported_languages():
    return sorted(whisper.tokenizer.LANGUAGES.keys()) + sorted([k.title() \
        for k in whisper.tokenizer.TO_LANGUAGE_CODE.keys()])


#################################

#################################
# Other utils.
#################################


def flatten(list_of_lists, key = None):
    """
    Flatten a list of list into a single list
    """
    for sublist in list_of_lists:
        for item in sublist.get(key, []) if key else sublist:
            yield item

def write_csv(
    transcript,
    file,
    sep = ",",
    text_first=True,
    format_timestamps=None,
    header=False
):
    """
    Write a whisper generated transcript into a csv file.
    """
    writer = csv.writer(file, delimiter=sep)
    if format_timestamps is None: format_timestamps = lambda x: x
    if header is True:
        header = ["text", "start", "end"] if text_first \
            else ["start", "end", "text"]
    if header:
        writer.writerow(header)
    if text_first:
        writer.writerows(
            [[segment["text"].strip(), format_timestamps(segment["start"]),
                 format_timestamps(segment["end"])] for segment in transcript]
        )
    else:
        writer.writerows(
            [[format_timestamps(segment["start"]), format_timestamps(segment["end"]),
                segment["text"].strip()] for segment in transcript]
        )

# https://stackoverflow.com/questions/66588715/runtimeerror-cudnn-error-cudnn-status-not-initialized-using-pytorch
# CUDA initialization may fail on old GPU card
def force_cudnn_initialization(
    device=None,
    s=32
):
    if device is None:
        device = torch.device('cuda')
    torch.nn.functional.conv2d(torch.zeros(s, s, s, s, device=device), torch.zeros(s, s, s, s, device=device))

