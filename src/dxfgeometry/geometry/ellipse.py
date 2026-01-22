# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.geometry.cad_element import CADElement
import math
from dxfgeometry.config import default_point_precision


class Ellipse(CADElement):
    _x: float
    _y: float
    _start_param: float
    _end_param: float
    _major_axis: any
    _ratio: float
    _radius: float
    _xfact: float
    _yfact: float
    _point_precision: int

    def __init__(self, x: float, y: float, start_param: float, end_param: float, major_axis: any,
                 ratio: float, layer_name: str, point_precision: int = default_point_precision) -> None:
        super(Ellipse, self).__init__(layer_name)

        self._point_precision = point_precision
        self._x = round(x, self._point_precision)
        self._y = round(y, self._point_precision)
        self._major_axis = major_axis
        self._start_param = round(start_param, self._point_precision)
        self._end_param = round(end_param, self._point_precision)
        self._ratio = round(ratio, self._point_precision)
        self._angle1 = self._end_param * 2 * math.pi
        self._angle2 = self._start_param * 2 * math.pi
        self._rx, self._ry = self._major_axis.magnitude, self._major_axis.magnitude * self._ratio
        self._radius = math.sqrt(self._major_axis.x ** 2 + self._major_axis.y ** 2)
        self.xfact = self._rx / self._radius
        self.yfact = self._ry / self._radius

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_start_param(self) -> float:
        return self._start_param

    def get_end_param(self) -> float:
        return self._end_param

    def get_major_axis(self):
        return self._major_axis

    def get_ratio(self) -> float:
        return self._ratio

    def get_radius(self) -> float:
        return self._radius

    def get_xfact(self) -> float:
        return self.xfact

    def get_yfact(self) -> float:
        return self.yfact

    def get_point_precision(self) -> int:
        return self._point_precision

    def get_start_point(self, angle_distance) -> tuple[float, float]:
        tran_angle_distance = angle_distance / 180 * math.pi
        x1 = self._x + self._rx * math.cos(self._angle1 - tran_angle_distance)
        y1 = self._y + self._ry * math.sin(self._angle1 - tran_angle_distance)
        return x1, y1

    def get_end_point(self, angle_distance) -> tuple[float, float]:
        tran_angle_distance = angle_distance / 180 * math.pi
        return self._x + self._rx * math.sin(self._angle2 + tran_angle_distance), self._y + self._ry * math.sin \
            (self._angle2 + tran_angle_distance)
