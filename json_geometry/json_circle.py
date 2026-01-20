# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from json_geometry.json_cad_element import JsonCADElement
from geometry.circle import Circle


class JsonCircle(JsonCADElement):
    x: float
    y: float
    radius: float

    def __init__(self, circle: Circle):
        super(JsonCircle, self).__init__(circle.get_layer_name(), "Circle")
        self.x = circle.get_x()
        self.y = circle.get_y()
        self.radius = circle.get_radius()
        self.electric_info = {}

    def __setitem__(self, key, value):
        self.electric_info[key] = value


def json_circle_to_circle(json_circle: dict) -> Circle:
    return Circle(json_circle['x'], json_circle['y'], json_circle['radius'], json_circle['layer_name'])
