# coding: utf-8
import logging
import traceback
from seleniumqt.ezUi.util.object import del_ele
from seleniumqt.ezUi.util.object import ui_mask
from seleniumqt.ezUi.util import highLightElement, elements

logger = logging.getLogger(__name__)


def run(wd, s0, ele_bf):
    try:
        ui_mask.tab_item_close(wd)
        wd.switch_to.default_content()
        if '查询' == s0[3] and '点击' == s0[1]:
            ui_mask.click_wd(wd)
        tg = elements.run([wd, s0])
        if tg:
            return True, screen_ele(wd, tg, s0, ele_bf)

        hds = wd.window_handles

        if len(hds) > 1:
            for i0 in range(3):
                for ih in hds:
                    try:
                        wd.switch_to.window(ih)
                        tg = elements.run([wd, s0])
                        if tg:
                            return True, screen_ele(wd, tg, s0, ele_bf)
                    except:
                        traceback.print_exc()
                        continue

        for i1 in range(3):
            handles = wd.window_handles
            for ih in handles:
                try:
                    wd.switch_to.window(ih)
                    if len(handles) > 1:
                        tg = elements.run([wd, s0])
                        if tg:
                            return True, screen_ele(wd, tg, s0, ele_bf)
                except:
                    traceback.print_exc()
                    continue

                try:
                    tab_iframe = wd.find_elements_by_xpath("//*[@class='dl-tab-item']/descendant::iframe")
                except:
                    return

                for i in del_ele.run(tab_iframe):
                    try:
                        wd.switch_to.frame(i)
                        tg = elements.run([wd, s0])
                        if tg:
                            return True, screen_ele(wd, tg, s0, ele_bf)
                    except:
                        traceback.print_exc()
                try:
                    ifz = wd.find_elements_by_tag_name('iframe')
                except:
                    return

                for iz in ifz:
                    try:
                        if iz.rect['width'] < 1:
                            continue
                        wd.switch_to.frame(iz)
                        tg = elements.run([wd, s0])
                        if tg:
                            return True, screen_ele(wd, tg, s0, ele_bf)
                    except:
                        traceback.print_exc()

                wd.switch_to.default_content()
                tg = elements.run([wd, s0])
                if tg:
                    return True, screen_ele(wd, tg, s0, ele_bf)

                wd.switch_to.parent_frame()
                tg = elements.run([wd, s0])
                if tg:
                    return True, screen_ele(wd, tg, s0, ele_bf)

                xele = wd.find_elements_by_xpath(
                    '//li[@class="bui-nav-tab-item"]/descendant::s[@class="tab-item-close"]')
                for xclose in xele:
                    try:
                        logger.info('关闭运营后台tab::switch_to.frame:%s' % str(s0[0]))
                        xclose.click()
                    except:
                        traceback.print_exc()
        else:
            wd.switch_to.default_content()
            return False, None
    except:
        traceback.print_exc()
        logger.info("[Exception:]funct:9_7%s" % str(s0))
    wd.switch_to.default_content()
    return False, None


def screen_ele(wd, tg, s0, ele_bf):
    if s0[1] in ['取参']:
        highLightElement.run(wd, tg, 2)

    t = tg
    if type(tg) is list and ele_bf:
        hl = 0
        er = ele_bf.rect
        for i in tg:
            print('_____')

            r = i.rect
            if er['x'] == r['x'] \
                    and er['height'] == r['height'] \
                    and er['width'] == r['width']:
                hh = int(r['y']) - int(er['y'])
                if hl == 0 or hl > hh:
                    hl = hh
                    t = i
    return t
