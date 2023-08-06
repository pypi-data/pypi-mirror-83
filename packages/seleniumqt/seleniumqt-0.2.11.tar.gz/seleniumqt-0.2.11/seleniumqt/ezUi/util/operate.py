#coding: utf-8
import os
from seleniumqt.ezUi.util.f2def import funct
from seleniumqt.ezUi.util import highLightElement


def run(p):
    highLightElement.run(p[0], p[1], 2)
    return funct(os.path.basename(__file__), p)
