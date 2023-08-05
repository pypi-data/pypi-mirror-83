# coding: utf-8
from seleniumqt.ezUi.util import v_alpha
from seleniumqt.ezUi.util.object import del_ele
import logging
import time
import traceback

logger = logging.getLogger(__name__)


def elements(p):
    _en, _dg, _sp, _zh, _pu = v_alpha.run(p[1][0])
    if _en == 0:
        return

    if str(p[1][0]).startswith('/'):
        for i in range(30):
            try:
                try:
                    ele_xpath = p[0].find_elements_by_xpath(p[1][0])
                except:
                    return
                if len(ele_xpath) == 0:
                    ifz = p[0].find_elements_by_tag_name('iframe')
                    logger.info('frame总数::%s,xpath::%s,控件数量%s,xpath::%s' % (len(ifz), p[1][0], len(ele_xpath), p[1][0]))
                    return

                ell = del_ele.run(ele_xpath)

                logger.info('xpath::%s,控件数量%s' % (p[1][0], len(ell)))

                if i > 3: logger.info(str(p[1][0]) + str(len(ell)))
                if len(ell) == 0:
                    logger.info(len(ele_xpath))
                    continue
                if len(ell) == 1:
                    # if p[1][1] == '验证':
                    #     logger.info(ell[0].get_attribute('innerHTML'))
                    #     if not ell[0].get_attribute('innerHTML'):
                    #         continue

                    return ell[0]
                else:
                    t0 = ell[0]
                    t1 = ell[1]
                    t_1 = ell[-1]
                    logger.info('--%s,%s' % (t0.text, t0.rect))
                    logger.info('--%s,%s' % (t1.text, t1.rect))
                    logger.info('--%s,%s' % (t_1.text, t_1.rect))
                    if t0.rect['x'] == t1.rect['x'] == t_1.rect['x'] \
                            and t0.rect['width'] == t1.rect['width'] == t_1.rect['width'] \
                            and t0.rect['height'] == t1.rect['height'] == t_1.rect['height']:
                        tf = t0 if t0.rect['y'] < t1.rect['y'] else t1

                        tr = tf if tf.rect['y'] < t_1.rect['y'] else t_1

                        return tr
            except:
                traceback.print_exc()
