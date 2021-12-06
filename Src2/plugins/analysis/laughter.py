# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 21:48:12
# Standard imports
from typing import Dict, Any, List, Tuple
import re
import numpy as np
import librosa
import keras
import scipy.signal as signal
# Local imports
from Src2.components import GBPlugin, PluginMethodSuite, Utt


class Laughter(GBPlugin):

    MODEL_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot-0.3/Src2/plugins/analysis/model.h5"
    AUDIO_SAMPLE_RATE = 44100

    def __init__(self) -> None:
        self.lb_gap = 0.3
        self.model = keras.models.load_model(self.MODEL_PATH)
        self.successful = False

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        try:
            new_map = dict()
            audio_paths = plugin_input.get_audio_paths()
            utterances_map = plugin_input.get_utterances()
            for identifier, utterances in utterances_map.items():
                print("HERE")
                print(audio_paths)
                audio_path = audio_paths[identifier]
                print(audio_path)
                instances = self._segment_laugh(audio_path, 0.4, 0.05)
                print(instances)
                utterances = self._transcribe_laughter(utterances, instances)
                new_map[identifier] = utterances
            self.successful = True
            print(new_map)
            return new_map
        except Exception as e:
            self.successful = False
            print("laughter", e)

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return self.successful

    ################################# PRIVATE  ###############################

    def _segment_laugh(
            self, audio_file_path: str, min_laugh_prob: float,
            min_laugh_length):
        timeSeries, samplingRate = librosa.load(
            audio_file_path, sr=self.AUDIO_SAMPLE_RATE)
        # Getting a list of different audio features for analysis.
        featureList = self._getFeatureList(timeSeries, samplingRate)
        # Generating output prediction for input samples.
        probs = self.model.predict_proba(featureList, verbose=1)
        # Reshaping the tensor to the specified shape for further use in the neural
        # network/
        probs = probs.reshape(len(probs))
        # Filtering the input signal using the butterworth filter.
        filtered = self._lowpass(probs)
        return self._getLaughterInstances(
            filtered, min_laugh_prob, min_laugh_length)

    def _getFeatureList(self, timeSeries, samplingRate, window_size=37):

        # Computing MFCC features.
        mfccFeatures = self._computeMfccFeatures(timeSeries, samplingRate)
        # Computing delta features.
        deltaFeatures = self._computeDeltaFeatures(mfccFeatures)
        zeroPadMFCC = np.zeros((window_size, mfccFeatures.shape[1]))
        zeroPadDelta = np.zeros((window_size, deltaFeatures.shape[1]))
        paddedMFCCFeatures = np.vstack(
            [zeroPadMFCC, mfccFeatures, zeroPadMFCC])
        paddedDeltaFeatures = np.vstack(
            [zeroPadDelta, deltaFeatures, zeroPadDelta])
        featureList = []
        for i in range(window_size, len(mfccFeatures)+window_size):
            featureList.append(self._formatFeatures(
                paddedMFCCFeatures, paddedDeltaFeatures,
                i, window_size))
        featureList = np.array(featureList)
        return featureList

    def _computeMfccFeatures(self, timeSeries, samplingRate):

        # Extractign the mel-frequency coefficients.
        # DCT type-II transform is used and 30 frequency bins are created.
        # Also computing a mel-sclaed spectogram.
        # Hop-length is the number of samples between successive frames. / columns of a spectogram.
        # The .T attribute is the transpose of the np array
        mfccFeatures = librosa.feature.mfcc(
            y=timeSeries, sr=samplingRate,
            n_mfcc=12, n_mels=12, hop_length=int(samplingRate/100),
            dct_type=2, n_fft=int(samplingRate/40)).T

        # Separating the complex valued Spectrogram D into its magnitude and phase components.
        # A complex valued spectogram does not have any negative frequency components.
        complexValuedMatrix = librosa.stft(
            timeSeries, hop_length=int(samplingRate/100))
        magnitude, phase = librosa.magphase(complexValuedMatrix)

        # Calculating the root-mean-square value / mean of the cosing function
        # Transposing the resultant matrix.
        rms = librosa.feature.rms(S=magnitude).T

        # stacking the arrays horizontally and returns resultant feature list.
        return np.hstack([mfccFeatures, rms])

    # Function that computes the delta features for the given time series.
    # Generates the local estimate of the first and second derivative of the input
    # data along the selected axis.
    # Input: Mel Frequency Cepstral Coefficients.
    # Returns: Delta features.

    def _computeDeltaFeatures(self, mfccFeatures):
        return np.vstack([librosa.feature.delta(mfccFeatures.T),
                          librosa.feature.delta(mfccFeatures.T, order=2)]).T

    # Function that formats mfcc and delta features in the correct format to use.
    def _formatFeatures(self, mfccFeatures, deltaFeatures, index, window_size=37):
        return np.append(mfccFeatures[index-window_size:index+window_size],
                         deltaFeatures[index-window_size:index+window_size])

    # Applying a lowpass filter to the audio.
    def _lowpass(self, sig, filter_order=2, cutoff=0.01):
        # Set up Butterworth filter

        filter_order = 2

        # Create a butterworth filter of the second order with
        # ba (numerator/denominator) output.
        B, A = signal.butter(filter_order, cutoff, output='ba')

        # Applies the linear filter twice to the signal,
        # Once forwards, and once backwards.
        return(signal.filtfilt(B, A, sig))

    # Extracts laughter from the filtered audio.
    def _frame_span_to_time_span(self, frame_span):
        return (frame_span[0] / 100., frame_span[1] / 100.)

    def _collapse_to_start_and_end_frame(self, instance_list):
        return (instance_list[0], instance_list[-1])

    def _getLaughterInstances(self, probs, threshold=0.5, minLength=0.2):
        instances = []
        current_list = []
        for i in range(len(probs)):
            if np.min(probs[i:i+1]) > threshold:
                current_list.append(i)
            else:
                if len(current_list) > 0:
                    instances.append(current_list)
                    current_list = []
        instances = [self._frame_span_to_time_span(
            self._collapse_to_start_and_end_frame(
                i)) for i in instances if len(i) > minLength]
        return instances

    def _transcribe_laughter(self, utterances, instances):
        new_utterances = list()
        for instance in instances:
            utterance = Utt(
                "", instance[0], instance[1], "&=laughs")
            new_utterances.append(utterance)
        for item in utterances:
            new_utterances.append(item)
        new_utterances.sort(key=lambda utt: utt.start_time_seconds)
        return new_utterances
