# coding: utf-8
import os
import time
from seleniumqt.ezUi.util.f2def import funct
from seleniumqt.ezUi.util import highLightElement
import logging
import traceback

logger = logging.getLogger(__name__)


def run(p):
    try:

        rt = funct(os.path.basename(__file__), p)
        if type(rt) is tuple and len(rt) == 2:
            if rt[0]:
                highLightElement.run(p[0], p[1], 0)
            else:
                highLightElement.run(p[0], p[1], 1)
            return rt
    except:
        traceback.print_exc()
