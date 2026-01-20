# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from typing import Optional
from geometry.angle import Angle
from geometry.line import Line
from geometry.cad_element import CADElement
from config import default_point_precision, default_angle_threshold, default_coord_key_precision, \
    default_minimum_point_distance
from util.tools import calculate_distance, simplify_polygon_vertices, get_angle, get_rect_mid_point
from exception.line_exception import LineLengthException
from exception.polygon_exception import PolygonTinyAreaException


class Polygon(CADElement):
    _point_list: list[list[float]] = []
    _mid_point_list: list[list[float]] = []
    _outline_dict: dict[float, dict[float, list[Line]]] = {}
    _point_precision: int
    _extra_info: dict

    def __init__(self, point_list: list[list[float]], layer_name: str, existing_angle_list: list[float],
                 extra_info=None, point_precision: int = default_point_precision) -> None:
        super(Polygon, self).__init__(layer_name)

        self._point_precision = point_precision
        point_list = self.preprocessing_point_list(point_list, self._point_precision)
        self._point_list = point_list
        self._mid_point_list = get_rect_mid_point(self._point_list)
        self._outline_dict = {}
        extra_info = {} if extra_info is None else extra_info
        self._extra_info = extra_info

        try:
            for index in range(-1, len(point_list) - 1):
                line = Line(point_list[index][0], point_list[index][1],
                            point_list[index + 1][0], point_list[index + 1][1], layer_name, existing_angle_list)
                if abs(line.get_length()) < 0.01:
                    continue
                self._outline_dict.setdefault(line.get_angle().get_angle(), {})
                self._outline_dict[line.get_angle().get_angle()].\
                    setdefault(round(line.get_key_coord(), default_coord_key_precision), []).append(line)
        except LineLengthException as e:
            print(self._point_list)
            raise PolygonTinyAreaException(self._point_list)

        angle_list: list[float] = list(self._outline_dict.keys())
        if len(angle_list) == 0 or len(angle_list) == 1:
            raise PolygonTinyAreaException(self._point_list)

    def __setitem__(self, key, value):
        self._extra_info[key] = value

    def preprocessing_point_list(self, point_list: list[list[float]], point_precision: int) -> list[list[float]]:
        rounded_point_list: list[list[float]] = []
        last_point = None
        for coord in point_list:
            next_point = [round(x, point_precision) for x in coord]
            if calculate_distance(last_point, next_point) > 1:
                rounded_point_list.append(next_point)
                last_point = next_point
        point_list = rounded_point_list

        if len(point_list) > 4:
            new_point_list = simplify_polygon_vertices(point_list)
            if new_point_list:
                point_list = new_point_list

        points_index_to_remove: list[int] = []
        for i in range(0, len(point_list) - 1):
            if abs((point_list[i][0] - point_list[i + 1][0]) ** 2 +
                   (point_list[i][1] - point_list[i + 1][1]) ** 2) < default_minimum_point_distance:
                points_index_to_remove.append(i)
        if abs((point_list[0][0] - point_list[-1][0]) ** 2 +
               (point_list[0][1] - point_list[-1][1]) ** 2) < default_minimum_point_distance:
            points_index_to_remove.append(-1)
        for index in sorted(points_index_to_remove, reverse=True):
            del point_list[index]

        if len(point_list) < 3:
            raise PolygonTinyAreaException(self._point_list)

        points_index_to_remove: list[int] = []
        for i in range(-1, len(point_list) - 2):
            if abs(get_angle(point_list[i][0], point_list[i][1], point_list[i + 1][0], point_list[i + 1][1]) -
                   get_angle(point_list[i + 1][0], point_list[i + 1][1], point_list[i + 2][0],
                             point_list[i + 2][1])) < default_angle_threshold:
                points_index_to_remove.append(i + 1)
        if abs(get_angle(point_list[-2][0], point_list[-2][1], point_list[-1][0], point_list[-1][1]) -
               get_angle(point_list[-1][0], point_list[-1][1], point_list[0][0],
                         point_list[0][1])) < default_angle_threshold:
            points_index_to_remove.append(len(point_list) - 1)
        for index in sorted(points_index_to_remove, reverse=True):
            del point_list[index]

        return point_list

    def get_coord_list_flatten(self) -> list[float]:
        result = []
        for point in self._point_list:
            result.append(point[0])
            result.append(point[1])
        return result

    def is_rect(self) -> bool:
        is_rect = True
        outline_dict: dict[float, dict[float, list[Line]]] = self.get_outline_dict()
        for angle in outline_dict:
            if len(outline_dict[angle]) != 2:
                is_rect = False
        return is_rect

    def get_point_list(self) -> list[list[float]]:
        return self._point_list

    def get_mid_point_list(self):
        return self._mid_point_list

    def get_mid_point_list_flatten(self) -> list[float]:
        return [p for point in self._mid_point_list for p in point]

    def get_x_and_y_list(self) -> tuple[list[float], list[float]]:
        x_list: list[float] = []
        y_list: list[float] = []
        for point in self._point_list:
            x_list.append(point[0])
            y_list.append(point[1])
        x_list.append(x_list[0])
        y_list.append(y_list[0])
        return x_list, y_list

    def get_outline_dict(self) -> dict[float, dict[float, list[Line]]]:
        return self._outline_dict

    def get_angle_list(self) -> list[float]:
        return list(self._outline_dict.keys())

    def get_outlines(self) -> list[Line]:
        line_list: list[Line] = []
        for angle in self._outline_dict:
            for key in self._outline_dict[angle]:
                line_list += self._outline_dict[angle][key]
        return line_list

    def get_centroid(self) -> list[float]:
        x, y = self.get_x_and_y_list()
        return [sum(x[:-1]) / (len(x) - 1), sum(y[:-1]) / (len(y) - 1)]

    def get_width_and_length(self) -> tuple[float, float, float, Optional[Angle]]:
        temp_width = float('inf')
        temp_length = -float('inf')
        length_angle = float('inf')
        angle_file = None
        if sorted(list(self._outline_dict.keys())) == [0.0, 90.0] or \
                (len(list(self._outline_dict.keys())) == 2 and
                 abs( list(self._outline_dict.keys())[0] - list(self._outline_dict.keys())[1]) - 90 < 1):
            for angle, lines in self._outline_dict.items():
                temp_value = lines[next(iter(lines))][0].get_length()
                temp_width = temp_value if temp_width > temp_value else temp_width
                if temp_length < temp_value:
                    temp_length = temp_value
                    length_angle = angle
                    angle_file = list(lines.values())[0][0].get_angle()
            return temp_width, temp_length, length_angle, angle_file
        else:
            return temp_width, temp_length, length_angle, angle_file

    def get_extra_info(self):
        return self._extra_info

    def get_point_precision(self) -> int:
        return self._point_precision
