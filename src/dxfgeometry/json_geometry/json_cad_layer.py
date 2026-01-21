# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.json_geometry.json_base_class import Jsonable
from src.dxfgeometry.json_geometry.json_point import JsonPoint, json_point_to_point
from src.dxfgeometry.json_geometry.json_circle import JsonCircle, json_circle_to_circle
from src.dxfgeometry.json_geometry.json_arc import JsonArc, json_arc_to_arc
from src.dxfgeometry.json_geometry.json_ellipse import JsonEllipse, json_ellipse_to_ellipse
from src.dxfgeometry.json_geometry.json_text import JsonText, json_text_to_text
from src.dxfgeometry.json_geometry.json_line import JsonLine, json_line_to_line
from src.dxfgeometry.json_geometry.json_ortho_polygon import JsonOrthoPolygon, json_ortho_polygon_to_ortho_polygon
from src.dxfgeometry.json_geometry.json_ortho_hatch import JsonOrthoHatch, json_ortho_hatch_to_ortho_hatch
from src.dxfgeometry.json_geometry.json_hatch import JsonHatch, json_hatch_to_hatch
from src.dxfgeometry.json_geometry.json_polyline import JsonPolyline, json_polyline_to_polyline
from src.dxfgeometry.json_geometry.json_polygon import JsonPolygon, json_polygon_to_polygon
from src.dxfgeometry.geometry.cad_layer import CADLayer


class JsonCADLayer(Jsonable):
    layer_name: str
    color: str
    point_list: list[JsonPoint]
    circle_list: list[JsonCircle]
    arc_list: list[JsonArc]
    ellipse_list: list[JsonEllipse]
    text_list: list[JsonText]
    line_list: list[JsonLine]
    ortho_polygon_list: list[JsonOrthoPolygon]
    ortho_hatch_list: list[JsonOrthoHatch]
    hatch_list: list[JsonHatch]
    polyline_list: list[JsonPolyline]
    polygon_list: list[JsonPolygon]
    x_range: tuple[float, float]
    y_range: tuple[float, float]

    def __init__(self, cad_layer: CADLayer):
        self.layer_name = cad_layer.get_layer_name()
        self.color = cad_layer.get_color()

        self.point_list = []
        for point in cad_layer.get_point_list():
            self.point_list.append(JsonPoint(point))

        self.circle_list = []
        for circle in cad_layer.get_circle_list():
            self.circle_list.append(JsonCircle(circle))

        self.arc_list = []
        for arc in cad_layer.get_arc_list():
            self.arc_list.append(JsonArc(arc))

        self.ellipse_list = []
        for ellipse in cad_layer.get_ellipse_list():
            self.ellipse_list.append(JsonEllipse(ellipse))

        self.text_list = []
        for text in cad_layer.get_text_list():
            self.text_list.append(JsonText(text))

        self.line_list = []
        for line in cad_layer.get_line_list():
            self.line_list.append(JsonLine(line))

        self.ortho_polygon_list = []
        for ortho_polygon in cad_layer.get_ortho_polygon_list():
            self.ortho_polygon_list.append(JsonOrthoPolygon(ortho_polygon))

        self.ortho_hatch_list = []
        for ortho_hatch in cad_layer.get_ortho_hatch_list():
            self.ortho_hatch_list.append(JsonOrthoHatch(ortho_hatch))

        self.hatch_list = []
        for hatch in cad_layer.get_hatch_list():
            self.hatch_list.append(JsonHatch(hatch))

        self.polyline_list = []
        for polyline in cad_layer.get_polyline_list():
            self.polyline_list.append(JsonPolyline(polyline))

        self.polygon_list = []
        for polygon in cad_layer.get_polygon_list():
            self.polygon_list.append(JsonPolygon(polygon))

        self.x_range = cad_layer.get_x_range()
        self.y_range = cad_layer.get_y_range()


def json_cad_layer_to_object(json_cad_layer, existing_angle: list[float]):
    layer_name = json_cad_layer["layer_name"]
    color = json_cad_layer["color"]
    cad_layer = CADLayer(layer_name, color)

    for json_point in json_cad_layer["point_list"]:
        cad_layer.add_point(json_point_to_point(json_point))

    for json_circle in json_cad_layer["circle_list"]:
        cad_layer.add_circle(json_circle_to_circle(json_circle))

    for json_arc in json_cad_layer["arc_list"]:
        cad_layer.add_arc(json_arc_to_arc(json_arc))

    for json_ellipse in json_cad_layer["ellipse_list"]:
        cad_layer.add_ellipse(json_ellipse_to_ellipse(json_ellipse))

    for json_text in json_cad_layer["text_list"]:
        cad_layer.add_text(json_text_to_text(json_text, existing_angle))

    for json_line in json_cad_layer["line_list"]:
        cad_layer.add_line(json_line_to_line(json_line, existing_angle))

    for json_ortho_polygon in json_cad_layer["ortho_polygon_list"]:
        cad_layer.add_ortho_polygon(json_ortho_polygon_to_ortho_polygon(json_ortho_polygon, existing_angle))

    for json_ortho_hatch in json_cad_layer["ortho_hatch_list"]:
        cad_layer.add_ortho_hatch(json_ortho_hatch_to_ortho_hatch(json_ortho_hatch, existing_angle))

    for json_hatch in json_cad_layer["hatch_list"]:
        cad_layer.add_hatch(json_hatch_to_hatch(json_hatch, existing_angle))

    for json_polyline in json_cad_layer["polyline_list"]:
        cad_layer.add_polyline(json_polyline_to_polyline(json_polyline, existing_angle))

    for json_polygon in json_cad_layer["polygon_list"]:
        cad_layer.add_polygon(json_polygon_to_polygon(json_polygon, existing_angle))

    return cad_layer

