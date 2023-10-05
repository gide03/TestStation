#!/usr/bin/python
# -*- coding:utf-8 -*-

from .CounterIndexer import CounterIndexer
from .  import SignalDrop
from .  import Utils


class CounterGateSourceIndexer(CounterIndexer):
    def __init__(self, nativeIndexer):
        super(CounterGateSourceIndexer, self).__init__(nativeIndexer, SignalDrop, Utils.toSignalDrop)
