# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""


class LineLengthException(ValueError):
    _point_list: list[list[float]]
    _track_back: str

    def __init__(self, point_list: list[list[float]]):
        self._point_list = point_list
        self._track_back = ""

    def __str__(self):
        return "该直线长度为0"

    def append_track_back(self, trace_back: str) -> None:
        self._track_back += trace_back

    def get_point_list(self) -> list[list[float]]:
        return self._point_list
