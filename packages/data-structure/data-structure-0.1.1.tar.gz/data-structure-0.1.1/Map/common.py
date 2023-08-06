from abc import ABC
from collections import MutableMapping
import random


class MapBase(MutableMapping, ABC):
    class _item:
        __slots__ = "key", "value"

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return not (self == other)

        def __cmp__(self, other):
            return self.key < other.key


class UnsortedTableMap(MapBase, ABC):
    def __init__(self):
        self.table = []

    def __getitem__(self, k):
        for item in self.table:
            if k == item.key:
                return item.value
        raise KeyError("Key error: " + repr(k))

    def __setitem__(self, k, v):
        for item in self.table:
            if k == item.key:
                item.value = v
                return  # quit
        self.table.append(self._item(k, v))

    def __delitem__(self, k):
        for j in range(len(self.table)):
            if k == self.table[j].key:
                self.table.pop(j)
                return
        raise KeyError("Key error: " + repr(k))

    def __len__(self):
        return len(self.table)

    def __iter__(self):
        for item in self.table:
            yield item.key


class HashMapBase(MapBase):
    def __init__(self, cap=11, p=109345121):
        self.table = cap * [None]
        self.n = 0
        self.prime = p
        self.scale = 1 + random.randrange(p-1)
        self.shift = random.randrange(p)

    def _hash_function(self, k):
        return (hash(k) * self.scale + self.shift) % self.prime % len(self.table)

    def __len__(self):
        return self.n

    def __getitem__(self, k):
        j = self._hash_function(k)


