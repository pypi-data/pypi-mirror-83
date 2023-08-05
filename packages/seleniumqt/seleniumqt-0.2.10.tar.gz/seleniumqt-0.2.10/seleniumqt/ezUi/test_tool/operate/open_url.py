# coding: utf-8
import logging

import time
import traceback

logger = logging.getLogger(__name__)


def operate(p):
    if 'url' == p[1]:
        wd = p[0]
        
        handles = wd.window_handles
        if (len(handles)) > 1:
            for ih in handles[:-1]:
                wd.switch_to.window(ih)  # 切换到最新打开的窗口
                wd.close()
            wd.switch_to.window(handles[-1])

        for i in range(3):
            try:
                wd.delete_all_cookies()
                wd.get(p[2])
                logger.info('[*Step*]%s%s' % (i, p[2]))
                # time.sleep(1)

                for j in range(10):
                    input_eles = wd.find_elements_by_tag_name('input')
                    time.sleep(1)
                    logger.info('输入框个数::%s' % len(input_eles))
                    if len(input_eles) > 1:
                        return True
            except:
                traceback.print_exc()
                print(p[2])
                # time.sleep(120)
