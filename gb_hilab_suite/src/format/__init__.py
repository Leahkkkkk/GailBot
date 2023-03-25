# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:51:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:13:22



from typing import List, Dict

def get_dependencies() -> List[Dict]:
    return [
         {
            "plugin_name": "chat",
            "plugin_dependencies": ["conv_model","gaps", "pauses", "overlaps"],
            "plugin_file_path": "format/chat.py",
            "plugin_source_name": "chat",
            "plugin_class_name": "ChatPlugin"
        },
        {
            "plugin_name": "text",
            "plugin_dependencies": ["conv_model","gaps", "pauses", "overlaps"],
            "plugin_file_path": "format/text.py",
            "plugin_source_name": "text",
            "plugin_class_name": "TextPlugin"
        },
        {
            "plugin_name": "csv",
            "plugin_dependencies": ["conv_model","gaps", "pauses", "overlaps"],
            "plugin_file_path": "format/csv.py",
            "plugin_source_name": "csv",
            "plugin_class_name": "CSVPlugin"
        },
        {
            "plugin_name": "xml",
            "plugin_dependencies": ["conv_model","gaps", "pauses", "overlaps"],
            "plugin_file_path": "format/xml.py",
            "plugin_source_name": "xml",
            "plugin_class_name": "XMLPlugin"
        },
    ]