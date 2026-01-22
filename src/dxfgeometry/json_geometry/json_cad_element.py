# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.json_geometry.json_base_class import Jsonable


class JsonCADElement(Jsonable):
    layer_name: str
    type: str

    def __init__(self, layer_name: str, type: str):
        self.layer_name = layer_name
        self.type = type
