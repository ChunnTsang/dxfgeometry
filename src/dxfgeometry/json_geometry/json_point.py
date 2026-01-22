# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.json_geometry.json_cad_element import JsonCADElement
from dxfgeometry.geometry.point import Point


class JsonPoint(JsonCADElement):
    x: float
    y: float
    
    def __init__(self, point: Point):
        super(JsonPoint, self).__init__(point.get_layer_name(), "Point")
        self.x = point.get_x()
        self.y = point.get_y()


def json_point_to_point(json_point: dict) -> Point:
    return Point(json_point['x'], json_point['y'], json_point['layer_name'])
