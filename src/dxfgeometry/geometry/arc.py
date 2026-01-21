# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.geometry.cad_element import CADElement
from src.dxfgeometry.config import default_point_precision


class Arc(CADElement):
    _x: float
    _y: float
    _start_angle: float
    _end_angle: float
    _radius: float
    _point_precision: int

    def __init__(self, x: float, y: float, start_angle: float, end_angle: float, radius: float, layer_name: str,
                 point_precision: int = default_point_precision) -> None:
        super(Arc, self).__init__(layer_name)

        self._point_precision = point_precision
        self._x = round(x, self._point_precision)
        self._y = round(y, self._point_precision)
        self._radius = round(radius, self._point_precision)
        self._start_angle = round(start_angle, self._point_precision)
        self._end_angle = round(end_angle, self._point_precision)

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_start_angle(self) -> float:
        return self._start_angle

    def get_end_angle(self) -> float:
        return self._end_angle

    def get_radius(self) -> float:
        return self._radius

    def get_point_precision(self) -> int:
        return self._point_precision
