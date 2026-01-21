# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from parser import read_dxf_to_geometry
from json_geometry.json_cad_result import JsonCADReadResult
from util.tools import save_json_file


if __name__ == '__main__':
    dxf_file_path = 'demo_file.dxf'
    cad_read_result = read_dxf_to_geometry(dxf_file_path)
    json_result = JsonCADReadResult(cad_read_result)
    save_json_file(json_result, 'result.json')
    print('>>>>>> Read complete! <<<<<<')
