# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.geometry.cad_element import CADElement
from src.dxfgeometry.config import default_point_precision


class Circle(CADElement):
    _x: float
    _y: float
    _radius: float
    _point_precision: int

    def __init__(self, x: float, y: float, radius: float, layer_name: str,
                 point_precision: int = default_point_precision) -> None:
        super(Circle, self).__init__(layer_name)

        self._point_precision = point_precision
        self._x = round(x, self._point_precision)
        self._y = round(y, self._point_precision)
        self._radius = radius

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_radius(self) -> float:
        return self._radius

    def get_point_precision(self) -> int:
        return self._point_precision
