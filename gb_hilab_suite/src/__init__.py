# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 11:15:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 11:42:48

import json
from typing import List
import os


from gb_hilab_suite.src.core import get_dependencies as core_dependencies
from gb_hilab_suite.src.analysis import get_dependencies as analysis_dependencies
from gb_hilab_suite.src.format import get_dependencies as format_dependencies


def generate_dependencies() -> List:
    dependencies = []
    dependencies.extend(core_dependencies())
    dependencies.extend(analysis_dependencies())
    dependencies.extend(format_dependencies())
    for item in dependencies:
        item["plugin_file_path"] = os.path.join("src",item["plugin_file_path"])
    return dependencies

def available_plugins() -> List[str]:
    dependencies = generate_dependencies()
    return [item["plugin_name"] for item in dependencies ]

def generate_config():
    with open("config.json","w") as f:
        json.dump({"plugin_configs" : generate_dependencies()},f)





