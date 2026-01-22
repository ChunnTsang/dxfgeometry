# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

import math
from dxfgeometry.geometry.point import Point
from dxfgeometry.geometry.angle import Angle
from dxfgeometry.geometry.cad_element import CADElement
from dxfgeometry.config import default_point_precision
from dxfgeometry.exception.line_exception import LineLengthException


class Line(CADElement):
    _k: float
    _start_point: Point
    _another_point: Point
    _angle: Angle
    _length: float
    _key_coord: float
    _length_coord: float
    _ori_points: list[list[float]]
    _point_precision: int

    def __init__(self, x1: float, y1: float, x2: float, y2: float, layer_name: str, existing_angle_list: list[float],
                 extra_info=None, point_precision: int = default_point_precision) -> None:
        super(Line, self).__init__(layer_name)
        self._point_precision = point_precision
        x1, y1 = round(x1, self._point_precision), round(y1, self._point_precision)
        x2, y2 = round(x2, self._point_precision), round(y2, self._point_precision)

        extra_info = {} if extra_info is None else extra_info
        self._extra_info = extra_info

        if math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < 1:
            raise LineLengthException([[x1, y1], [x2, y2]])

        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        if x1 == x2:
            self._k = math.inf
            self._angle = Angle(0.0, existing_angle_list)
            if abs(0 - self._angle.get_angle()) > 45:
                self._start_point = Point(x1, max(y1, y2), layer_name)
                self._another_point = Point(x1, min(y1, y2), layer_name)
            else:
                self._start_point = Point(x1, min(y1, y2), layer_name)
                self._another_point = Point(x1, max(y1, y2), layer_name)
            self._length = abs(y1 - y2)
        else:
            self._k = (y2 - y1) / (x2 - x1)
            angle = 90.0 - math.atan(self._k) * 180.0 / math.pi
            self._angle = Angle(angle, existing_angle_list)
            if abs(angle - self._angle.get_angle()) > 45:
                x1, y1, x2, y2 = x2, y2, x1, y1
            self._start_point = Point(x1, y1, layer_name)
            self._another_point = Point(x2, y2, layer_name)
            self._length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        self._ori_points = [[x1, y1], [x2, y2]]

        self._key_coord, self._length_coord = self._angle.get_key_coord_len_coord_of_point(self._start_point)

    def __setitem__(self, key, value):
        self._extra_info[key] = value

    def __repr__(self) -> str:
        return "*线条* 起始点: (" + str(self.get_start_point().get_x()) + ", " + str(self.get_start_point().get_y()) \
               + ") 长度: " + str(self._length) + " 角度: " + str(self._angle.get_angle()) + " length coord " \
               + str(self._length_coord) + " key " + str(self._key_coord)

    def equal(self, other: "Line", precision: float) -> bool:
        if other is None:
            return False
        return self._start_point.equal(other.get_start_point(), precision) and \
               abs(self._length - other.get_length()) < precision and \
               abs(self._angle.get_angle() - other.get_angle().get_angle()) < precision

    def expend_at_both_end(self, length: float) -> None:
        self._start_point = self._angle.get_point_at_dist(self._start_point, length, True)
        self._another_point = self._angle.get_point_at_dist(self._another_point, length, False)
        self._length = self._length + 2 * length
        self._length_coord = self._length_coord - length
        self._ori_points = [self.get_start_point().get_x_y(), self.get_another_point().get_x_y()]

    def shorten_at_both_end(self, length: float) -> None:
        self._start_point = self._angle.get_point_at_dist(self._start_point, length, False)
        self._another_point = self._angle.get_point_at_dist(self._another_point, length, True)
        self._length = self._length - 2 * length
        self._length_coord = self._length_coord + length
        self._ori_points = [self.get_start_point().get_x_y(), self.get_another_point().get_x_y()]

    def shorten_at_start(self, length: float) -> None:
        self._start_point = self._angle.get_point_at_dist(self._start_point, length, False)
        self._length = self._length - length
        self._length_coord = self._length_coord + length
        self._ori_points = [self.get_start_point().get_x_y(), self.get_another_point().get_x_y()]

    def expand_at_start(self, length: float) -> None:
        self._start_point = self._angle.get_point_at_dist(self._start_point, length, True)
        self._length = self._length + length
        self._length_coord = self._length_coord - length
        self._ori_points = [self.get_start_point().get_x_y(), self.get_another_point().get_x_y()]

    def expand_at_end(self, length: float) -> None:
        self._length = self._length + length
        self._another_point = self._angle.get_point_at_dist(self._another_point, length, False)
        self._ori_points = [self.get_start_point().get_x_y(), self.get_another_point().get_x_y()]

    def shorten_at_end(self, length: float) -> None:
        self._length = self._length - length
        self._another_point = self._angle.get_point_at_dist(self._another_point, length, True)
        self._ori_points = [self.get_start_point().get_x_y(), self.get_another_point().get_x_y()]

    def get_mid_point(self) -> Point:
        return self._angle.get_mid_point(self._start_point, self._length)

    def get_x_and_y_list(self) -> tuple[list[float], list[float]]:
        x_list: list[float] = [self._start_point.get_x(), self.get_another_point().get_x()]
        y_list: list[float] = [self._start_point.get_y(), self.get_another_point().get_y()]
        return x_list, y_list

    def get_ori_points(self) -> list[list[float]]:
        return self._ori_points

    def get_start_point(self) -> Point:
        return self._start_point

    def get_length(self) -> float:
        return self._length

    def set_length(self, length: float):
        self._length = length

    def get_angle(self) -> Angle:
        return self._angle

    def get_another_point(self) -> Point:
        return self._another_point

    def get_key_coord(self) -> float:
        return self._key_coord

    def get_length_coord(self) -> float:
        return self._length_coord

    def get_mapping_length_coord(self, mapping_angle) -> float:
        _, len_coord = mapping_angle.get_key_coord_len_coord_of_point(self._start_point)
        return len_coord

    def get_end_length_coord(self) -> float:
        return self._length_coord + self._length

    def get_mid_length_coord(self) -> float:
        return self._length_coord + self._length * 0.5

    def get_extra_info(self):
        return self._extra_info

    def get_k(self) -> float:
        return self._k

    def get_point_precision(self) -> int:
        return self._point_precision
