# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.json_geometry.json_cad_element import JsonCADElement
from src.dxfgeometry.geometry.ortho_polygon import OrthoPolygon


class JsonOrthoPolygon(JsonCADElement):
    points: list[float]
    width: float
    length: float
    mid_points: list[float]
    extra_info: dict

    def __init__(self, polygon: OrthoPolygon):
        super(JsonOrthoPolygon, self).__init__(polygon.get_layer_name(), "OrthoPolygon")
        self.points = polygon.get_coord_list_flatten()
        self.width, self.length, _, _ = polygon.get_width_and_length()
        self.extra_info = polygon.get_extra_info()
        self.mid_points = polygon.get_mid_point_list_flatten()


def json_ortho_polygon_to_ortho_polygon(json_ortho_polygon: dict, existing_angles: list[float]) -> OrthoPolygon:
    point_list: list[list[float]] = []
    for i in range(0, len(json_ortho_polygon["points"]), 2):
        point_list.append([json_ortho_polygon["points"][i], json_ortho_polygon["points"][i + 1]])

    if "extra_info" in json_ortho_polygon and json_ortho_polygon["extra_info"] is not None:
        extra_info = json_ortho_polygon.get("extra_info", {})
    else:
        extra_info = {}

    if "layer_name" in json_ortho_polygon and json_ortho_polygon["layer_name"] is not None:
        layer_name = json_ortho_polygon["layer_name"]
    else:
        layer_name = ""

    return OrthoPolygon(point_list, layer_name, existing_angles, extra_info)
