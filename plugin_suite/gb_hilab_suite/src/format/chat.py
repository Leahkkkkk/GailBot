# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:16:03
import os 
import logging
from typing import Dict, Any
# Local imports
from gailbot import Plugin, GBPluginMethods, UttObj
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.configs import INTERNAL_MARKER, load_label, OUTPUT_FILE, PLUGIN_NAME, CHAT_FORMATTER

MARKER = INTERNAL_MARKER
LABEL = load_label().CHAT

class ChatPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods):
        """
        Prints the entire tree in a user-specified chat format
        """
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
                MARKER.GAPS:                 LABEL.GAPMARKER,
                MARKER.OVERLAP_FIRST_START:  LABEL.OVERLAPMARKER_CURR_START,
                MARKER.OVERLAP_FIRST_END:    LABEL.OVERLAPMARKER_CURR_END,
                MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER_NEXT_START,
                MARKER.OVERLAP_SECOND_END:   LABEL.OVERLAPMARKER_NEXT_END,
                MARKER.PAUSES:               LABEL.PAUSE,
                MARKER.FASTSPEECH_START:     MARKER.FASTSPEECH_DELIM,
                MARKER.FASTSPEECH_END:       MARKER.FASTSPEECH_DELIM,
                MARKER.SLOWSPEECH_START:     MARKER.SLOWSPEECH_DELIM,
                MARKER.SLOWSPEECH_END:       MARKER.SLOWSPEECH_DELIM
        }
        # Gets tree and utterance map from conversation model generated from dependency map

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        # start printing to file
        # header of the file 
        # TODO: eng? 
        data = [
            CHAT_FORMATTER.HEADER_LANGUAGE.format("eng")
        ]
        
        path = os.path.join(methods.output_path, OUTPUT_FILE.CHAT)
        utterances = newUttMap
        with open(path, "w", encoding='utf-8') as outfile:
            for item in data:
                outfile.write(item)
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                l = []
                for word in curr_utt:
                    l.append(word.text)
                txt = CHAT_FORMATTER.TXT_SEP.join(l)
                if (curr_utt[0].sLabel != LABEL.PAUSE and
                    curr_utt[0].sLabel != LABEL.GAPMARKER):
                    sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
                else:
                    sLabel = ""
                # actual text content 
                turn = CHAT_FORMATTER.TURN.format(
                    sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime,
                    0x15)

                outfile.write(turn)
        self.successful = True
        return