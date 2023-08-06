# coding: utf-8
import logging

logger = logging.getLogger(__name__)


def elements(p):
    try:
        if p[1][1] in ['点击'] and u'\u9fa5' >= p[1][0][0] >= u'\u4e00':
            i_rp = p[1][0].replace(' ', '')
            ell_one = p[0].find_elements_by_xpath(
                "//*[contains(text(),'" + i_rp[0] + "')]/parent::*")

            er = list()
            for ele_one in ell_one:
                t_rp = ele_one.text.replace(' ', '')
                if t_rp == i_rp:
                    if ele_one.tag_name in ['a', 'span']:
                        er.insert(ele_one, 0)
                    else:
                        er.append(ele_one)
            if len(er) > 0:
                return er[0]

    except Exception as e:
        logger.info('%s,%s' % (p[1][0], e))

    return None
