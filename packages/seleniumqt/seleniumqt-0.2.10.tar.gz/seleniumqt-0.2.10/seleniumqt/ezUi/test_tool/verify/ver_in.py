# coding: utf-8

import logging

logger = logging.getLogger(__name__)


def verify(p):
    try:
        if str(p[2]).startswith('_'):
            txt_value = p[1].text
            if not txt_value:
                txt_value = p[1].get_attribute("value")

            if txt_value and str(p[2])[1:] in str(txt_value):
                info = ('[INFO:]***测试通过*** 关系:包含,预期结果:', str(p[2])[1:], '实际结果', str(txt_value))
                return True, info

            if not txt_value and len(str(p[2])) == 1:
                info = ('[INFO:]***测试通过*** 关系:包含,预期结果:', str(p[2])[1:], '实际结果', str(p[1].text))
                return True, info

            logger.info('%s,%s' % (str(p[2]), txt_value))

            info = ('[INFO:]***测试失败*** 关系:包含,预期结果:', str(p[2]), '实际结果', str(txt_value))
            return False, info
    except Exception as e:
        logger.info(e)
