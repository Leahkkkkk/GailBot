# # -*- coding: utf-8 -*-
# # @Author: Muhammad Umair
# # @Date:   2023-01-15 12:02:59
# # @Last Modified by:   Muhammad Umair
# # @Last Modified time: 2023-01-15 13:32:42

# from gailbot.core.pipeline import (
#     Pipeline, Component, ComponentResult, ComponentState
# )
# from typing import Dict, List, Any

# class TestComponent(Component):


#     def __init__(self, name : str):
#         self.name = str(name)

#     def __repr__(self):
#         return self.name

#     def __call__(
#         self,
#         dependency_outputs : Dict[str, Any]
#     ) -> ComponentState:

#         """Get a source and the associated settings objects and transcribe"""
#         print(f"Running component {self.name}")
#         print(f"Dependency outputs {dependency_outputs}")
#         return ComponentResult(
#             state=ComponentState.SUCCESS,
#             result=self.name,
#             runtime=0
#         )


# def test_pipeline():
#     # 2 and 4 should run together
#     components = {
#         str(i) : TestComponent(i) for i in range(1,6)
#     }
#     pipeline = Pipeline(
#         dependency_map={
#             "1" : [],
#             "2" : ["1"],
#             "3" : ["2"],
#             "4" : ["1"],
#             "5" : ["1", "3"]
#         },
#         components=components
#     )
#     print(pipeline.component_children("1"))
#     print(pipeline)
#     res = pipeline({})
#     print(res)