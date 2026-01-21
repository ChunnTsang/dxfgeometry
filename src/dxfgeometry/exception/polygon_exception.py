# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""


class PolygonException(Exception):
    _point_list: list[list[float]]

    def __init__(self, point_list: list[list[float]]):
        super().__init__()
        self._point_list = point_list

    def get_points(self):
        return self._point_list


class PolygonAngleException(PolygonException):
    _angle_num: int

    def __init__(self, angle_num: int, point_list: list[list[float]]):
        super(PolygonException, self).__init__(point_list)
        self._angle_num = angle_num
        self._point_list = point_list

    def __str__(self):
        return f"多边形角度个数错误。有{self._angle_num}个角度，形状点位:{self._point_list}"


class PolygonTinyAreaException(PolygonException):
    def __init__(self, point_list: list[list[float]]):
        super(PolygonTinyAreaException, self).__init__(point_list)

    def __str__(self):
        return "多边形过于小"
