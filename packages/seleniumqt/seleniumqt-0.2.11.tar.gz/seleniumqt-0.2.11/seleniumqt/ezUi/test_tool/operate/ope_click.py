# coding: utf-8
import logging
import time
from selenium.webdriver import ActionChains
import traceback
from util import obj_sleep
from util.object import del_ele

logger = logging.getLogger(__name__)


def operate(p):
    v, t_ = obj_sleep.run(p[2])

    if str(v).startswith('点击'):
        type_ = p[1].get_attribute("type")
        txt = p[1].text
        wd = p[0]

        tag_name = p[1].tag_name

        if_query = txt.replace(' ', '')
        logger.info('if_query%s' % (if_query))
        if len(if_query) == 2 and if_query == '查询':
            for loop_run in range(6):
                try:
                    for tw in range(2):
                        try:
                            p[1].click()
                        except:
                            logger.info('ActionChains|move_to_element|click::%s' % (if_query))
                            ActionChains(wd).move_to_element(p[1]).perform()
                            ActionChains(wd).click(p[1]).perform()

                        table_thead = '//table/thead/tr/child::*'
                        table_thead_before = wd.find_elements_by_xpath(table_thead)
                        if len(table_thead_before) == 0:
                            logger.info('%s_ERROR_YZF' % (table_thead))
                            time.sleep(0.5)
                            continue

                        table_tbody = '//table/tbody/*/*'
                        tbody_before_query_ele = wd.find_elements_by_xpath(table_tbody)
                        tbody_before_query = del_ele.run(tbody_before_query_ele)

                        if len(tbody_before_query) == 0:
                            logger.info('%s_ERROR_YZF' % (table_tbody))
                            time.sleep(0.5)
                            continue

                        text_before_query = list()
                        for i_tbody_before_query in tbody_before_query:
                            try:
                                if i_tbody_before_query.text:
                                    text_before_query.append(i_tbody_before_query.text)
                            except:
                                continue

                        for ir in range(5):
                            tbody_after_query_ele = wd.find_elements_by_xpath(table_tbody)
                            tbody_after_query = del_ele.run(tbody_after_query_ele)

                            if len(tbody_before_query) != len(tbody_after_query):
                                # 如果查询后查询table内容变化,结束查询
                                logger.info('循环次数%s,查询前::%s,查询后::%s' % (ir
                                                                        , len(tbody_before_query)
                                                                        , len(tbody_after_query)))
                                return True, 0

                            if len(tbody_after_query) > 2 and ir > 0:
                                for i_ele in tbody_after_query:
                                    if len(i_ele.text) > 0:
                                        # 有多查询内容,并且是非首次查询，结束查询
                                        logger.info('循环次数%s,查询文本::%s' % (ir, i_ele.text))
                                        return True, 0

                            for i_tbody_after_query in tbody_after_query:
                                try:
                                    if i_tbody_after_query.text \
                                            and i_tbody_after_query.text \
                                            not in text_before_query:
                                        # 如果出现新文字内容,结束查询
                                        logger.info('循环次数%s,查询文本::%s' % (ir, i_tbody_after_query.text))
                                        return True, 1
                                except:
                                    continue

                            try:
                                logger.info('循环次数%s,查询前::%s,查询后::%s' % (ir
                                                                        , len(tbody_before_query)
                                                                        , len(tbody_after_query)))
                                p[1].click()
                                time.sleep(0.2)
                                continue
                            except:
                                time.sleep(0.2)
                        else:
                            return True, 1

                except Exception as e:
                    traceback.print_exc()
                    if loop_run < 2: continue

                    try:
                        logger.info('等待...%s' % e)
                        logger.info(tag_name)
                        logger.info(txt)
                        logger.info(v)
                    except:
                        time.sleep(1)
                        traceback.print_exc()
                    return True, 0
            else:
                logger.info('[INFO:]click ele not ok')
            logger.info('%s,%s' % (v, t_))

        if type_ != 'submit':
            has_displayed = False
            has_click = False

            form_input = wd.find_elements_by_xpath('//form/descendant::input')
            del_form_input = del_ele.run_rect_lg(form_input)

            for i in range(5):
                try:
                    for tw in range(30):

                        if tag_name == 'button' and txt.replace(' ', '') == '登录':
                            form_input_login = wd.find_elements_by_xpath('//form/descendant::input')
                            del_form_input_login = del_ele.run_rect_lg(form_input_login)

                            if len(del_form_input_login) == 2:
                                for login_input in del_form_input_login:
                                    if login_input.rect['width'] > 1:
                                        value_login = login_input.get_attribute("value")
                                        if len(value_login) == 0:
                                            logger.info('value_login::%s' % value_login)
                                            return

                        try:
                            rect = p[1].rect
                            if int(rect['width']) == 0:
                                logger.info('未显示控件::%s' % (str(rect)))
                                return
                        except:
                            if i == 1: traceback.print_exc()
                            if has_click: return True, 0
                            break
                        try:
                            is_displayed = p[1].is_displayed()
                            is_enabled = p[1].is_enabled()
                        except:
                            continue

                        try:
                            expanded = p[1].get_attribute('aria-expanded')
                        except:
                            expanded = None

                        if is_displayed:
                            has_displayed = True

                        if has_displayed and not is_displayed:
                            return True, 0

                        try:
                            if expanded == 'true':
                                return True, 0

                            logger.info('debug::%s,%s' % (tw, rect))

                            if tw % 5 < 4 or (rect and rect['width'] == 0):
                                logger.info('run__click::%s' % (str(rect)))
                                try:
                                    p[1].click()
                                except:
                                    continue
                            else:
                                logger.info('ActionChains__click::%s' % (str(rect)))
                                ActionChains(wd).move_to_element(p[1]).perform()
                                ActionChains(wd).click(p[1]).perform()
                            has_click = True
                        except:
                            logger.info('loop::%s,expanded::%s,is_enabled::%s,is_displayed::%s,has_click::%s'
                                        % (i, expanded, is_enabled, is_displayed, has_click))

                            if not has_click:
                                traceback.print_exc()
                                continue

                        if len(del_form_input) > 0 \
                                and tag_name in ['button', 'input', 'span'] \
                                and txt.replace(' ', '') in ['登录', '提交', '查看更多']:
                            form_input_ = wd.find_elements_by_xpath('//form/descendant::input')
                            del_form_input_ = del_ele.run_rect_lg(form_input_)

                            if len(del_form_input_) == len(del_form_input):
                                continue

                        return True, 0
                except:
                    traceback.print_exc()
                    # time.sleep(t_)
                    return True, 0

            else:
                logger.info('[INFO:]点击click ele not ok%s' % p[1].is_displayed())
            logger.info('点击%s,%s' % (v, t_))
