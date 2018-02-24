#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: 
# @date: '14-4-11'


import threading


class EntityBuffer(object):
    def __init__(self, size=10):
        self._size = size
        self._entity_list = []
        self._lock = threading.RLock()

    def add_entities(self, entities):
        self._entity_list += entities

    def add_entity(self, entity):
        self._entity_list.append(entity)

    def is_full(self):
        return len(self._entity_list) >= self._size

    def get_all_entities(self):
        return self._entity_list

    def empty(self):
        self._entity_list = []

    def pop_all(self):
        self._lock.acquire()
        size = len(self._entity_list)
        entities = self._entity_list[:size]
        self._entity_list = self._entity_list[size:]
        self._lock.release()
        return entities


if __name__ == "__main__":
    pass
