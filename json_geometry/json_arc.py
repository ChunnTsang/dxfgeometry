# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from json_geometry.json_cad_element import JsonCADElement
from geometry.arc import Arc


class JsonArc(JsonCADElement):
    x: float
    y: float
    start_angle: float
    end_angle: float
    radius: float

    def __init__(self, arc: Arc):
        super(JsonArc, self).__init__(arc.get_layer_name(), "ARC")
        self.x = arc.get_x()
        self.y = arc.get_y()
        self.start_angle = arc.get_start_angle()
        self.end_angle = arc.get_end_angle()
        self.radius = arc.get_radius()


def json_arc_to_arc(json_arc):
    return Arc(json_arc["x"], json_arc["y"], json_arc["start_angle"], json_arc["end_angle"], json_arc["radius"],
               json_arc["layer_name"])
