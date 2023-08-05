# coding: utf-8
import logging
from seleniumqt.ezUi.util.object import ui_mask
from seleniumqt.ezUi.util import obj_sleep, v_alpha

logger = logging.getLogger(__name__)


def elements(p):
    try:
        # from util import v_alpha
        _en, _dg, _sp, _zh, _pu = v_alpha.run(p[1][0])
        if _en == 0 or _zh > 0:
            return
        v, t_ = obj_sleep.run(p[1][0])

        if str(p[1][0]).startswith('/'):
            return

        for i_loop in range(3):
            ell_ = p[0].find_elements_by_xpath("//*[@name='" + v + "']")

            ell = ui_mask.un_mask_lg(p[0], ell_)

            if len(ell) == 1:
                return ell[0]
            elif len(ell) > 1 and i_loop == 2:
                for i in ell:
                    logger.info('ERROR::v:%s,tag:%s,rect:%s' % (v, str(i.tag_name), str(i.rect)))
                return ell[0]

            # ell = del_ele.run_rect_lg(ell_)
            #
            # ele_n = list()
            #
            # for ei in ell:
            #     mask_show, ele_disable = ui_mask.run(p[0], ei, i_loop * 2)
            #     if not mask_show and not ele_disable:
            #         ele_n.append(ei)
            # if len(ele_n) == 1:
            #     return ele_n[0]
            # elif len(ele_n) > 1 and i_loop == 2:
            #     for i in ell:
            #         logger.info('error_info::v:%s,tag:%s,rect:%s' % (v, str(i.tag_name), str(i.rect)))
            #     return ele_n[0]

            # if len(ell) == 1:
            #         return ell[0]
            # elif len(ell) > 1:
            #     ele_n = list()
            #     for i in ell:
            #         if i.rect['x'] > 0 and i.rect['y'] > 0 and \
            #                 i.rect['width'] > 0 and i.rect['height'] > 0:
            #             mask_show, ele_disable = ui_mask.run(p[0], i, i_loop * 2)
            #             if not mask_show and not ele_disable:
            #                 ele_n.append(i)
            #     if len(ele_n) == 1:
            #         return ele_n[0]
            #     if len(ele_n) > 1:
            #         for i in ell:
            #             logger.info('v:%s,tag:%s,rect:%s' % (v, str(i.tag_name), str(i.rect)))
            #         return ele_n[0]
            #     return False
        return False

    except Exception as e:
        logger.info('%s' % (e))

    return None
