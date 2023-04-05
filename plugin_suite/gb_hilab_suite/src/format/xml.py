# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 11:03:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:30:28

from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot import Plugin, GBPluginMethods
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.config import MARKER, THRESHOLD, LABEL, PLUGIN_NAME, XML

from lxml import etree

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
            MARKER.GAPS: LABEL.XML_GAPMARKER,
            MARKER.OVERLAPS: LABEL.XML_OVERLAPMARKER,
            MARKER.MARKER1: LABEL.XML_OVERLAPMARKER,
            MARKER.MARKER2: LABEL.XML_OVERLAPMARKER,
            MARKER.MARKER3: LABEL.XML_OVERLAPMARKER,
            MARKER.MARKER4: LABEL.XML_OVERLAPMARKER
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
       
        metadata1 = etree.SubElement(head, XML.META)
        metadata1.set(XML.NAME, '@Languages')
        metadata1.set(XML.CONTENT, 'eng')
        
        metadata2 = etree.SubElement(head, XML.META)
        metadata2.set(XML.NAME, '@Options')
        metadata2.set(XML.CONTENT, 'CA')
        
        metadata3 = etree.SubElement(head, XML.META)
        metadata3.set(XML.NAME, '@Media')
        metadata3.set(XML.CONTENT, 'test, audio')
        
        metadata4 = etree.SubElement(head, XML.META)
        metadata4.set(XML.NAME, '@Comment')
        metadata4.set(XML.CONTENT, 'absolute')
        
        metadata5 = etree.SubElement(head, XML.META)
        metadata5.set(XML.NAME, '@Transcriber')
        metadata5.set(XML.CONTENT, XML.GB_VERSION)
        
        metadata6 = etree.SubElement(head, XML.META)
        metadata6.set(XML.NAME, '@Location')
        metadata6.set(XML.CONTENT, XML.HIL)
        
        metadata7 = etree.SubElement(head, XML.META)
        metadata7.set(XML.NAME, '@Room')
        metadata7.set(XML.CONTENT, 'big')
        
        metadata8 = etree.SubElement(head, XML.META)
        metadata8.set(XML.NAME, '@Situation')
        metadata8.set(XML.CONTENT, XML.TEST)
        
        metadata9 = etree.SubElement(head, XML.META)
        metadata9.set(XML.NAME, '@Conversation')
       
        #retrieve list of files used for this conversation
        files = methods.filenames
        filenames = ""
        
        for name in files:
            filenames = filenames + name + " "
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
                sLabel = LABEL.XML_SPEAKERLABEL + str(curr_utt[0].sLabel)
            else:
                sLabel = curr_utt[0].sLabel
            
            m1.set(XML.S_LABEL, str(sLabel))

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
            MARKER.GAPS: LABEL.XML_GAPMARKER,
            MARKER.OVERLAPS: LABEL.XML_OVERLAPMARKER,
            MARKER.MARKER1: LABEL.OVERLAPMARKER_CURR_START,
            MARKER.MARKER2: LABEL.OVERLAPMARKER_CURR_END,
            MARKER.MARKER3: LABEL.OVERLAPMARKER_NEXT_START,
            MARKER.MARKER4: LABEL.OVERLAPMARKER_NEXT_END,
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
        root = etree.Element("CHAT")
        root.set('xmlns', XML.TALKBANK_LINK)
        root.set('Corpus', 'timmy')
        root.set('Version', '2.16.0')
        root.set('Lang', 'eng')
        root.set('Date', '1996-02-29')

        # populate Participants tag
        speakerMap = cm.getSpeakerMap(True)
        Participants = etree.SubElement(root, "Participants")
        comment = etree.SubElement(root, "comment")
        comment.set('type', 'Location')
        comment.text = "HI_LAB"
        for speaker in speakerMap.keys():
            Participants.append(etree.Element("participant", id=str(LABEL.XML_SPEAKERLABEL + speaker), role="Unidentified"))
            
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
            utterance.set('who', str(LABEL.XML_SPEAKERLABEL + str(curr_utt[0].sLabel)))
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
                            if key == MARKER.MARKER1 or key == MARKER.MARKER3:
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
                                                if  key == MARKER.MARKER2:
                                                    overlap.append(etree.Element("overlap", type="overlap precedes"))
                                                    exit = True
                                                    break
                                                elif key == MARKER.MARKER4:
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
                                pause.set('length', tempArr[1])
                                pause.set('symbolic-length', 'simple')
                                utterance.append(pause)
                            elif key == MARKER.SLOWSPEECH_START or key == MARKER.FASTSPEECH_START:
                                currWord = etree.SubElement(utterance, "w")
                                speech = etree.SubElement(currWord, "ca-delimiter")
                                speech.set('type', "begin")
                                if key == MARKER.SLOWSPEECH_START:
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
                                    currText = word.text.split(MARKER.KEYVALUE_SEP)[0]
                                    if currText in varDict.values() and exit == False:
                                        for key, value in varDict.items():
                                            if currText == value:
                                                # speech.tail = cumCurrText # TODO: verify if work
                                                if key == MARKER.SLOWSPEECH_END:
                                                    #put text here
                                                    speech.tail = cumCurrText
                                                    speechEnd = etree.SubElement(currWord, "ca-delimiter")
                                                    speechEnd.set('type', "end")
                                                    speechEnd.set('label', "slower")
                                                    exit = True
                                                    break
                                                elif key == MARKER.FASTSPEECH_END:
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

