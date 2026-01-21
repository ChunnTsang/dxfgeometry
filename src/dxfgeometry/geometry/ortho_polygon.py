# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

import math
from src.dxfgeometry.geometry.line import Line
from src.dxfgeometry.geometry.polygon import Polygon
from src.dxfgeometry.geometry.angle import Angle
from shapely.geometry import Polygon as ShapelyPolygon
from typing import Optional
from src.dxfgeometry.exception.polygon_exception import PolygonAngleException
from src.dxfgeometry.config import default_point_precision


class OrthoPolygon(Polygon):
    _point_list: list[list[float]]
    _outline_dict: dict[float, dict[float, list[Line]]]
    _length_mid_line: Optional[Line]
    _width_mid_line: Optional[Line]
    _angle: Optional[Angle]

    def __init__(self, point_list: list[list[float]], layer_name: str, existing_angle_list: list[float],
                 extra_info=None, point_precision: int = default_point_precision) -> None:
        super(OrthoPolygon, self).__init__(point_list, layer_name, existing_angle_list, extra_info, point_precision)

        self._length_mid_line = None
        self._width_mid_line = None
        self._angle = None
        angle_list: list[float] = list(self._outline_dict.keys())

        if len(angle_list) != 2 or round(abs(abs(angle_list[0] - angle_list[1]) - 90), 0) > 1:
            raise PolygonAngleException(len(angle_list), self._point_list)

    def is_rect(self) -> bool:
        is_rect = True
        outline_dict: dict[float, dict[float, list[Line]]] = self.get_outline_dict()
        for angle in outline_dict:
            if len(outline_dict[angle]) != 2:
                is_rect = False
        return is_rect

    def get_width(self) -> float:
        point_list: list[list[float]] = self.get_point_list()
        rectangle = ShapelyPolygon(point_list)
        min_bounding_rect = rectangle.minimum_rotated_rectangle

        vertices = min_bounding_rect.exterior.coords
        edge1_length = math.sqrt((vertices[0][0] - vertices[1][0]) ** 2 + (vertices[0][1] - vertices[1][1]) ** 2)
        edge2_length = math.sqrt((vertices[1][0] - vertices[2][0]) ** 2 + (vertices[1][1] - vertices[2][1]) ** 2)

        width = min(edge1_length, edge2_length)
        return round(width)

    def get_width_and_length(self) -> tuple[float, float, float, Optional[Angle]]:
        temp_width = float('inf')
        temp_length = -float('inf')
        length_angle = float('inf')
        angle_file = None
        if sorted(list(self._outline_dict.keys())) == [0.0, 90.0] or \
                (len(list(self._outline_dict.keys())) == 2 and
                 abs(list(self._outline_dict.keys())[0] - list(self._outline_dict.keys())[1]) - 90 < 1):
            for angle, lines in self._outline_dict.items():
                temp_value = lines[next(iter(lines))][0].get_length()
                temp_width = temp_value if temp_width > temp_value else temp_width
                if temp_length < temp_value:
                    temp_length = temp_value
                    length_angle = angle
                    angle_file = list(lines.values())[0][0].get_angle()
            return round(temp_width, 0), round(temp_length, 0), length_angle, angle_file
        else:
            return temp_width, temp_length, length_angle, angle_file

    def get_length_coord_and_width(self) -> str:
        point_list = self._point_list
        mid_line_1: Line = Line((point_list[0][0] + point_list[1][0]) / 2,
                                (point_list[0][1] + point_list[1][1]) / 2,
                                (point_list[2][0] + point_list[3][0]) / 2,
                                (point_list[2][1] + point_list[3][1]) / 2,
                                "", [])

        mid_line_2: Line = Line((point_list[0][0] + point_list[3][0]) / 2,
                                (point_list[0][1] + point_list[3][1]) / 2,
                                (point_list[1][0] + point_list[2][0]) / 2,
                                (point_list[1][1] + point_list[2][1]) / 2,
                                "", [])
        if mid_line_1.get_length() >= mid_line_2.get_length():
            self._angle = mid_line_1.get_angle()
            self._length_mid_line = mid_line_1
            self._width_mid_line = mid_line_2
        else:
            self._angle = mid_line_2.get_angle()
            self._length_mid_line = mid_line_2
            self._width_mid_line = mid_line_1
        return str(round(self._length_mid_line.get_key_coord() + 0.4, 0)) + "_" + str(self.get_width())

    def get_polygon_angle(self) -> Angle:
        outline = self._outline_dict
        max_length = -float('inf')
        the_angle = None
        for angle_value, lines_dict in outline.items():
            for key_coord, lines in lines_dict.items():
                for line in lines:
                    if line.get_length() > max_length:
                        max_length = line.get_length()
                        the_angle = line.get_angle()
        return the_angle

    def update_point_list(self, new_point_list: list[list[float]]):
        self._point_list = new_point_list

    def update_point_list_round(self, point_precision):
        rounded_point_list: list[list[float]] = []
        for coord in self.get_point_list():
            rounded_point_list.append([round(x, point_precision) for x in coord])
        self._point_list = rounded_point_list

    def get_length_mid_line(self) -> Optional[Line]:
        return self._length_mid_line

    def get_width_mid_line(self) -> Optional[Line]:
        return self._width_mid_line

    def get_angle(self) -> Optional[Angle]:
        return self._angle

