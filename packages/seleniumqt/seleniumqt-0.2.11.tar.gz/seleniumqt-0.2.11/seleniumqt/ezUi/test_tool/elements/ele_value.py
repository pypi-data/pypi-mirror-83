# coding: utf-8
import logging
from seleniumqt.ezUi.util import obj_sleep
import traceback
import time
from seleniumqt.ezUi.util.object import ui_mask

from seleniumqt.ezUi.util.object import del_ele

logger = logging.getLogger(__name__)


def elements(p):
    v, t_ = obj_sleep.run(p[1][0])
    try:
        wd = p[0]
        ele_return = list()
        ell = wd.find_elements_by_tag_name("input")

        ell_all_del = del_ele.run_rect(ell)

        for i in ell_all_del:
            try:
                if i.get_attribute("value") == v:
                    mask_show, ele_disable = ui_mask.run(wd, i, 0)
                    print(v, mask_show, ele_disable)
                    if not mask_show and not ele_disable:
                        ele_return.append(i)
            except:
                continue
        if len(ele_return) == 1:
            return ele_return[0]
        else:
            for i in ele_return:
                print(i.rect)
    except:
        return
