# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 11:03:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:30:28
import logging
from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
import os 
from gailbot import Plugin, GBPluginMethods
from gb_hilab_suite.src.core.conversation_model import ConversationModel

from gb_hilab_suite.src.configs import (
    load_internal_marker, 
    load_label, 
    PLUGIN_NAME, 
    OUTPUT_FILE
)
from gb_hilab_suite.src.configs.xml import (
    XML, 
    ATT_NAME, 
    TAG, 
    ATT_VALUE,
    COMMENTS,
    UTT
)
MARKER = load_internal_marker()
LABEL = load_label().TXT
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
        logging.info("start generating native xml file")
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS:                 LABEL.GAPMARKER,
            MARKER.OVERLAPS:             LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START:  LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_END:    LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_END:   LABEL.OVERLAPMARKER
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
        head = etree.SubElement(root, TAG.HEAD)


        # setting meta data
        filenames = " ".join(methods.filenames)
        extra_meta = {XML.NAME: XML.CONV_META_NAME, XML.CONTENT: filenames.rstrip()}
        
        metas: List[Dict] = XML.META_DATAS  + [extra_meta]
        
        for meta in metas:
            for att, value in meta.items():
                meta_elem = etree.SubElement(head, XML.META)
                meta_elem.set(att, value)
        #retrieve list of files used for this conversation

        logging.debug("finish setting meta data for native xml")
        
        for _, (_, nodeList) in enumerate(utterances.items()):
            count += 1
            curr_utt = cm.getWordFromNode(nodeList)
            
            logging.debug(f"get the list of utterance {curr_utt}")
            
            #Create utterance elements
            m1 = etree.SubElement(root, XML.UTT)
            m1.set(ATT_NAME.START_TIME, str(curr_utt[0].startTime))
            m1.set(ATT_NAME.END_TIME, str(curr_utt[-1].endTime))

           
            if (curr_utt[0].sLabel != MARKER.GAPS and
                curr_utt[0].sLabel != MARKER.PAUSES):
                sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
            else:
                sLabel = curr_utt[0].sLabel
            
            m1.set(ATT_NAME.S_LABEL, str(sLabel))

            for word in curr_utt:
                b2 = etree.SubElement(m1, TAG.WORD)
                b2.set(ATT_NAME.START_TIME, str(word.startTime))
                b2.set(ATT_NAME.END_TIME, str(word.endTime))
                b2.text = word.text
            root.append(m1)
        tree = etree.ElementTree(root)
        logging.debug("finish building xml native tree")
        path = os.path.join(methods.output_path, OUTPUT_FILE.NATIVE_XML)
        utterances = cm.getUttMap(False)
        
        with open (path, "wb") as files :
            tree.write(files)
        logging.debug("finish wrting xml_native.xml")


    def xml_talkbank(
        self,
        dependency_outputs: Dict[str, Any],
        methods: GBPluginMethods
    ):
        
        logging.info("start writing talkbank xml")
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.PAUSES:               MARKER.PAUSES,
            MARKER.GAPS:                 LABEL.GAPMARKER,
            MARKER.OVERLAPS:             LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START:  LABEL.OVERLAPMARKER_CURR_START,
            MARKER.OVERLAP_FIRST_END:    LABEL.OVERLAPMARKER_CURR_END,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER_NEXT_START,
            MARKER.OVERLAP_SECOND_END:   LABEL.OVERLAPMARKER_NEXT_END,
            MARKER.FASTSPEECH_START:     MARKER.FASTSPEECH_START,
            MARKER.FASTSPEECH_END:       MARKER.FASTSPEECH_END,
            MARKER.SLOWSPEECH_START:     MARKER.SLOWSPEECH_START,
            MARKER.SLOWSPEECH_END:       MARKER.SLOWSPEECH_END
        }
        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)


        #Root element is the CHAT tag
        root = etree.Element(ATT_NAME.CHAT)
        root.set(ATT_NAME.LINK, XML.TALK_BANK_LINK)
        
        root.set(ATT_NAME.CORP, ATT_VALUE.TIMMY)
        root.set(ATT_NAME.VSN,  ATT_VALUE.VERSION)
        root.set(ATT_NAME.LANG, ATT_VALUE.LANG)
        root.set(ATT_NAME.DATE, ATT_VALUE.YEAR)

        # populate Participants tag
        speakerMap = cm.getSpeakerMap(True)
        Participants = etree.SubElement(root, ATT_NAME.PARTS)
        
        comment = etree.SubElement(root, COMMENTS.COMMENT)
        comment.set(ATT_NAME.TYPE, COMMENTS.LOCATION)
        comment.text = COMMENTS.HILAB
        
        for speaker in speakerMap.keys():
            Participants.append(etree.Element(TAG.PARTICIPANT, id=str(LABEL.SPEAKERLABEL + speaker), role="Unidentified"))
            
        # populate the u tag
        count = 0
        utterances = newUttMap
        
        for _, (_, nodeList) in enumerate(utterances.items()):
            count += 1
            curr_utt = cm.getWordFromNode(nodeList)
            # Create utterance elements
            if curr_utt[0].sLabel == MARKER.NO_SPEAKER:
                logging.debug("skip with no speaker detected")
                continue

            
            # outer level utterance 
            utterance = etree.SubElement(root, TAG.UTT)
            utterance.set(UTT.WHO, str(LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)))
            utterance.set(UTT.ID, UTT.U + str(count))

            # traverse utt using index i
            i = 0

            # within tag
            # populate "w" tag
            while i < (len(curr_utt)):

                word = curr_utt[i]
                # utterance separater
                if MARKER.DELIM_MARKER1 in word.text or (MARKER.DELIM_MARKER2 in word.text and MARKER.PAUSES not in word.text):
                    i += 1
                    logging.info("skip with % . detected")
                    continue
                currText = word.text.split(MARKER.KEYVALUE_SEP)[0]

                # set keeping track of starting of nested markers in nested markers

                # if the word is a marker, use their own tag
                if currText in varDict.values():
                    for key, value in varDict.items():
                        if currText == value:
                            logging.debug(f"detect key marker {currText}")
                            # if the start of an overlap is detected, create g-tag to nest other tags
                            if key == MARKER.OVERLAP_FIRST_START or key == MARKER.OVERLAP_SECOND_START:
                                logging.debug(f"insert overlap  start tag")
                                # add overlap tag
                                overlap = etree.SubElement(utterance, TAG.OVERLAP_SUB)
                                exit = False # used to break out of the outter loop
                               
                                while i < (len(curr_utt)):
                                    word = curr_utt[i]
                                    currText = word.text.split(MARKER.KEYVALUE_SEP)[0]
                                    
                                    # add overlap tag within utterance list 
                                    if currText in varDict.values():
                                        for key, value in varDict.items():
                                            if currText == value:
                                                if  key == MARKER.OVERLAP_FIRST_END:
                                                    logging.debug("insert first overlap end tag")
                                                    overlap.append(etree.Element(TAG.OVERLAP, type=TAG.OVERLAP_PRE))
                                                    exit = True
                                                    break
                                                elif key == MARKER.OVERLAP_SECOND_END:
                                                    logging.debug("insert second overlap end tag")
                                                    overlap.append(etree.Element(TAG.OVERLAP, type=TAG.OVERLAP_POST))
                                                    exit = True
                                                    break
                                    # add word "w" tag 
                                    elif exit == False:
                                        if MARKER.DELIM_MARKER1 in word.text or MARKER.DELIM_MARKER2 in word.text:
                                            word.text = word.text.replace(MARKER.DELIM_MARKER1, '')
                                            word.text = word.text.replace(MARKER.DELIM_MARKER2, '')
                                            i += 1
                                        newelem = etree.SubElement(overlap, TAG.WORD_SUB)
                                        newelem.text = word.text
                                    else:
                                        i -= 1
                                        break
                                    i += 1

                                # when overlap starts but does not finish HACK
                                if exit == False:
                                    overlap.append(etree.Element(TAG.OVERLAP, type=TAG.OVERLAP_POST))

                            # if a pause tag is detected
                            # add pauses tag 
                            elif key == MARKER.PAUSES:
                                # print("pauses")
                                logging.debug(f"insert pauses with pause length {tempArr[1]}")
                                tempArr = word.text.split(MARKER.KEYVALUE_SEP)
                                pause = etree.Element(TAG.PAUSES)
                                pause.set(ATT_NAME.LENGTH, tempArr[1])
                                pause.set(ATT_NAME.SYMBOL_LENTH, ATT_VALUE.SIMPLE)
                                utterance.append(pause)
                                
                            elif key == MARKER.SLOWSPEECH_START or key == MARKER.FASTSPEECH_START:
                                currWord = etree.SubElement(utterance, TAG.WORD_SUB)
                                speech = etree.SubElement(currWord, TAG.DELIM)
                                speech.set(ATT_NAME.TYPE, ATT_VALUE.BEGIN)
                                if key == MARKER.SLOWSPEECH_START:
                                    logging.debug(f"insert slow speech tag")
                                    speech.set(XML.LABEL, XML.SLOWER)
                                    i += 1
                                else:
                                    logging.debug(f"insert fast speech tag")
                                    speech.set(XML.LABEL, XML.FASTER)
                                    i += 1

                                # trying to fix empty syllRate surrounding tags
                                cumCurrText = XML.EMPTY
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
                                                    speechEnd = etree.SubElement(currWord, TAG.DELIM)
                                                    speechEnd.set(ATT_NAME.TYPE, ATT_VALUE.END)
                                                    speechEnd.set(XML.LABEL, XML.SLOWER)
                                                    exit = True
                                                    break
                                                elif key == MARKER.FASTSPEECH_END:
                                                    #put text here
                                                    speech.tail = cumCurrText
                                                    speechEnd = etree.SubElement(currWord, TAG.DELIM)
                                                    speechEnd.set(ATT_NAME.TYPE, ATT_VALUE.END)
                                                    speechEnd.set(XML.LABEL, XML.FASTER)
                                                    exit = True
                                                    break
                                    elif exit == False:
                                        if MARKER.DELIM_MARKER1 in currText or MARKER.DELIM_MARKER2 in currText:
                                            i += 1
                                            continue
                                        if cumCurrText == XML.EMPTY:
                                            cumCurrText = ""
                                        cumCurrText = str(cumCurrText) + str(currText)
                                        cumCurrText = cumCurrText + " "
                                    else:
                                        i -= 1
                                        break
                                    i += 1
                else:
                    # the rests are words
                    if MARKER.DELIM_MARKER1 in word.text or MARKER.DELIM_MARKER2 in word.text:
                        i += 1
                        continue
                    newelem = etree.SubElement(utterance, TAG.WORD_SUB)
                    newelem.text = word.text
                i += 1

            newelem = etree.SubElement(utterance, TAG.TERM_SUB, type = TAG.TERM_SUB_TYPE)
            media = etree.SubElement(utterance, TAG.MEDIA)
            media.set(ATT_NAME.START,str(curr_utt[0].startTime))
            media.set(ATT_NAME.END, str(curr_utt[-1].endTime))
            media.set(ATT_NAME.TIME_UNIT, ATT_VALUE.TIME_UNIT)
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        tree = etree.ElementTree(root)
        path = os.path.join(methods.output_path, OUTPUT_FILE.TB_XML)
        with open (path, "wb") as files :
            tree.write(files)

