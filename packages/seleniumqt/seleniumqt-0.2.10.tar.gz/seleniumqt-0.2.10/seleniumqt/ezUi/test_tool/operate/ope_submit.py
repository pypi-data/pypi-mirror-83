# coding: utf-8
import time
from util import obj_sleep
import logging
from util.object import ui_mask
import traceback

logger = logging.getLogger(__name__)


def operate(p):
    v, t_ = obj_sleep.run(p[2])
    type_ = p[1].get_attribute("type")

    if p[3] == 'None' and ('提交' == v or type_ == 'submit'):

        wd = p[0]
        has_displayed = False

        bf_all_windows = wd.window_handles

        if type_ == 'submit':
            # tf = '//input[@type="submit"]'
            try:
                tag = p[1].tag_name

                value = p[1].get_attribute("value")
                txt_del = p[1].text.replace(' ', '')

                id = p[1].get_attribute("id")
                name = p[1].get_attribute("name")

                tf = "//" + tag + '[@type="submit"'
                if name:
                    tf = tf + ' and @name="' + name + '"'
                if id:
                    tf = tf + ' and @id="' + id + '"'
                tf = tf + ']'

                lf = len(wd.find_elements_by_xpath('//form/descendant::input'))
                ls = len(wd.find_elements_by_xpath(tf))
                lb = len(wd.find_elements_by_xpath('//button'))

                for k in range(20):

                    mask_show, ele_disable = ui_mask.run(wd, p[1], k)

                    if has_displayed and (txt_del in ['登录', '下一步'] or value in ['登录', '下一步']):
                        Brk = False
                        for ic in range(6):
                            div3rt = wd.find_elements_by_xpath('/html/body/descendant::div[*]')
                            logger.info('%s%s,页面加载完成div%s' % (txt_del, value, len(div3rt)))
                            if ele_disable and len(div3rt) > 10:
                                Brk = True
                                break
                            time.sleep(1)
                        if Brk:
                            break

                        # if has_displayed:
                    logger.info('%s%s,has_displayed:%s,mask_show:%s,ele_disable:%s,len_submit_input:%s' % (
                        txt_del,
                        value,
                        has_displayed,
                        mask_show,
                        ele_disable,
                        ls))

                    if has_displayed and not mask_show and ele_disable and (
                            ls > 1 or (k > 3 and ls == 1)):
                        logger.info('break::%s,%s,%s,%s' % (lf, ls, lb, mask_show))
                        break

                    try:
                        if mask_show:
                            logger.info('boolean_ui_mask')
                            time.sleep(1)
                            continue
                        if not ele_disable:
                            try:
                                p[1].click()
                                has_displayed = True
                                logger.info('点击::%s,%s,%s,%s' % (lf, ls, lb, mask_show))
                            except:
                                logger.info('点击失败::%s,%s,%s,%s' % (lf, ls, lb, mask_show))
                                if has_displayed:
                                    break

                            time.sleep(1)

                        try:
                            lf_ = len(wd.find_elements_by_xpath('//form/descendant::input'))
                            ls_ = len(wd.find_elements_by_xpath(tf))
                            lb_ = len(wd.find_elements_by_xpath('//button'))

                            logger.info('%s,%s,%s,%s,%s,%s,%s' % (lf, lf_, ls, ls_, lb, lb_, mask_show))
                            if lf != lf_ or ls != ls_ or lb != lb_:
                                break
                        except:
                            logger.info('点击失败::对象不可用')
                    except:
                        traceback.print_exc()
            except:
                traceback.print_exc()

        if not has_displayed:
            try:
                p[1].click()
            except:
                pass
            logger.info('提交失败,点击::has_displayed::%s' % (has_displayed))
        try:
            main_windows = wd.current_window_handle
            all_windows = wd.window_handles

            if len(all_windows) > len(bf_all_windows):
                for handle in all_windows:
                    if handle != main_windows:
                        wd.switch_to.window(handle)
        except:
            traceback.print_exc()

        return True, 10
