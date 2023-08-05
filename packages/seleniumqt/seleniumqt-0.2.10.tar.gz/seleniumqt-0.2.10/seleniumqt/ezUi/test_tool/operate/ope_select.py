# coding: utf-8
from selenium.webdriver.support.select import Select
import logging
import time
import traceback
from util.object import ui_mask

logger = logging.getLogger(__name__)


def operate(p):
    if '选择' == p[2]:
        ele = p[1]
        v = str(p[3])
        logger.info('%s,%s,%s' % (v, ele.rect, ele.tag_name))

        for k in range(30):
            mask_show, ele_disable = ui_mask.run(p[0], ele, k)
            if mask_show or ele_disable:
                continue

            if ele.tag_name == 'select':
                try:
                    s = Select(ele)
                    for so in s.options:
                        text = so.text
                        if str(text).replace(' ', '') == v:
                            s.select_by_visible_text(text)
                            if text == s.first_selected_option.text:
                                return True, 0
                        value = so.get_attribute("value")
                        if str(value).replace(' ', '') == v:
                            s.select_by_value(value)
                            if v == s.first_selected_option.get_attribute("value"):
                                return True, 0
                except:
                    traceback.print_exc()
            else:
                try:
                    for i in range(30):
                        ele.click()
                        time.sleep(0.1)
                        t = p[0].find_elements_by_xpath('//li[text()="' + v + '"]')
                        logger.info('select_div::%s' % (len(t)))
                        if len(t) > 0:
                            for j in t:
                                try:
                                    j.click()
                                except:
                                    traceback.print_exc()
                            return True, 1
                except:
                    traceback.print_exc()

                time.sleep(1)
