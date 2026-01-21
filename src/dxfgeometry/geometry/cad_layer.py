# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.geometry.line import Line
from src.dxfgeometry.geometry.polygon import Polygon
from src.dxfgeometry.geometry.ortho_polygon import OrthoPolygon
from src.dxfgeometry.geometry.text import Text
from src.dxfgeometry.geometry.ortho_hatch import OrthoHatch
from src.dxfgeometry.geometry.hatch import Hatch
from src.dxfgeometry.geometry.point import Point
from src.dxfgeometry.geometry.circle import Circle
from src.dxfgeometry.geometry.arc import Arc
from src.dxfgeometry.geometry.ellipse import Ellipse
from src.dxfgeometry.geometry.polyline import Polyline


class CADLayer:
    _layer_name: str
    _color: str
    _point_list: list[Point]
    _circle_list: list[Circle]
    _arc_list: list[Arc]
    _ellipse_list: list[Ellipse]
    _text_list: list[Text]
    _line_list: list[Line]
    _ortho_polygon_list: list[OrthoPolygon]
    _ortho_hatch_list: list[OrthoHatch]
    _hatch_list: list[Hatch]
    _polyline_list: list[Polyline]
    _polygon_list: list[Polygon]
    _x_range: tuple[float, float] = None
    _y_range: tuple[float, float] = None

    def __init__(self, layer_name: str, color: str):
        self._layer_name = layer_name
        self._color = color
        self._text_list = []
        self._ortho_polygon_list = []
        self._line_list = []
        self._ortho_hatch_list = []
        self._hatch_list = []
        self._point_list = []
        self._circle_list = []
        self._arc_list = []
        self._ellipse_list = []
        self._polyline_list = []
        self._polygon_list = []

    def get_layer_name(self) -> str:
        return self._layer_name

    def get_color(self) -> str:
        return self._color

    def get_text_list(self) -> list[Text]:
        return self._text_list

    def get_line_list(self) -> list[Line]:
        return self._line_list

    def get_polygon_list(self) -> list[Polygon]:
        return self._polygon_list

    def get_ortho_polygon_list(self) -> list[OrthoPolygon]:
        return self._ortho_polygon_list

    def get_ortho_hatch_list(self) -> list[OrthoHatch]:
        return self._ortho_hatch_list

    def get_hatch_list(self) -> list[Hatch]:
        return self._hatch_list

    def get_point_list(self) -> list[Point]:
        return self._point_list

    def get_circle_list(self) -> list[Circle]:
        return self._circle_list

    def get_arc_list(self) -> list[Arc]:
        return self._arc_list

    def get_ellipse_list(self) -> list[Ellipse]:
        return self._ellipse_list

    def get_polyline_list(self) -> list[Polyline]:
        return self._polyline_list

    def add_text(self, text: Text):
        self._text_list.append(text)
        for point in text.get_anchor_point_list():
            self.extend_layer_boundary(point[0], point[1])

    def add_line(self, line: Line):
        self._line_list.append(line)
        self.extend_layer_boundary(line.get_start_point().get_x(), line.get_start_point().get_y())
        self.extend_layer_boundary(line.get_another_point().get_x(), line.get_another_point().get_y())

    def add_polygon(self, polygon: Polygon) -> None:
        self._polygon_list.append(polygon)
        for point in polygon.get_point_list():
            self.extend_layer_boundary(point[0], point[1])

    def add_ortho_polygon(self, polygon: OrthoPolygon):
        self._ortho_polygon_list.append(polygon)
        for point in polygon.get_point_list():
            self.extend_layer_boundary(point[0], point[1])

    def add_hatch(self, hatch: Hatch):
        self._hatch_list.append(hatch)
        for point in hatch.get_point_list():
            self.extend_layer_boundary(point[0], point[1])

    def add_ortho_hatch(self, hatch: OrthoHatch):
        self._ortho_hatch_list.append(hatch)
        for point in hatch.get_point_list():
            self.extend_layer_boundary(point[0], point[1])

    def add_point(self, point: Point):
        self._point_list.append(point)
        self.extend_layer_boundary(point.get_x(), point.get_y())

    def add_circle(self, circle: Circle):
        self._circle_list.append(circle)

    def add_arc(self, arc: Arc):
        self._arc_list.append(arc)

    def add_ellipse(self, ellipse: Ellipse):
        self._ellipse_list.append(ellipse)

    def add_polyline(self, polyline: Polyline):
        self._polyline_list.append(polyline)
        for point in polyline.get_point_list():
            self.extend_layer_boundary(point[0], point[1])

    def get_x_range(self) -> tuple[float, float]:
        return self._x_range

    def get_y_range(self) -> tuple[float, float]:
        return self._y_range

    def extend_layer_boundary(self, x: float, y: float) -> None:
        if self._x_range is None:
            self._x_range = (x, x)
            self._y_range = (y, y)
            return

        (x1, x2) = self._x_range
        (y1, y2) = self._y_range

        if x < x1:
            self._x_range = (x, x2)
        elif x2 < x:
            self._x_range = (x1, x)

        if y < y1:
            self._y_range = (y, y2)
        elif y2 < y:
            self._y_range = (y1, y)
