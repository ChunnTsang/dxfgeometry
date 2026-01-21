# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.json_geometry.json_cad_element import JsonCADElement
from src.dxfgeometry.geometry.hatch import Hatch


class JsonHatch(JsonCADElement):
    points: list[float]
    pattern: str

    def __init__(self, hatch: Hatch):
        super(JsonHatch, self).__init__(hatch.get_layer_name(), "HATCH")
        self.points = hatch.get_coord_list_flatten()
        self.pattern = hatch.get_hatch_pattern_name()


def json_hatch_to_hatch(json_hatch: dict, existing_angles: list[float]) -> Hatch:
    point_list: list[list[float]] = []
    for i in range(0, len(json_hatch["points"]), 2):
        point_list.append([json_hatch["points"][i], json_hatch["points"][i + 1]])

    return Hatch(point_list, json_hatch["layer_name"], json_hatch["pattern"], existing_angles)
