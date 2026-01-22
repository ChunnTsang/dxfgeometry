# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.json_geometry.json_cad_element import JsonCADElement
from dxfgeometry.geometry.line import Line


class JsonLine(JsonCADElement):
    points: list[float]
    start_x: float
    start_y: float
    length: float
    extra_info: dict

    def __init__(self, line: Line):
        super(JsonLine, self).__init__(line.get_layer_name(), "Line")
        self.points = []
        for point in line.get_ori_points():
            self.points.append(point[0])
            self.points.append(point[1])
        self.start_x = line.get_start_point().get_x()
        self.start_y = line.get_start_point().get_y()
        self.length = line.get_length()
        self.extra_info = line.get_extra_info()


def json_line_to_line(json_line, existing_angle_list: list[float]) -> Line:
    extra_info = json_line["extra_info"] if "extra_info" in json_line else {}
    return Line(json_line["points"][0], json_line["points"][1], json_line["points"][2], json_line["points"][3],
                json_line["layer_name"], existing_angle_list, extra_info)

