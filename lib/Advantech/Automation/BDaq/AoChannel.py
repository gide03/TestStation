#!/usr/bin/python
# -*- coding:utf-8 -*-


from .AnalogOutputChannel import AnalogOutputChannel


class AoChannel(AnalogOutputChannel):
    def __init__(self, nativeChannelObj):
        super(AoChannel, self).__init__(nativeChannelObj)
