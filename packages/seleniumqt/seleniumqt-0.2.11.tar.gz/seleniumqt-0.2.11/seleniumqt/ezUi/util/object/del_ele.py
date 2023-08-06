# coding: utf-8
import logging
import traceback

logger = logging.getLogger(__name__)


def run(eles_):
    return run_rect(run_text(eles_))


def run_text(eles_):
    ell = list()

    for i in eles_:
        try:
            if len(i.text) > 0:
                ell.append(i)
            elif i.tag_name in ['input']:
                ell.append(i)
        except:
            continue
    if len(ell) == 0:
        return eles_
    return ell


def run_rect_lg(eles_):
    ell = list()
    if type(eles_) is list:

        for i in eles_:
            try:
                if i.rect['x'] > 0 and i.rect['y'] > 0 and i.rect['width'] > 5 and i.rect['height'] > 5:
                    ell.append(i)
            except:
                continue

        if len(eles_) > 0 and len(ell) == 0:
            logger.info('eles_::%s' % (len(eles_)))
            for i in eles_:
                try:
                    logger.info(i.rect)
                except:
                    continue

    return ell


def clickIfNone(wd, tpath):
    for i in range(6):
        try:
            t_f = wd.find_elements_by_xpath(tpath + '/..' * i)
            t_find__ = run_rect_lg(t_f)
            for j in t_find__:
                if j.is_displayed():
                    j.click()
                    t_find = wd.find_elements_by_xpath(tpath)
                    t_find_r = run_rect_lg(t_find)
                    if len(t_find_r) > 0:
                        return t_find_r
        except:
            traceback.print_exc()


def ele_down(ele_up, eles):
    eles_down = list()
    th_rect = ele_up[0].rect
    for td_i in eles:
        td_rect = td_i.rect
        if td_i not in eles_down \
                and td_rect['x'] < td_rect['x'] + th_rect['width'] / 2 < td_rect['x'] + td_rect['width'] \
                and th_rect['x'] < td_rect['x'] + td_rect['width'] / 2 < th_rect['x'] + th_rect['width']:
            eles_down.append(td_i)

    return eles_down


def run_del_same_rect(eles_, es):
    ell = list()
    try:
        if len(eles_) == 1:
            return eles_

        es_rect = list()

        for j in es:
            es_rect.append(j.rect)

        for i in eles_:
            if i.rect not in es_rect:
                ell.append(i)
    except:
        traceback.print_exc()
    return ell


def run_rect(eles_):
    ell = list()
    try:
        # if len(eles_) == 1:
        #     return eles_

        for i in eles_:
            try:
                rect = i.rect
                is_displayed_ = i.is_displayed()
            except:
                continue

            if is_displayed_ and rect['x'] > 0 and rect['y'] > 0 and rect['width'] > 5 and rect['height'] > 5:
                ell.append(i)

        if len(ell) == 0 and len(eles_) > 0:
            rect_std = None
            ele = None
            for i in eles_:

                try:
                    rect = i.rect
                except:
                    continue

                if not rect_std:
                    rect_std = rect
                    ele = i
                elif rect['width'] >= rect_std['width'] \
                        and rect['height'] >= rect_std['height']:
                    rect_std = rect
                    ele = i
            ell.append(ele)
    except:
        traceback.print_exc()
    return ell


def run_max_rect(eles_, v):
    er = None
    if type(eles_) is list:
        if len(eles_) == 1:
            return eles_[0]
        w_max = 0
        for i in eles_:
            try:
                if (v and v in i.text) or not v:
                    t = i.rect
                    if t['width'] > w_max and t['height'] > 0:
                        logger.info(t)
                        w_max = t['width']
                        er = i
            except:
                traceback.print_exc()

        if not er:
            for i in eles_:
                try:
                    logger.info('ERROR::%s,%s,%s' % (v, i.text, i.rect))
                except:
                    traceback.print_exc()
    return er
