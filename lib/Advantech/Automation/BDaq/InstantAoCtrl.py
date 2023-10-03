#!/usr/bin/python
# -*- coding:utf-8 -*-

from ctypes import *

from .  import Scenario, ErrorCode
from .BDaqApi import TInstantAoCtrl
from .AoCtrlBase import AoCtrlBase


class InstantAoCtrl(AoCtrlBase):
    def __init__(self, devInfo = None):
        super(InstantAoCtrl, self).__init__(Scenario.SceInstantAo, devInfo)

    def writeAny(self, chStart, chCount, dataRaw, dataScaled):
        doubleArray = (c_double * chCount)()
        for i in range(chCount):
            doubleArray[i] = dataScaled[i]

        return ErrorCode.lookup(TInstantAoCtrl.writeAny(self._obj, chStart, chCount, dataRaw, doubleArray))

