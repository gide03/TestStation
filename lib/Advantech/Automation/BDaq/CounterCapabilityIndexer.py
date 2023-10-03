#!/usr/bin/python
# -*- coding:utf-8 -*-

from .CounterIndexer import CounterIndexer
from .  import CounterCapability
from .  import Utils


class CounterCapabilityIndexer(CounterIndexer):
    def __init__(self, nativeIndexer):
        super(CounterCapabilityIndexer, self).__init__(nativeIndexer, CounterCapability, Utils.toCounterCapability)
