#!/usr/bin/python
# -*- coding:utf-8 -*-

from .CounterIndexer import CounterIndexer
from .  import SignalDrop
from .  import Utils


class CounterClockSourceIndexer(CounterIndexer):
    def __init__(self, nativeIndexer):
        super(CounterClockSourceIndexer, self).__init__(nativeIndexer, SignalDrop, Utils.toSignalDrop)
