# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.geometry.cad_layer import CADLayer


class CADReadResult:
    _file_name: str = None
    _layers: dict[str, CADLayer] = None
    _x_range: tuple[int|float, int|float]
    _y_range: tuple[int|float, int|float]
    _existing_angle: list[float]

    def __init__(self, file_name: str, layers: dict[str, "CADLayer"], existing_angle: list[float]) -> None:
        self._file_name = file_name
        self._layers = layers
        self._existing_angle = existing_angle

        if len(self._layers) == 0:
            return

        self._x_range = (min([o.get_x_range()[0] for (_, o) in self._layers.items() if o.get_x_range()]),
                         max([o.get_x_range()[1] for (_, o) in self._layers.items() if o.get_x_range()]))
        self._y_range = (min([o.get_y_range()[0] for (_, o) in self._layers.items() if o.get_y_range()]),
                         max([o.get_y_range()[1] for (_, o) in self._layers.items() if o.get_y_range()]))

    def get_file_name(self) -> str:
        return self._file_name

    def get_existing_angles(self) -> list[float]:
        return self._existing_angle

    def get_layers(self) -> dict[str, "CADLayer"]:
        return self._layers

    def get_x_range(self) -> tuple[int, int]:
        return self._x_range

    def get_y_range(self) -> tuple[int, int]:
        return self._y_range

    def merge_with_other_result(self, other: "CADReadResult") -> None:
        self._layers = self._layers | other.get_layers()
        self._x_range = (
            min(self._x_range[0], other.get_x_range()[0]), max(self._x_range[1], other.get_x_range()[1]))
        self._y_range = (
            min(self._y_range[0], other.get_y_range()[0]), max(self._y_range[1], other.get_y_range()[1]))
