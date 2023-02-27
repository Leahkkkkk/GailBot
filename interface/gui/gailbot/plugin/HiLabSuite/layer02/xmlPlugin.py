# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 13:31:24
# Standard imports

from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt
from markerdef import *

# import xml.etree.ElementTree as etree
from lxml import etree

class xmlPlugin(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite):
        """
        Prints the entire tree in a user-specified format
        """

        try:
            cm = dependency_outputs["convModelPlugin"]
            varDict = {
                GAPS: XML_GAPMARKER,
                OVERLAPS: XML_OVERLAPMARKER,
                MARKER1: XML_OVERLAPMARKER,
                MARKER2: XML_OVERLAPMARKER,
                MARKER3: XML_OVERLAPMARKER,
                MARKER4: XML_OVERLAPMARKER
            }
            root = cm.getTree(False)
            newUttMap = dict()
            myFunction = cm.outer_buildUttMapWithChange(0)
            myFunction(root, newUttMap, varDict)

            count = 100
            #data = ["this is a xml file"]
            # path = "{}/{}.txt".format(plugin_input.get_result_directory_path(),
            #                         str(count))

            utterances = newUttMap

            #Root element is the conversation
            count = 0

            #Add metadata tags
            root = etree.Element("Conversation")
            head = etree.SubElement(root, "head")
            metadata1 = etree.SubElement(head, "meta")
            metadata1.set('name', '@Languages')
            metadata1.set('content', 'eng')
            metadata2 = etree.SubElement(head, "meta")
            metadata2.set('name', '@Options')
            metadata2.set('content', 'CA')
            metadata3 = etree.SubElement(head, "meta")
            metadata3.set('name', '@Media')
            metadata3.set('content', 'test, audio')
            metadata4 = etree.SubElement(head, "meta")
            metadata4.set('name', '@Comment')
            metadata4.set('content', 'absolute')
            metadata5 = etree.SubElement(head, "meta")
            metadata5.set('name', '@Transcriber')
            metadata5.set('content', 'Gailbot 0.3.0')
            metadata6 = etree.SubElement(head, "meta")
            metadata6.set('name', '@Location')
            metadata6.set('content', 'Hilab')
            metadata7 = etree.SubElement(head, "meta")
            metadata7.set('name', '@Room')
            metadata7.set('content', 'big')
            metadata8 = etree.SubElement(head, "meta")
            metadata8.set('name', '@Situation')
            metadata8.set('content', 'test')
            metadata9 = etree.SubElement(head, "meta")
            metadata9.set('name', '@Conversation')
            #retrieve list of files used for this conversation
            filename = plugin_input.get_audio_paths();
            filenames = ""
            for key, pathname in filename.items():
                filename = pathname.rsplit('/', 1)[-1]
                filenames = filenames + filename + " "
            metadata9.set('content', filenames.rstrip())

            for _, (_, nodeList) in enumerate(utterances.items()):
                count += 1

                curr_utt = cm.getWordFromNode(nodeList)

                #Create utterance elements
                m1 = etree.SubElement(root, "Utterance")
                m1.set('startTime', str(curr_utt[0].startTime))
                m1.set('endtime', str(curr_utt[-1].endTime))

                sLabel = ""
                if (curr_utt[0].sLabel != "gaps" and
                    curr_utt[0].sLabel != "pauses"):
                    sLabel = XML_SPEAKERLABEL + str(curr_utt[0].sLabel)
                m1.set('speakerlabel', str(curr_utt[0].sLabel))

                for word in curr_utt:
                    b2 = etree.SubElement(m1, "Word")
                    b2.set('startTime', str(word.startTime))
                    b2.set('endTime', str(word.endTime))
                    b2.text = word.text

                root.append(m1)

            tree = etree.ElementTree(root)

            path = "{}/{}.xml".format(plugin_input.get_result_directory_path(),
                                    str(count))

            utterances = cm.getUttMap(False)
            with open (path, "wb") as files :
                tree.write(files)

            self.successful = True
            return

        except Exception as E:
            print("exception in xmlPlugin")
            print(E)
            self.successful = False