# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.json_geometry.json_cad_element import JsonCADElement
from dxfgeometry.json_geometry.json_line import JsonLine
from dxfgeometry.geometry.polyline import Polyline


class JsonPolyline(JsonCADElement):
    points: list[float]
    line_list: list[JsonLine]
    extra_info: dict

    def __init__(self, polyline: Polyline):
        super(JsonPolyline, self).__init__(polyline.get_layer_name(), "POLYLINE")
        self.points = polyline.get_coord_list_flatten()
        self.line_list = []
        for line in polyline.get_line_list():
            self.line_list.append(JsonLine(line))
        self.extra_info = polyline.get_extra_info()


def json_polyline_to_polyline(json_polyline, existing_angles: list[float]):
    point_list: list[list[float]] = []
    for i in range(0, len(json_polyline["points"]), 2):
        point_list.append([json_polyline["points"][i], json_polyline["points"][i + 1]])

    extra_info = json_polyline["extra_info"] if "extra_info" in json_polyline else {}
    return Polyline(point_list, json_polyline["layer_name"], existing_angles, extra_info)

