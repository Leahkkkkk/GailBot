# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-03 17:30:43
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 13:38:17
import io
from typing import Dict, Any, List, Tuple
import xml.etree.ElementTree as ET
from gailbot.plugins import GBPlugin, PluginMethodSuite

class XMLtoCSV(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite):
        """
        Converts between XML and CSV documents
        Credit: https://stackoverflow.com/questions/29596584/getting-a-list-of-xml-tags-in-file-using-xml-etree-elementtree
        """
        tree = ET.parse('test.xml')
        root = tree.getroot()
        # for child in root:
        #     print(child.tag)
        elemList = []

        # #retrieve all tags present in the XML document
        # for elem in tree.iter():
        #     print("tags")
        #     elemList.append(elem.tag)

        #remove duplicities by converting to set and back to list
        elemList = list(set(elemList))
        # for element in elemList:
        #     print(element)
        #for utterance in root:
            #find text associated with each presentt ag
            #append to CSV row


        #for utterance in root:
        self.successful = True
        return
