# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:25:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 15:47:14


from core.pipeline import Component, ComponentState
from plugins import Plugin, PluginManager, Suite
from services.baseObjects.payload import Payload

class FormatComponent(Component):

    def __init__(self,*args, **kwargs):
        pass

    def __repr__(self):
        raise NotImplementedError()

    def __call__(self, payload : Payload) -> ComponentState:
        """Get a source and the associated settings objects and transcribe"""
        raise NotImplementedError()


