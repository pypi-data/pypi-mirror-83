# coding: utf-8
import logging
import time
import traceback
from util.object import del_ele

logger = logging.getLogger(__name__)


def operate(p):
    try:
        wd = p[0]
        ele = p[1]
        if '输入' == p[2]:
            for i in range(30):
                try:
                    ele.get_attribute("type")
                except:
                    return
                try:
                    input_ele = wd.find_elements_by_xpath('//form/descendant::input')
                    input_ele_del = del_ele.run_rect_lg(input_ele)
                except:
                    continue

                if len(input_ele_del) > 0:

                    button_ele = wd.find_elements_by_xpath(
                        '//button[contains(text(),"查") and contains(text(),"询")]')
                    button_ele_del = del_ele.run_rect_lg(button_ele)

                    if len(button_ele_del) > 0:
                        th_ele = wd.find_elements_by_xpath('//table/descendant::th')
                        th_ele_del = del_ele.run_rect_lg(th_ele)

                        if len(th_ele_del) == 0:
                            time.sleep(1)
                            if i % 4 == 3 and len(button_ele_del) == 1:
                                button_ele_del[0].click()
                            continue

                    submit_ele = wd.find_elements_by_xpath('//form/descendant::*[@type="submit"]')
                    submit_ele_del = del_ele.run_rect_lg(submit_ele)

                    if len(submit_ele_del) > 0 and ele.is_displayed():
                        break
                    tijiao_ele = wd.find_elements_by_xpath(
                        '//form/descendant::*[contains(text(),"提") and contains(text(),"交")]')
                    tijiao_ele_del = del_ele.run_rect_lg(tijiao_ele)

                    if len(tijiao_ele_del) > 0 and ele.is_displayed():
                        break

                if i > 3:
                    try:
                        logger.info('%s,%s,%s' % (i, ele.rect, ele.tag_name))
                    except:
                        continue

                if ele.is_displayed():
                    break
            # try:
            #     ele.clear()
            # except:
            #     traceback.print_exc()

            if '_' != p[3]:
                try:
                    send_keys(wd, ele, p[3])
                except:
                    traceback.print_exc()
                    return
                logon_ele = wd.find_elements_by_xpath(
                    '//button/descendant-or-self::*[contains(text(),"登") and contains(text(),"录")]')

                if len(logon_ele) > 0:
                    value_ = ele.get_attribute("value")
                    logger.info('登录输入::%s,%s,%s' % (p[3], value_, value_ == p[3]))
                    if value_ != p[3]:
                        # ele.clear()
                        # time.sleep(1)
                        send_keys(wd, ele, p[3])
                        time.sleep(1)

            return True, 1
    except:
        traceback.print_exc()


def send_keys(wd, e, v):
    if ':' in v and len(str(v).split(':')) == 3:
        id = e.get_attribute('id')
        js = None

        if id:
            js = 'document.getElementById("%s").removeAttribute("readonly");' % (id)
        else:
            name = e.get_attribute('name')
            if name:
                js = 'document.getElementsByName("%s").removeAttribute("readonly");' % (name)

        if js:
            wd.execute_script(js)
            e.clear()
            e.send_keys(v)
    else:

        try:
            e.clear()
        except:
            traceback.print_exc()

        e.send_keys(v)

    '''
    确定: //button[text()="确定"]
    '''
