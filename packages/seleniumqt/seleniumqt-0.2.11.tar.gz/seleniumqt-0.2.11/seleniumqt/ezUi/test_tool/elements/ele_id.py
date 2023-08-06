# coding: utf-8
import logging
import time
from seleniumqt.ezUi.util import obj_sleep, v_alpha

logger = logging.getLogger(__name__)


def elements(p):
    try:
        wd = p[0]
        text_value = p[1][0]
        _en, _dg, _sp, _zh, _pu = v_alpha.run(text_value)
        if _en == 0 or _zh > 0:
            return
        v, t_ = obj_sleep.run(text_value)

        if str(text_value).startswith('/'):
            return
        ell = wd.find_elements_by_xpath("//*[@id='" + v + "']")
        if len(ell) == 1:

            # for iw in range(8):
            #     if ell[0].is_displayed():
            #         break
            # time.sleep(1)
            # time.sleep(t_)

            print(len(ell), ell[0].is_displayed(), ell[0].rect)

            if ell[0].is_displayed():
                return ell[0]

            pth = "//*[@id='" + v + "']"
            for iw in range(8):

                ell_anc = wd.find_elements_by_xpath(pth + '/..' * iw)

                print(4, iw, len(ell_anc), ell_anc[0].is_displayed())

                if len(ell_anc) == 1 and ell_anc[0].is_displayed():
                    return ell_anc[0]
                if len(ell_anc) > 1:
                    return

        elif len(ell) > 1:

            ele_n = list()
            for i in ell:
                if i.rect['width'] > 0 and i.rect['height'] > 0:
                    ele_n.append(i)
            if len(ele_n) == 1:
                return ele_n[0]

            for i in ele_n:
                logger.info('v:%s,tag:%s,rect:%s' %
                            (text_value, str(i.tag_name), str(i.rect)))
            return False

    except Exception as e:
        logger.info('%s' % (e))

    return None
