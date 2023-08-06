# coding: utf-8
import re

import logging

logger = logging.getLogger(__name__)


def verify(p):
    try:
        if '==' in p[2] and p[1].text:
            b = str(p[2][:p[2].index('==')])
            b_ = str(p[2][p[2].index('==') + 2:])
            t = str(p[1].text)
            t_ = '"' + b + '":"(.*)"' if '":"' in t else b + ':(.*)'
            rlt = re.findall(t_, t.replace(' ', ''))
            for i in rlt:
                if str(i).startswith(b_):
                    info = ('[INFO:]***测试通过*** 关系:JSON字段,预期结果:', str(b_), '实际结果', str(i))
                    return True, info

                if '||' in b_:
                    if str(i) + '||' in b_ or '||' + str(i) in b_:
                        info = ('[INFO:]***测试通过*** 关系:JSON字段,预期结果:', str(b_), '实际结果', str(i))
                        return True, info

            info = ('[INFO:]***测试失败***关系:JSON字段,预期结果:', str(p[2]), '实际结果', str(p[1].text))
            return False, info
    except Exception as e:
        logger.info(e)
