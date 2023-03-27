# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:16:03

from typing import Dict, Any
# Local imports
from gailbot import Plugin, GBPluginMethods, UttObj
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.config import MARKER, THRESHOLD, LABEL, PLUGIN_NAME


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
                MARKER.GAPS: LABEL.CHAT_GAPMARKER,
                MARKER.MARKER1: LABEL.OVERLAPMARKER_CURR_START,
                MARKER.MARKER2: LABEL.OVERLAPMARKER_CURR_END,
                MARKER.MARKER3: LABEL.OVERLAPMARKER_NEXT_START,
                MARKER.MARKER4: LABEL.OVERLAPMARKER_NEXT_END,
                MARKER.PAUSES: LABEL.CHAT_PAUSE,
                MARKER.FASTSPEECH_START: MARKER.FASTSPEECH_START,
                MARKER.FASTSPEECH_END: MARKER.FASTSPEECH_END,
                MARKER.SLOWSPEECH_START: MARKER.SLOWSPEECH_START,
                MARKER.SLOWSPEECH_END: MARKER.SLOWSPEECH_END
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        # start printing to file
        data = [
            "@Begin\n@Languages:\t{0}\n".format("eng")
        ]
        
        path = "{}/conversation.cha".format(methods.output_path)

        utterances = newUttMap
        with open(path, "w", encoding='utf-8') as outfile:
            for item in data:
                outfile.write(item)
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                l = []
                for word in curr_utt:
                    l.append(word.text)
                txt = ' '.join(l)

                sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)

                turn = '{0}\t{1} {2}{4}_{3}{4}\n'.format(
                    sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime,
                    0x15)

                outfile.write(turn)
        self.successful = True
        return