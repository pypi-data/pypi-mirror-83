#coding: utf-8
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
from util import obj_sleep

logger = logging.getLogger(__name__)


def operate(p):
    v, t_ = obj_sleep.run(p[2])
    if '鼠标悬停' == v:
        for i in range(10):
            if i > 3: logger.info(i)

            if p[1].is_displayed():
                try:
                    time.sleep(1)
                    ActionChains(p[0]).move_to_element(p[1]).move_by_offset(5, 5).perform()
                    time.sleep(1)
                    return True, 10
                except Exception as e:
                    logger.info('Exception', p[1].rect, e)
                    time.sleep(1)
        else:
            logger.info('[INFO:]click ele not ok', p[1].is_displayed())
