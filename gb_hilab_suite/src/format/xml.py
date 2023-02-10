# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 11:03:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:30:28

from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt 

from gb_hilab_suite.src.gb_hilab_suite import *

# import xml.etree.ElementTree as etree
from lxml import etree

class XMLPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Methods):
        """
        Prints the entire tree in a user-specified format
        """
        self.xml_native(dependency_outputs, plugin_input)
        self.xml_talkbank(dependency_outputs, plugin_input)
        self.successful = True

    def xml_native(
        self,
        dependency_outputs: Dict[str, Any],
        plugin_input: Methods
    ):
        cm = dependency_outputs["conv_model"]
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

        path = "{}/native.xml".format(plugin_input.get_result_directory_path())

        utterances = cm.getUttMap(False)
        with open (path, "wb") as files :
            tree.write(files)

    def xml_talkbank(
        self,
        dependency_outputs: Dict[str, Any],
        plugin_input: Methods
    ):
        cm = dependency_outputs["conv_model"]
        varDict = {
            PAUSES: PAUSES,
            GAPS: XML_GAPMARKER,
            OVERLAPS: XML_OVERLAPMARKER,
            MARKER1: OVERLAPMARKER_CURR_START,
            MARKER2: OVERLAPMARKER_CURR_END,
            MARKER3: OVERLAPMARKER_NEXT_START,
            MARKER4: OVERLAPMARKER_NEXT_END,
            FASTSPEECH_START: FASTSPEECH_START,
            FASTSPEECH_END: FASTSPEECH_END,
            SLOWSPEECH_START: SLOWSPEECH_START,
            SLOWSPEECH_END: SLOWSPEECH_END
        }
        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        utterances = newUttMap

        #Root element is the CHAT tag
        root = etree.Element("CHAT")
        root.set('xmlns', 'http://www.talkbank.org/ns/talkbank')
        root.set('Corpus', 'timmy')
        root.set('Version', '2.16.0')
        root.set('Lang', 'eng')
        root.set('Date', '1996-02-29')

        speakerMap = cm.getSpeakerMap(True)
        Participants = etree.SubElement(root, "Participants")
        comment = etree.SubElement(root, "comment")
        comment.set('type', 'Location')
        comment.text = "HI_LAB"

        for speaker in speakerMap.keys():
            Participants.append(etree.Element("participant", id=str(XML_SPEAKERLABEL + speaker), role="Unidentified"))

        count = 0

        for _, (_, nodeList) in enumerate(utterances.items()):
            count += 1

            curr_utt = cm.getWordFromNode(nodeList)

            # Create utterance elements
            if curr_utt[0].sLabel == "NONE":
                continue

            utterance = etree.SubElement(root, "u")
            utterance.set('who', str(XML_SPEAKERLABEL + str(curr_utt[0].sLabel)))
            utterance.set('uID', "u" + str(count))

            # traverse utt using index i
            i = 0
            while i < (len(curr_utt)):

                word = curr_utt[i]
                # print(word.text)

                if '%' in word.text or ('.' in word.text and PAUSES not in word.text):
                    i += 1
                    continue
                currText = word.text.split(KEYVALUE_SEP)[0]

                # set keeping track of startings of nested markers in nested markers

                # if the word is a marker, use their own tag
                if currText in varDict.values():
                    for key, value in varDict.items():

                        if currText == value:

                            # if the start of an overlap is detected, create g-tag to nest other tags
                            if key == MARKER1 or key == MARKER3:

                                overlap = etree.SubElement(utterance, "g")
                                exit = False # used to break out of the outter loop
                                while i < (len(curr_utt)):
                                    word = curr_utt[i]
                                    currText = word.text.split(KEYVALUE_SEP)[0]
                                    if currText in varDict.values():
                                        for key, value in varDict.items():
                                            if currText == value:
                                                if  key == MARKER2:
                                                    overlap.append(etree.Element("overlap", type="overlap precedes"))
                                                    exit = True
                                                    break
                                                elif key == MARKER4:
                                                    overlap.append(etree.Element("overlap", type="overlap follows"))
                                                    exit = True
                                                    break

                                    elif exit == False:
                                        if '%' in word.text or '.' in word.text:
                                            word.text = word.text.replace('%', '')
                                            word.text = word.text.replace('.', '')
                                            i += 1
                                        newelem = etree.SubElement(overlap, "w")
                                        newelem.text = word.text
                                    else:
                                        i -= 1
                                        break
                                    i += 1

                                # when overlap starts but does not finish HACK
                                if exit == False:
                                    overlap.append(etree.Element("overlap", type="overlap follows"))

                            # if a pause tag is detected
                            elif key == PAUSES:
                                # print("pauses")
                                tempArr = word.text.split(KEYVALUE_SEP)
                                pause = etree.Element("pause")
                                pause.set('length', tempArr[1])
                                pause.set('symbolic-length', 'simple')
                                utterance.append(pause)

                            # TODO: ADD OTHER MARKER AS NEW TAGS
                            elif key == SLOWSPEECH_START or key == FASTSPEECH_START:

                                currWord = etree.SubElement(utterance, "w")
                                speech = etree.SubElement(currWord, "ca-delimiter")
                                speech.set('type', "begin")
                                if key == SLOWSPEECH_START:
                                    speech.set('label', "slower")
                                    i += 1
                                else:
                                    speech.set('label', "faster")
                                    i += 1

                                # trying to fix empty syllRate surrounding tags
                                cumCurrText = "EMPTY"
                                exit = False
                                while i < (len(curr_utt)):
                                    word = curr_utt[i]
                                    currText = word.text.split(KEYVALUE_SEP)[0]
                                    if currText in varDict.values() and exit == False:
                                        for key, value in varDict.items():
                                            if currText == value:
                                                # speech.tail = cumCurrText # TODO: verify if work
                                                if key == SLOWSPEECH_END:
                                                    #put text here
                                                    speech.tail = cumCurrText
                                                    speechEnd = etree.SubElement(currWord, "ca-delimiter")
                                                    speechEnd.set('type', "end")
                                                    speechEnd.set('label', "slower")
                                                    exit = True
                                                    break
                                                elif key == FASTSPEECH_END:
                                                    #put text here
                                                    speech.tail = cumCurrText
                                                    speechEnd = etree.SubElement(currWord, "ca-delimiter")
                                                    speechEnd.set('type', "end")
                                                    speechEnd.set('label', "faster")
                                                    exit = True
                                                    break
                                    elif exit == False:
                                        if '%' in currText or '.' in currText:
                                            i += 1
                                            continue
                                        if cumCurrText == "EMPTY":
                                            cumCurrText = ""
                                        cumCurrText = str(cumCurrText) + str(currText)
                                        cumCurrText = cumCurrText + " "
                                    else:
                                        i -= 1
                                        break
                                    i += 1

                                # # when slow/fast speech starts but does not finish HACK
                                # if exit == False:
                                #     currWord.remove(speech)


                else:
                    # the rests are words
                    if '%' in word.text or '.' in word.text:
                        i += 1
                        continue
                    newelem = etree.SubElement(utterance, "w")
                    newelem.text = word.text
                i += 1

            newelem = etree.SubElement(utterance, "t", type = "p")
            media = etree.SubElement(utterance, "media")
            media.set('start', str(curr_utt[0].startTime))
            media.set('end', str(curr_utt[-1].endTime))
            media.set('unit', 's')

            #root.append(utterance)

        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        tree = etree.ElementTree(root)

        path = "{}/{}.xml".format(plugin_input.get_result_directory_path(),
                                "talkbank")
        with open (path, "wb") as files :
            tree.write(files)

