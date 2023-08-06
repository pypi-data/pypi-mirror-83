# coding: utf-8
from seleniumqt.ezUi.util.object import del_ele
import logging
from selenium.webdriver import ActionChains
import traceback

logger = logging.getLogger(__name__)


def run(dr, ele, k):
    mask_show = False
    ele_disable = False

    try:

        is_enabled = ele.is_enabled()
        is_displayed = ele.is_displayed()

        if k > 3:
            logger.info('is_enabled:%s,is_displayed:%s' % (str(is_enabled), str(is_displayed)))

        if not is_enabled:
            logger.info('控件不可点击！！！')
        if not is_displayed:
            logger.info('无控件显示！！！')
        if not is_enabled or not is_displayed:
            ele_disable = True
    except:
        ele_disable = True
        logger.info('error::ele,is_enabled,is_displayed')

    try:
        t = dr.find_elements_by_xpath('//*[@class="ui-mask"]')
        if len(t) > 0:
            for i in t:
                try:
                    if i.is_displayed():
                        mask_show = True
                        break
                except:
                    logger.info('*error,ui-mask')
    except:
        logger.info('error::ele,@class="ui-mask"')
        ele_disable = True

    return mask_show, ele_disable


def un_mask_lg(dr, ell_):
    ell = del_ele.run_rect_lg(ell_)
    ele_n = list()
    ele_rect = list()

    for ei in ell:
        mask_show, ele_disable = run(dr, ei, 1)
        if not mask_show and not ele_disable and ei.rect not in ele_rect:
            ele_n.append(ei)
            ele_rect.append(ei.rect)
    return ele_n


def len_ele(wd, xpth):
    try:
        t = wd.find_elements_by_xpath(xpth)
        return t
    except:
        traceback.print_exc()
    return []


def click_wd(wd):
    len_ul = len_ele(wd, '//ul[@class="dl-hide-list ks-hidden"]')
    for i in len_ul:
        logger.info('关闭功能菜单......%s' % len(len_ul))
        try:
            if i.is_displayed():
                # import time
                ActionChains(wd).move_to_element(i).perform()
                ActionChains(wd).move_to_element_with_offset(i, 200, 100).perform()
                ActionChains(wd).move_by_offset(0, 0)
                try:
                    ActionChains(wd).move_to_element(i).perform()
                    ActionChains(wd).move_to_element_with_offset(i, 400, 200).perform()
                    ActionChains(wd).move_by_offset(0, 0)
                    ActionChains(wd).move_to_element(i).perform()
                    ActionChains(wd).move_to_element_with_offset(i, 600, 300).perform()
                    ActionChains(wd).move_by_offset(0, 0)
                except:
                    logger.info('功能菜单已关闭......')

        except:
            traceback.print_exc()


def tab_item_close(wd):
    try:
        wd.switch_to.alert.accept()
    except:
        pass

    item_pth = "//*[@class='bui-nav-tab-item']/descendant::*[@class='tab-item-close']"
    wd.switch_to.default_content()
    gf = wd.find_elements_by_xpath(item_pth)
    if len(gf) > 0:

        for i in gf:
            if 15 > i.rect['width'] > 10:
                logger.info('关闭多余iframe::%s,非当前的Iframe总数:%s' % (item_pth, len(gf)))
                i.click()
        click_wd(wd)
