# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from geometry.cad_element import CADElement
from config import default_point_precision


class Point(CADElement):
    _x: float
    _y: float
    _point_precision: int

    def __init__(self, x: float, y: float, layer_name: str, point_precision: int = default_point_precision) -> None:
        super(Point, self).__init__(layer_name)
        self._point_precision = point_precision
        self._x = round(x, self._point_precision)
        self._y = round(y, self._point_precision)

    def get_x_y(self) -> list[float]:
        return [self._x, self._y]

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def set_x(self, x: float) -> None:
        self._x = x

    def set_y(self, y: float) -> None:
        self._y = y

    def get_point(self) -> "Point":
        return self

    def equal(self, other: "Point", precision: float) -> bool:
        return abs(self._x - other.get_x()) < precision and abs(self._y - other.get_y()) < precision

    def get_point_precision(self) -> int:
        return self._point_precision
