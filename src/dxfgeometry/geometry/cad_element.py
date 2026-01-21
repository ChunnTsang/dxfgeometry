# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""


class CADElement(object):
    _layer_name: str = None

    def __init__(self, layer_name: str) -> None:
        self._layer_name = layer_name

    def get_layer_name(self) -> str:
        return self._layer_name

    def set_layer_name(self, layer_name: str) -> None:
        self._layer_name = layer_name
