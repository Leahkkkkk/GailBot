# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:17:38


from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot import Plugin,  UttObj, GBPluginMethods
from gb_hilab_suite.src.core.conversation_model import ConversationModel

from gb_hilab_suite.src.configs import  load_internal_marker, load_label, PLUGIN_NAME
MARKER = load_internal_marker()
LABEL = load_label().TXT

class TextPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods):
        """
        Prints the entire tree in a user-specified format
        """
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]

        varDict = {
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAPS: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER,
            MARKER.PAUSES: LABEL.PAUSE,
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        path = "{}/conversation.txt".format(methods.output_path)

        utterances = newUttMap

        with io.open(path, "w", encoding='utf-8') as outfile:
            for i, (id, nodeList) in enumerate(utterances.items()):
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

