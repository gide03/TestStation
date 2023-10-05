#!/usr/bin/python
# -*- coding:utf-8 -*-

from .AnalogInputChannel import AnalogInputChannel


class AiChannel(AnalogInputChannel):
    def __init__(self, nativeChannelObj):
        super(AiChannel, self).__init__(nativeChannelObj)
