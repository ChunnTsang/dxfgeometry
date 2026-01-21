# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from json import loads
from src.dxfgeometry.json_geometry.json_base_class import Jsonable
from src.dxfgeometry.json_geometry.json_cad_layer import JsonCADLayer, json_cad_layer_to_object
from src.dxfgeometry.geometry.cad_result import CADReadResult
from src.dxfgeometry.geometry.cad_layer import CADLayer


class JsonCADReadResult(Jsonable):
    file_name: str = None
    layers: dict[str, JsonCADLayer] = None
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    existing_angle_list: list[float]

    def __init__(self, cad_read_result: CADReadResult):
        self.file_name = cad_read_result.get_file_name()
        self.x_range = cad_read_result.get_x_range()
        self.y_range = cad_read_result.get_y_range()
        self.existing_angle_list = cad_read_result.get_existing_angles()

        self.layers = {}
        for layer_name in cad_read_result.get_layers():
            self.layers[layer_name] = JsonCADLayer(cad_read_result.get_layers()[layer_name])


def json_cad_read_result_to_object(json_cad_read_result_str):
    layer_dict: dict[str, CADLayer] = {}
    json_cad_read_result = loads(json_cad_read_result_str)
    existing_angle = json_cad_read_result["existing_angle_list"]
    for layer_name, json_layer in json_cad_read_result["layers"].items():
        layer_dict[layer_name] = json_cad_layer_to_object(json_layer, existing_angle)
    return CADReadResult(json_cad_read_result["file_name"], layer_dict, existing_angle)
