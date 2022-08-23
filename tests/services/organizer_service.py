# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 11:39:42
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:41:18

import pytest
from gailbot.services.organizer_service import OrganizerService

def test_initialize():
    assert type(OrganizerService("./")) == OrganizerService