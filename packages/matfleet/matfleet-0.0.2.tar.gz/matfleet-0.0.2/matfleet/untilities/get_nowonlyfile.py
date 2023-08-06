#   coding: utf-8
#   This file is part of matfleet.

#   matfleet is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/10/22"

import os
from pathlib import PurePath


def get_now_allfiles(path:str, suffix:list=None):

    assert os.path.exists(path)
    final_pt = []
    for subfn in os.listdir(path):
        if PurePath(subfn).suffix.lower() in suffix:
            final_pt.append(os.path.join(path, subfn))
        else:
            pass

    return final_pt


def abs_file(filename):
    return os.path.abspath(os.path.join(os.getcwd(), filename))