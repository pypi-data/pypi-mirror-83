# coding: utf-8
import os
import logging
from seleniumqt.ezUi.util.sk2 import gte
import traceback

logger = logging.getLogger(__name__)


def attr_ele(fn, ele, p):
    imp = 'test_tool' + '.' + fn + '.' + ele

    try:
        dd = __import__(imp, fromlist=True)
        if hasattr(dd, fn):
            f = getattr(dd, fn, None)
            t = f(p)
            return t
    except:
        traceback.print_exc()


def funct(fn, p):
    try:
        pt = os.listdir(os.getcwd() + '/test_tool/' + fn[:-3])
        el = [i[:-3] for i in pt if i.startswith(fn[:3] + '_') and i.endswith('.py')]
        el.sort()

        if p[0]:
            for i in el:
                try:
                    if fn[:-3] == 'operate':
                        p[1].get_attribute("type")
                except:
                    return
                try:
                    # print('^' * 8, i)
                    t = attr_ele(fn[:-3], i, p)
                    if t:
                        if fn[:-3] == 'operate':
                            logger.info("operate::%s, %s, %s" % (i, p[2], p[3]))

                        if type(t) is not str and fn[:-3] == 'elements':

                            logger.info("elements::%s, %s, %s, %s, %s, %s"
                                        % (i, p[1][3], p[1][1], p[1][2], p[1][0], t.rect))
                            on_screen = gte(p[0], t)
                            if on_screen:
                                t = attr_ele(fn[:-3], i, p)
                        return t
                except:
                    traceback.print_exc()
    except:
        traceback.print_exc()

    # return False, 0
