# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from geometry.cad_element import CADElement
from geometry.line import Line
from config import default_point_precision


def preprocessing_point_list(point_list: list[list[float]], point_precision: int):
    rounded_point_list: list[list[float]] = []
    for coord in point_list:
        rounded_point_list.append([round(x, point_precision) for x in coord])

    points_index_to_remove: list[int] = []
    for i in range(0, len(rounded_point_list) - 1):
        if abs((rounded_point_list[i][0] - rounded_point_list[i + 1][0]) ** 2 +
               (rounded_point_list[i][1] - rounded_point_list[i + 1][1]) ** 2) < 10:
            points_index_to_remove.append(i)

    if abs((rounded_point_list[0][0] - rounded_point_list[-1][0]) ** 2 +
           (rounded_point_list[0][1] - rounded_point_list[-1][1]) ** 2) < 10:
        points_index_to_remove.append(-1)

    for index in sorted(points_index_to_remove, reverse=True):
        del rounded_point_list[index]

    return rounded_point_list


class Polyline(CADElement):
    _point_list: list[list[float]]
    _line_list: list[Line]
    _point_precision: int

    def __init__(self, point_list: list[list[float]], layer_name: str, existing_angle_list: list[float],
                 extra_info=None, point_precision: int = default_point_precision) -> None:
        super(Polyline, self).__init__(layer_name)

        self._point_precision = point_precision
        rounded_point_list = preprocessing_point_list(point_list, self._point_precision)
        self._point_list = rounded_point_list
        self._line_list = []
        extra_info = {} if extra_info is None else extra_info
        self._extra_info = extra_info

        for i in range(len(rounded_point_list) - 1):
            self._line_list.append(Line(rounded_point_list[i][0], rounded_point_list[i][1],
                                        rounded_point_list[i+1][0], rounded_point_list[i+1][1], "",
                                        existing_angle_list))

    def __setitem__(self, key, value):
        self._extra_info[key] = value

    def get_point_list(self) -> list[list[float]]:
        return self._point_list

    def get_x_y_list(self) -> tuple[list[float], list[float]]:
        x_list, y_list = [], []
        for point in self._point_list:
            x_list.append(point[0])
            y_list.append(point[1])
        return x_list, y_list

    def get_line_list(self) -> list[Line]:
        return self._line_list

    def get_coord_list_flatten(self) -> list[float]:
        result = []
        for point in self._point_list:
            result.append(point[0])
            result.append(point[1])
        return result

    def get_extra_info(self):
        return self._extra_info

    def get_point_precision(self) -> int:
        return self._point_precision

