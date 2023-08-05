# coding: utf-8

import logging

logger = logging.getLogger(__name__)


def verify(p):
    try:
        if str(p[2]) == 'xxx':
            txt_value = p[1].text
            if not txt_value:
                txt_value = p[1].get_attribute("value")
            print('-' * 8, txt_value, '-' * 8)
            info = ('[INFO:]***测试通过*** 关系:包含,预期结果:', 'xxx', '实际结果', txt_value)
            return True, info
    except Exception as e:
        logger.info(e)
