# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:20:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 15:27:33


from core.pipeline import Component, ComponentState
from services.baseObjects.payload import Payload


class TranscribeComponent(Component):

    def __init__(self,*args, **kwargs):
        pass

    def __repr__(self):
        raise NotImplementedError()

    def __call__(self, payload : Payload) -> ComponentState:
        """Get a source and the associated settings objects and transcribe"""
        raise NotImplementedError()



