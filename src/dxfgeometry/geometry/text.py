# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.geometry.angle import Angle
from dxfgeometry.geometry.cad_element import CADElement


class Text(CADElement):
    _angle: Angle
    _content: str
    _width: float
    _height: float
    _anchor_point_list: list[list[float]]
    _layer_name: str

    def __init__(self, anchor_point_list: list[list[float]], layer_name: str, content: str,
                 angle: float, width: float, height: float, existing_angle_list: list[float]) -> None:
        super(Text, self).__init__(layer_name)

        self._layer_name = layer_name
        self._anchor_point_list = []
        for point in anchor_point_list:
            self.add_anchor_point(point)
        self._angle = Angle(angle, existing_angle_list)
        self._content = content
        self._width = max(width, 0.1) if width is not None else 0.1
        self._height = height

    def __repr__(self):
        return self._content

    def add_anchor_point(self, point):
        if len(self._anchor_point_list) == 0:
            self._anchor_point_list.append(point)
            return
        for existing_point in self._anchor_point_list:
            if abs(point[0] - existing_point[0]) > 10 or abs(point[1] - existing_point[1]) > 10:
                self._anchor_point_list.append(point)
                return

    def get_angle(self) -> Angle:
        return self._angle

    def get_content(self) -> str:
        return self._content

    def update_content(self, new_content):
        self._content = new_content

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def get_anchor_point_list(self) -> list[list[float]]:
        return self._anchor_point_list
