# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

import math
from src.dxfgeometry.geometry.point import Point
from typing import Optional
from shapely.geometry import LineString as ShapelyLineString
from src.dxfgeometry.config import default_angle_precision, default_min_angle_difference, default_strong_orthogonality, \
    default_expanded_length, default_point_min_diff


def check_approximate_angle(angle: float, existing_angle_list: list[float], min_angle_difference: float,
                            strong_orthogonality: bool) -> float:
    angle_exists = False
    first_level = False
    for existing_angle in existing_angle_list:
        if abs(existing_angle - angle) < min_angle_difference or \
                abs(existing_angle - (angle - 180)) < min_angle_difference or \
                abs(existing_angle - 180 - angle) < min_angle_difference:
            if existing_angle == angle:
                angle = existing_angle
                angle_exists = True
                break
            else:
                angle = existing_angle
                angle_exists = True
                first_level = True

        elif (min_angle_difference <= abs(existing_angle - angle) < min_angle_difference * 2 or
              min_angle_difference <= abs(existing_angle - (angle - 180)) < min_angle_difference * 2 or
              min_angle_difference <= abs(existing_angle - 180 - angle) < min_angle_difference * 2) and \
                not first_level:
            if angle > existing_angle:
                angle = existing_angle + min_angle_difference * 2
                if angle >= 180:
                    angle -= 180
            elif angle < existing_angle:
                angle = existing_angle - min_angle_difference * 2
                if angle < 0:
                    angle += 180

    if not angle_exists:
        if strong_orthogonality:
            if math.isclose(angle, 90, abs_tol=min_angle_difference * 2):
                angle = 90
            elif math.isclose(angle, 0, abs_tol=min_angle_difference * 2) or \
                    math.isclose(angle, 180, abs_tol=min_angle_difference * 2):
                angle = 0
            existing_angle_list.append(angle)
        else:
            existing_angle_list.append(angle)
    return angle


class Angle(object):
    _angle: float
    _angle_in_radius: float
    _angle_precision: int
    _min_angle_difference: float
    _strong_orthogonality: bool

    def __init__(self, angle: float, existing_angle_list: list[float], angle_precision: int = default_angle_precision,
                 min_angle_difference: float = default_min_angle_difference,
                 strong_orthogonality: bool = default_strong_orthogonality) -> None:
        if angle < 0 or angle >= 180:
            raise ValueError("Angle初始化错误：角度范围错误。得到的角度为%d", angle)

        self._angle_precision = angle_precision
        self._min_angle_difference = min_angle_difference
        self._strong_orthogonality = strong_orthogonality

        angle = round(angle, self._angle_precision)
        if angle == 180:
            angle = 0

        angle = check_approximate_angle(angle, existing_angle_list, self._min_angle_difference,
                                        self._strong_orthogonality)

        self._angle = angle
        self._angle_in_radius = self._angle * (math.pi / 180)

    def get_angle(self) -> float:
        return self._angle

    def get_angle_in_radius(self) -> float:
        return self._angle_in_radius

    def get_angle_precision(self) -> int:
        return self._angle_precision

    def get_min_angle_difference(self) -> float:
        return self._min_angle_difference

    def get_strong_orthogonality(self) -> bool:
        return self._strong_orthogonality

    def get_another_point(self, ori_point: Point, length: float) -> Point:
        return Point(ori_point.get_x() + length * math.sin(self._angle_in_radius),
                     ori_point.get_y() + length * math.cos(self._angle_in_radius),
                     ori_point.get_layer_name())

    def get_mid_point(self, point: Point, length: float) -> Optional[Point]:
        return Point(point.get_x() + length * math.sin(self._angle_in_radius) / 2,
                     point.get_y() + length * math.cos(self._angle_in_radius) / 2,
                     point.get_layer_name())

    def get_point_at_dist(self, ori_point: Point, length: float, reverse: bool) -> Point:
        if not reverse:
            return Point(ori_point.get_x() + length * math.sin(self._angle_in_radius),
                         ori_point.get_y() + length * math.cos(self._angle_in_radius),
                         ori_point.get_layer_name())
        else:
            return Point(ori_point.get_x() - length * math.sin(self._angle_in_radius),
                         ori_point.get_y() - length * math.cos(self._angle_in_radius),
                         ori_point.get_layer_name())

    def get_mirroring_angle(self, mirroring_angle: "Angle", existing_angle_list: list[float]) -> float:
        mirroring_result: float = 2 * mirroring_angle.get_angle() - self._angle

        while mirroring_result >= 180:
            mirroring_result -= 180
        while mirroring_result < 0:
            mirroring_result += 180

        angle_not_exists = True
        for existing_angle in existing_angle_list:
            if abs(existing_angle - mirroring_result) < self._min_angle_difference or \
                    abs(existing_angle - (mirroring_result - 180)) < self._min_angle_difference:
                mirroring_result = existing_angle
                angle_not_exists = False
        if angle_not_exists:
            existing_angle_list.append(mirroring_result)

        return mirroring_result

    def get_ortho_angle(self, existing_angle_list: list[float]) -> "Angle":
        ortho_angle = (self.get_angle() + 90) % 180
        return Angle(ortho_angle, existing_angle_list)

    def get_key_coord_len_coord_of_point(self, point: Point) -> tuple[float, float]:
        one_point = self.get_point_at_dist(point, default_expanded_length, True)
        another_point = self.get_point_at_dist(point, default_expanded_length, False)

        expanded_line: ShapelyLineString = ShapelyLineString([[one_point.get_x(), one_point.get_y()],
                                                              [another_point.get_x(), another_point.get_y()]])

        angle_in_radius: float = self._angle_in_radius + math.pi / 2
        perpendicular_line: ShapelyLineString = ShapelyLineString([
            [default_expanded_length * math.sin(angle_in_radius),
             default_expanded_length * math.cos(angle_in_radius)],
            [-default_expanded_length * math.sin(angle_in_radius),
             -default_expanded_length * math.cos(angle_in_radius)]
        ])

        intersection_point = perpendicular_line.intersection(expanded_line)
        x_coord, y_coord = list(intersection_point.coords)[0]

        if (abs(y_coord) < default_point_min_diff and
            x_coord < -default_point_min_diff) or \
                y_coord > default_point_min_diff:
            key_coord = - math.sqrt(x_coord ** 2 + y_coord ** 2)
        else:
            key_coord = math.sqrt(x_coord ** 2 + y_coord ** 2)

        if self._angle < 90:
            if point.get_x() > x_coord or point.get_y() > y_coord:
                length_coord = math.sqrt((point.get_x() - x_coord) ** 2 + (point.get_y() - y_coord) ** 2)
            else:
                length_coord = -math.sqrt((point.get_x() - x_coord) ** 2 + (point.get_y() - y_coord) ** 2)
        else:
            if point.get_x() > x_coord or point.get_y() < y_coord:
                length_coord = math.sqrt((point.get_x() - x_coord) ** 2 + (point.get_y() - y_coord) ** 2)
            else:
                length_coord = -math.sqrt((point.get_x() - x_coord) ** 2 + (point.get_y() - y_coord) ** 2)

        return key_coord, length_coord

