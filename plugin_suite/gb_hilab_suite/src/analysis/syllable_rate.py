# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:32:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:12:15


from typing import Dict, Any, List, TypedDict
import logging
from scipy.stats import median_abs_deviation
import syllables
import numpy
from gailbot import Plugin, GBPluginMethods, UttObj
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.core.nodes import Node
from gb_hilab_suite.src.configs import INTERNAL_MARKER, load_threshold, PLUGIN_NAME
MARKER = INTERNAL_MARKER 
THRESHOLD = load_threshold()
class SYLL_DICT(TypedDict):
    utt: List[Node]
    syllableNum: int 
    syllRate: float
        

class STAT_DICT(TypedDict):
    median: float
    medianAbsDev: float
    upperLimit: float
    lowerLimit: float
    fastturncount: int 
    slowturncount: int 

# The number of deviations above or below the absolute median deviation.
LimitDeviations = 2

class SyllableRatePlugin(Plugin):
    def __init__(self) -> None:
        """
        Note: marker_limit value set to 4 for testing purpose
        """
        super().__init__()
        self.marker_limit = THRESHOLD.OVERLAP_MARKERLIMIT

    def apply(self, dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods) -> List[UttObj]:
        """
        Calculates the syllable rates for each utterance and statistics for
        the conversation as a whole, including the median, MAD, fast speech
        counts and slow speech counts.

        Args:
            dependency_outputs (Dict[str, Any]):
            methods (PluginMethodSuite):
        """
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        utterances = cm.getUttMap(False)
        syll_dict = self.syll_rate(cm, utterances)
        logging.debug("computed syllable dictionary")
        cm.Maps["map3"]["uttLevel"]["uttRate"] = syll_dict
        
        # list of dic, each ele in dic is corr to an utt
        statsDic = self.stats(cm.Maps["map3"]["uttLevel"]["uttRate"])
        cm.Maps["map3"]["convLevel"]["stats"] = statsDic

        # add marker to the tree based on the syllable dictionary
        self.addDelims(cm, syll_dict, statsDic)

        self.successful = True
        return cm


    def syll_rate(self, cm: ConversationModel, utterances: List[UttObj]) -> List[SYLL_DICT]:
        """
        Calculates the syllable rates for each utterance
        """
        logging.debug("start computing syllable dictionary")
        mapIter = cm.map_iterator(utterances) # iterator
        i = mapIter.iter() # i is the iterable object

        # while there is still an utterance
        syll_num = 0
        utt_syll_dict = [] # list of dictionary
        
        while i.hasNext():
            utt = i.next()
            curr_utt = cm.getWordFromNode(utt)
            syll_num = sum([syllables.estimate(word.text) for word in curr_utt])
            logging.debug(f"estimated syllable num {syll_num}")
            time_diff = abs(curr_utt[0].startTime - curr_utt[-1].endTime)
            logging.warn(f"get time {curr_utt[0].startTime} and {curr_utt[-1].endTime}")
        
            if time_diff == 0:
                logging.warn(f"get no 0 time difference between the words {curr_utt[0].text} and {curr_utt[-1].text}")
                time_diff = 0.001
                
            syll_rate = round(syll_num / time_diff, 2)
            new_syll_dict: SYLL_DICT = {"utt": utt, "syllableNum": syll_num, "syllRate": syll_rate} 
            logging.debug(f"get new syllable dictionary {new_syll_dict}")
            utt_syll_dict.append(new_syll_dict)
            
        return utt_syll_dict


    def stats(self, utt_syll_dict) -> STAT_DICT:
        """
        Creates a dictionary containing the statistics
        """
        logging.debug("start analysis syllable rate stats")
        allRates = []
        for dic in utt_syll_dict:
            allRates.append(dic['syllRate'])

        allRates = numpy.sort(numpy.array(allRates))
        median = numpy.median(allRates)
        median_absolute_deviation = round(median_abs_deviation(allRates), 2)
        lowerLimit = (median-(LimitDeviations*median_absolute_deviation))
        upperLimit = (median+(LimitDeviations*median_absolute_deviation))
        stats: STAT_DICT = {"median": median, 
                            "medianAbsDev": median_absolute_deviation,
                            "upperLimit": upperLimit, 
                            "lowerLimit": lowerLimit}
        logging.debug(f"computed syllable rate stats {stats}")
        return stats

    def addDelims(self, cm: ConversationModel,
                  dictionaryList: List[SYLL_DICT], 
                  statsDic: STAT_DICT):
        """
        Adds fast and slow speech delimiter markers into the tree.
        """
        logging.debug("start add marker to syllable tree")
        vowels = ['a', 'e', 'i', 'o', 'u']
        fastCount = 0
        slowCount = 0
        for utt_dict in dictionaryList:
            utt_words = cm.getWordFromNode(utt_dict['utt'])

            if utt_words[0].text not in MARKER.UTT_PAUSE_MARKERS:
                if utt_dict['syllRate'] <= statsDic['lowerLimit']:
                    logging.debug("detect potential slow speech")
                    if len(utt_words) == 1 and any(char in vowels for char in utt_words[0].text):
                        pos = self.lastVowelPos(utt_words[0].text)
                        colons = self.numColons(statsDic['medianAbsDev'],
                                                utt_dict['syllRate'],
                                                statsDic['median'])
                    else:
                        markerText1 = MARKER.TYPE_INFO_SP.format(
                            MARKER.SLOWSPEECH_START, MARKER.SLOWSPEECH_DELIM, utt_words[0].sLabel)
                        markerText2 = MARKER.TYPE_INFO_SP.format(
                            MARKER.SLOWSPEECH_END, MARKER.SLOWSPEECH_DELIM, utt_words[0].sLabel)

                        cm.insertToTree(utt_words[0].startTime,
                                        utt_words[0].startTime,
                                        MARKER.SLOWSPEECH_START,
                                        markerText1)
                        cm.insertToTree(utt_words[-1].endTime,
                                        utt_words[-1].endTime,
                                        MARKER.SLOWSPEECH_END,
                                        markerText2)
                        logging.debug(f"insert marker for slow speech start {markerText1}, \
                                        and slow speech end {markerText2}")
                        slowCount += 1
                elif utt_dict['syllRate'] >= statsDic['upperLimit']:
                    markerText1 = MARKER.TYPE_INFO_SP.format(
                        MARKER.FASTSPEECH_END, MARKER.FASTSPEECH_DELIM, utt_words[0].sLabel)
                    markerText2 = MARKER.TYPE_INFO_SP.format(
                        MARKER.FASTSPEECH_END, MARKER.FASTSPEECH_DELIM, utt_words[0].sLabel)
                   
                    cm.insertToTree(utt_words[0].startTime,
                                    utt_words[0].startTime,
                                    MARKER.FASTSPEECH_START,
                                    markerText1)
                    cm.insertToTree(utt_words[-1].endTime,
                                    utt_words[-1].endTime,
                                    MARKER.FASTSPEECH_END,
                                    markerText2)
                    logging.debug(f"insert marker for fast speech start {markerText1}, \
                                    and fast speech end {markerText2}")
                    fastCount += 1
        logging.debug(f"the total count for fast speech is {fastCount}, for slow speech is {slowCount}")
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
        if syllRateMAD == 0: 
            syllRateMAD = 0.1
        # OverflowError: cannot convert float infinity to integer
        colons = int(round(syllRateDiff / syllRateMAD))
        return colons