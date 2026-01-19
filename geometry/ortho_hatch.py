# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

from geometry.ortho_polygon import OrthoPolygon
from config import default_point_precision


class OrthoHatch(OrthoPolygon):
    _hatch_pattern_name: str

    def __init__(self, point_list: list[list[float]], layer_name: str, hatch_pattern_name: str,
                 existing_angle_list: list[float], point_precision: int = default_point_precision) -> None:
        super(OrthoHatch, self).__init__(point_list, layer_name, existing_angle_list, point_precision=point_precision)
        self._hatch_pattern_name = hatch_pattern_name

    def get_hatch_pattern_name(self) -> str:
        return self._hatch_pattern_name
