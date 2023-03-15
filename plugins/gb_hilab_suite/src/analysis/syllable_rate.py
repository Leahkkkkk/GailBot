# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:32:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:12:15


import io
from typing import Dict, Any, List

from scipy.stats import median_abs_deviation
import syllables
import numpy
from gailbot.plugins.plugin import Plugin, Methods, Utt
from gb_hilab_suite.src.gb_hilab_suite import *


# The number of deviations above or below the absolute median deviation.
LimitDeviations = 2

delims = {
    "slowSpeech":  u'\u2207',
    "fastSpeech":  u'\u2206'
}


class SyllableRatePlugin(Plugin):

    def __init__(self) -> None:
        """
        Note: marker_limit value set to 4 for testing purpose
        """
        super().__init__()
        self.marker_limit = OVERLAP_MARKERLIMIT

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Methods) -> List[Utt]:
        """
        Calculates the syllable rates for each utterance and statistics for
        the conversation as a whole, including the median, MAD, fast speech
        counts and slow speech counts.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):
        """
        cm = dependency_outputs["conv_model"]
        utterances = cm.getUttMap(False)
        syll_dict = self.syll_rate(cm, utterances)

        cm.Maps["map3"]["uttLevel"]["uttRate"] = syll_dict
        # list of dic, each ele in dic is corr to an utt
        statsDic = self.stats(cm.Maps["map3"]["uttLevel"]["uttRate"])
        cm.Maps["map3"]["convLevel"]["stats"] = statsDic

        self.addDelims(cm, syll_dict, statsDic)

        self.successful = True


    def syll_rate(self, cm, utterances):
        """
        Calculates the syllable rates for each utterance
        """
        mapIter = cm.map_iterator(utterances) # iterator
        i = mapIter.iter() # i is the iterable object

        # while there is still an utterance
        syll_num = 0
        utt_syll_dict = [] # list of dictionary
        while i.hasNext():
            utt = i.next()
            curr_utt = cm.getWordFromNode(utt)
            syll_num = sum([syllables.estimate(word.text)
                                for word in curr_utt])
            utt_syll_dict.append({"utt": utt, "syllableNum": syll_num,
                                  "syllRate": round(syll_num/(abs(curr_utt[0].startTime - curr_utt[-1].endTime)), 2)})
        return utt_syll_dict


    def stats(self, utt_syll_dict):
        """
        Creates a dictionary containing the statistics
        """
        allRates = []
        for dic in utt_syll_dict:
            allRates.append(dic['syllRate'])

        allRates = numpy.sort(numpy.array(allRates))
        median = numpy.median(allRates)
        median_absolute_deviation = round(median_abs_deviation(allRates), 2)
        lowerLimit = (median-(LimitDeviations*median_absolute_deviation))
        upperLimit = (median+(LimitDeviations*median_absolute_deviation))
        return {"median": median, "medianAbsDev": median_absolute_deviation,
                "upperLimit": upperLimit, "lowerLimit": lowerLimit}

    def addDelims(self, cm, dictionaryList, statsDic):
        """
        Adds fast and slow speech delimiter markers into the tree.
        """
        vowels = ['a', 'e', 'i', 'o', 'u']
        fastCount = 0
        slowCount = 0
        for utt_dict in dictionaryList:
            utt_words = cm.getWordFromNode(utt_dict['utt'])

            # TODO: make this as a constant
            if utt_words[0].text != "%HESITATION":
                if utt_dict['syllRate'] <= statsDic['lowerLimit']:
                    # TO DO
                    if len(utt_words) == 1 and any(char in vowels for char in utt_words[0].text):
                        pos = self.lastVowelPos(utt_words[0].text)
                        colons = self.numColons(statsDic['medianAbsDev'],
                                                utt_dict['syllRate'],
                                                statsDic['median'])
                        # cm.insertToTree(utt_words[0].startTime,
                        #                 utt_words[0].startTime,
                        #                 SLOWSPEECH,
                        #                 markerText)
                        # utt_words[0].text = utt_words[0].text[:pos+1] + (":"*colons) + utt_words[0].text[pos+1:]
                    else:
                        markerText1 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                            str(MARKERTYPE) +
                                                            str(KEYVALUE_SEP) +
                                                            str(SLOWSPEECH_START),
                                                            str(MARKERINFO) +
                                                            str(KEYVALUE_SEP) +
                                                            delims['slowSpeech'],
                                                            str(MARKERSPEAKER) +
                                                            str(KEYVALUE_SEP) +
                                                            utt_words[0].sLabel)
                        markerText2 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                            str(MARKERTYPE) +
                                                            str(KEYVALUE_SEP) +
                                                            str(SLOWSPEECH_END),
                                                            str(MARKERINFO) +
                                                            str(KEYVALUE_SEP) +
                                                            delims['slowSpeech'],
                                                            str(MARKERSPEAKER) +
                                                            str(KEYVALUE_SEP) +
                                                            utt_words[0].sLabel)

                        cm.insertToTree(utt_words[0].startTime,
                                        utt_words[0].startTime,
                                        SLOWSPEECH_START,
                                        markerText1)
                        cm.insertToTree(utt_words[-1].endTime,
                                        utt_words[-1].endTime,
                                        SLOWSPEECH_END,
                                        markerText2)
                        slowCount += 1
                elif utt_dict['syllRate'] >= statsDic['upperLimit']:
                    markerText1 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                        str(MARKERTYPE) +
                                                        str(KEYVALUE_SEP) +
                                                        str(FASTSPEECH_START),
                                                        str(MARKERINFO) +
                                                        str(KEYVALUE_SEP) +
                                                        delims['fastSpeech'],
                                                        str(MARKERSPEAKER) +
                                                        str(KEYVALUE_SEP) +
                                                        utt_words[0].sLabel)

                    markerText2 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                        str(MARKERTYPE) +
                                                        str(KEYVALUE_SEP) +
                                                        str(FASTSPEECH_END),
                                                        str(MARKERINFO) +
                                                        str(KEYVALUE_SEP) +
                                                        delims['fastSpeech'],
                                                        str(MARKERSPEAKER) +
                                                        str(KEYVALUE_SEP) +
                                                        utt_words[0].sLabel)

                    cm.insertToTree(utt_words[0].startTime,
                                    utt_words[0].startTime,
                                    FASTSPEECH_START,
                                    markerText1)
                    cm.insertToTree(utt_words[-1].endTime,
                                    utt_words[-1].endTime,
                                    FASTSPEECH_END,
                                    markerText2)
                    fastCount += 1
        statsDic['fastturncount'] = fastCount
        statsDic['slowturncount'] = slowCount

    def lastVowelPos(self, string) -> int:
        """
        Calculates the last vowel position in a word string.
        """
        vowelList = []
        vowels = set("aeiouAEIOU")
        for pos, char in enumerate(string):
            if char in vowels:
                vowelList.append(pos)
        return vowelList[-1]

    def numColons(self, syllRateMAD, syllRateTurn, median) -> int:
        """
        Calculates the number of colons for slow speech.
        """
        syllRateDiff = abs(syllRateTurn - median)
        # Handling case where difference is 0 i.e. denominator cannot be 0.
        if syllRateDiff == 0:
            syllRateDiff = 0.1
        colons = int(round(syllRateDiff / syllRateMAD))
        return colons