# coding: utf-8
import logging
import time
import traceback

logger = logging.getLogger(__name__)


def verify(p):
    try:
        if str(p[2]) == 'wait_Exit':
            has_show = False
            for i in range(30):

                time.sleep(0.5)
                try:
                    if p[1] and p[1].is_enabled() and p[1].is_displayed():
                        logger.info('控件存在')
                        has_show = True
                    elif has_show:
                        info = ('[INFO:]***测试通过*** 关系:控件检测,预期结果:', '控件不存在', '实际结果', '控件不存在')
                        break
                except:
                    if has_show:
                        info = ('[INFO:]***测试通过*** 关系:控件检测,预期结果:', '控件不存在', '实际结果', '控件不存在')
                        break
            else:
                info = ('[INFO:]***执行失败*** 关系:控件检测,预期结果:', '控件不存在', '实际结果', '控件存在')
                return False, info
            return True, info

    except:
        traceback.print_exc()
        info = ('[INFO:]***执行失败*** 关系:控件检测,预期结果:', '控件不存在', '实际结果', '未执行')
        return True, info
