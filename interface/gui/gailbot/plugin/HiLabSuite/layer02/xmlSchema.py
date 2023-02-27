# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-12 13:14:56
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 13:35:00

# Code could be cleaner, in the process of getting things to work

# Standard imports
from operator import contains
from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt
from markerdef import *

# import xml.etree.ElementTree as etree
from lxml import etree

class xmlSchema(GBPlugin):
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
                                    "talkBankXML")

            with open (path, "wb") as files :
                tree.write(files)

            self.successful = True
            return

        except Exception as E:
            print("exception in xmlSchema")
            print(E)
            self.successful = False