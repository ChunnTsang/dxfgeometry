# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

import json


class Jsonable(object):
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)

    def save_to_file(self, output):
        return json.dump(self, output, indent=4, default=lambda o: o.__dict__)
