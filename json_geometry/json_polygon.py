# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from json_geometry.json_cad_element import JsonCADElement
from geometry.polygon import Polygon


class JsonPolygon(JsonCADElement):
    points: list[float]
    mid_points: list[float]
    extra_info: dict

    def __init__(self, polygon: Polygon):
        super(JsonPolygon, self).__init__(polygon.get_layer_name(), "Polygon")
        self.points = polygon.get_coord_list_flatten()
        self.extra_info = polygon.get_extra_info()
        self.mid_points = polygon.get_mid_point_list_flatten()


def json_polygon_to_polygon(json_polygon: dict, existing_angles: list[float]) -> Polygon:
    point_list: list[list[float]] = []
    for i in range(0, len(json_polygon["points"]), 2):
        point_list.append([json_polygon["points"][i], json_polygon["points"][i + 1]])

    if "extra_info" in json_polygon and json_polygon["extra_info"] is not None:
        extra_info = json_polygon.get("extra_info", {})
    else:
        extra_info = {}

    if "layer_name" in json_polygon and json_polygon["layer_name"] is not None:
        layer_name = json_polygon["layer_name"]
    else:
        layer_name = ""

    return Polygon(point_list, layer_name, existing_angles, extra_info)
