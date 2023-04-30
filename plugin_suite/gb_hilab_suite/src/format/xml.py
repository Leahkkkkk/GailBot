# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 11:03:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:30:28
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot import Plugin, GBPluginMethods
from gb_hilab_suite.src.core.conversation_model import ConversationModel

from gb_hilab_suite.src.configs import  load_internal_marker, load_label, PLUGIN_NAME
MARKER = load_internal_marker()
LABEL = load_label().TXT
from lxml import etree


@dataclass 
class XML:
    LABEL = "label"
    S_LABEL = "speakerlabel"
    UTT = "Utterance"
    START = "startTime"
    END = "endTime"
    NAME = "name"
    CONTENT = "content"
    META = "meta"
    GB_VERSION = 'Gailbot 0.3.0'
    TEST = "test"
    CONV = "Conversation"
    HIL = "HiLab"
    LENGTH = "length"
    DELIM = "ca-delimiter"
    VERSION_NUM = "ca-delimiter"
    TALK_BANK_LINK = "http://www.talkbank.org/ns/talkbank"
@dataclass
class TAGS:
    PARTS = "Participants"
    CHAT = "CHAT"
    VSN = "Version"
    LANG = "Lang"
    CORP = "Corpus"
    DATE = "Date"
    W = "w"
class XMLPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods):
        """
        Prints the entire tree in a user-specified format
        """
        self.xml_native(dependency_outputs, methods)
        self.xml_talkbank(dependency_outputs, methods)
        self.successful = True

    def xml_native(
        self,
        dependency_outputs: Dict[str, Any],
        methods: GBPluginMethods
    ):
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAPS: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER
        }
        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        count = 100
        utterances = newUttMap
        #Root element is the conversation
        count = 0

        root = etree.Element(XML.CONV)
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
        files = methods.filenames
        filenames = ""
        
        # for name in files:
        #     filenames = filenames + name + " "
        filenames = " ".join(methods.filenames)
        metadata9.set(XML.CONTENT, filenames.rstrip())

        for _, (_, nodeList) in enumerate(utterances.items()):
            count += 1

            curr_utt = cm.getWordFromNode(nodeList)

            #Create utterance elements
            m1 = etree.SubElement(root, XML.UTT)
            m1.set(XML.START, str(curr_utt[0].startTime))
            m1.set(XML.END, str(curr_utt[-1].endTime))

            # TODO: check sLabel
            if (curr_utt[0].sLabel != MARKER.GAPS and
                curr_utt[0].sLabel != MARKER.PAUSES):
                sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
            else:
                sLabel = curr_utt[0].sLabel
            
            m1.set('speakerlabel', str(sLabel))

            for word in curr_utt:
                b2 = etree.SubElement(m1, "Word")
                b2.set(XML.START, str(word.startTime))
                b2.set(XML.END, str(word.endTime))
                b2.text = word.text
            root.append(m1)

        tree = etree.ElementTree(root)

        path = "{}/native.xml".format(methods.output_path)

        utterances = cm.getUttMap(False)
        with open (path, "wb") as files :
            tree.write(files)

    def xml_talkbank(
        self,
        dependency_outputs: Dict[str, Any],
        methods: GBPluginMethods
    ):
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.PAUSES: MARKER.PAUSES,
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAPS: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER_CURR_START,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER_CURR_END,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER_NEXT_START,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER_NEXT_END,
            MARKER.FASTSPEECH_START: MARKER.FASTSPEECH_START,
            MARKER.FASTSPEECH_END: MARKER.FASTSPEECH_END,
            MARKER.SLOWSPEECH_START: MARKER.SLOWSPEECH_START,
            MARKER.SLOWSPEECH_END: MARKER.SLOWSPEECH_END
        }
        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)


        #Root element is the CHAT tag
        root = etree.Element(TAGS.CHAT)
        root.set('xmlns', XML.TALK_BANK_LINK)
        
        root.set(TAGS.CORP, 'timmy')
        root.set(TAGS.VSN, '2.16.0')
        root.set(TAGS.LANG, 'eng')
        root.set(TAGS.DATE, '1996-02-29')

        # populate Participants tag
        speakerMap = cm.getSpeakerMap(True)
        Participants = etree.SubElement(root, TAGS.PARTS)
        comment = etree.SubElement(root, "comment")
        comment.set('type', 'Location')
        comment.text = "HI_LAB"
        for speaker in speakerMap.keys():
            Participants.append(etree.Element("participant", id=str(LABEL.SPEAKERLABEL + speaker), role="Unidentified"))
            
        # populate the u tag
        count = 0
        utterances = newUttMap
        
        for _, (_, nodeList) in enumerate(utterances.items()):
            count += 1

            curr_utt = cm.getWordFromNode(nodeList)

            # Create utterance elements
            if curr_utt[0].sLabel == "NONE":
                continue
            
            
            # outer level utterance 
            utterance = etree.SubElement(root, "u")
            utterance.set('who', str(LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)))
            utterance.set('uID', "u" + str(count))

            # traverse utt using index i
            i = 0

            # within tag
            # populate "w" tag
            while i < (len(curr_utt)):

                word = curr_utt[i]
                # utterance separater
                if '%' in word.text or ('.' in word.text and MARKER.PAUSES not in word.text):
                    i += 1
                    continue
                currText = word.text.split(MARKER.KEYVALUE_SEP)[0]

                # set keeping track of starting of nested markers in nested markers

                # if the word is a marker, use their own tag
                if currText in varDict.values():
                    for key, value in varDict.items():
                        if currText == value:
                            # if the start of an overlap is detected, create g-tag to nest other tags
                            if key == MARKER.OVERLAP_FIRST_START or key == MARKER.OVERLAP_SECOND_START:
                                # add overlap tag
                                overlap = etree.SubElement(utterance, "g")
                                exit = False # used to break out of the outter loop
                               
                                while i < (len(curr_utt)):
                                    word = curr_utt[i]
                                    currText = word.text.split(MARKER.KEYVALUE_SEP)[0]
                                    
                                    # add overlap tag within utterance list 
                                    if currText in varDict.values():
                                        for key, value in varDict.items():
                                            if currText == value:
                                                if  key == MARKER.OVERLAP_FIRST_END:
                                                    overlap.append(etree.Element("overlap", type="overlap precedes"))
                                                    exit = True
                                                    break
                                                elif key == MARKER.OVERLAP_SECOND_END:
                                                    overlap.append(etree.Element("overlap", type="overlap follows"))
                                                    exit = True
                                                    break
                                    # add word "w" tag 
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
                            # add pauses tag 
                            elif key == MARKER.PAUSES:
                                # print("pauses")
                                tempArr = word.text.split(MARKER.KEYVALUE_SEP)
                                pause = etree.Element("pause")
                                pause.set(XML.LENGTH, tempArr[1])
                                pause.set('symbolic-length', 'simple')
                                utterance.append(pause)
                            elif key == MARKER.SLOWSPEECH_START or key == MARKER.FASTSPEECH_START:
                                currWord = etree.SubElement(utterance, TAGS.W)
                                speech = etree.SubElement(currWord, XML.DELIM)
                                speech.set('type', "begin")
                                if key == MARKER.SLOWSPEECH_START:
                                    speech.set(XML.LABEL, "slower")
                                    i += 1
                                else:
                                    speech.set(XML.LABEL, "faster")
                                    i += 1

                                # trying to fix empty syllRate surrounding tags
                                cumCurrText = "EMPTY"
                                exit = False
                                
                                while i < (len(curr_utt)):
                                    word = curr_utt[i]
                                    currText = word.text.split(MARKER.KEYVALUE_SEP)[0]
                                    if currText in varDict.values() and exit == False:
                                        for key, value in varDict.items():
                                            if currText == value:
                                                # speech.tail = cumCurrText # TODO: verify if work
                                                if key == MARKER.SLOWSPEECH_END:
                                                    #put text here
                                                    speech.tail = cumCurrText
                                                    speechEnd = etree.SubElement(currWord, XML.DELIM)
                                                    speechEnd.set('type', "end")
                                                    speechEnd.set(XML.LABEL, "slower")
                                                    exit = True
                                                    break
                                                elif key == MARKER.FASTSPEECH_END:
                                                    #put text here
                                                    speech.tail = cumCurrText
                                                    speechEnd = etree.SubElement(currWord, XML.DELIM)
                                                    speechEnd.set('type', "end")
                                                    speechEnd.set(XML.LABEL, "faster")
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
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        tree = etree.ElementTree(root)

        path = "{}/{}.xml".format(methods.output_path, "talkbank")
        with open (path, "wb") as files :
            tree.write(files)

