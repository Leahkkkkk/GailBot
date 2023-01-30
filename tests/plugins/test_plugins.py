# # -*- coding: utf-8 -*-
# # @Author: Muhammad Umair
# # @Date:   2023-01-15 13:37:25
# # @Last Modified by:   Muhammad Umair
# # @Last Modified time: 2023-01-16 13:11:27

# import sys
# import os

# from gailbot.plugins import (
#     PluginManager,
#     PluginSuite,
#     Plugin,
#     Methods
# )

# from typing import Dict, List, Any


# PLUGIN_MANAGER_WS = "./plugins_ws"
# SUITE_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot/plugins/hilabSuite"

# class GBPluginMethods(Methods):

#     def __init__(self):
#         pass

#     @property
#     def audios(self) -> Dict[str,str]:
#         raise NotImplementedError()

#     @property
#     def utterances(self) -> Dict[str,Dict]:
#         raise NotImplementedError()

#     @property
#     def save_dir(self) -> str:
#         raise NotImplementedError()

# def test_manager():
#     manager = PluginManager(PLUGIN_MANAGER_WS)
#     print(manager)
#     manager.register_suite(SUITE_PATH)
#     print(manager.suite_names())
#     suite = manager.get_suite("HiLab")
#     print(suite)
#     suite(
#         base_input=None,
#         methods = GBPluginMethods()
#     )