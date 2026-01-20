# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""


class ReadElementException(Exception):
    _point_list: list[list[float]]
    _reason: str

    def __init__(self, point_list: list[list[float]], reason: str):
        self._point_list = point_list
        self._reason = reason

    def get_point_list(self) -> list[list[float]]:
        return self._point_list

    def get_reason(self) -> str:
        return self._reason

    def __str__(self):
        return self._reason


def handle_exception(e: Exception, point_list: list[list[float]], shape_with_exception: list[ReadElementException]):
    shape_with_exception.append(ReadElementException(point_list, str(e)))
