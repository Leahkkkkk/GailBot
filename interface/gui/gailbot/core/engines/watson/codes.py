# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-16 11:07:12
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:07:46

from enum import IntEnum

class WatsonReturnCodes(IntEnum):
    """
    Return codes from Watson.
    """
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    UNSUPPORTED = 415
