# coding: utf-8
import logging
import time
from seleniumqt.ezUi.util.object import del_ele
import traceback

logger = logging.getLogger(__name__)


def run(dr, t, pl):
    try:
        eles = dr.find_elements_by_xpath(t)

        for index in range(len(eles)):
            xpath = ''
            t_ = t

            for i in range(30):
                # logger.info(i, xpath)
                e_on = dr.find_elements_by_xpath(t_)
                t_ = t_ + '/..'
                # logger.info(len(eles), index, len(e_on), t_)
                tn = e_on[index].tag_name

                if tn == 'body':
                    break

                xpath = '/' + tn + xpath

                for j in pl:
                    if j in xpath:
                        continue
                    else:
                        break
                else:
                    return eles[index]

    except Exception as e:
        logger.info('%s,%s,%s' % (t, str(pl), e))
        traceback.print_exc()

    return None


def right_ele_by_tag(dr, v, tag):
    pth = '//*[text()="%s："]' % v

    if '-t-' in v:
        vI_ = v.split('-t-')

        for i in range(5):
            try:

                pth_tmp = '//*[text()="%s"]' % vI_[0] + \
                          '/..' * i + \
                          '/descendant::*[text()="%s："]' % vI_[1]

                v_find = dr.find_elements_by_xpath(pth_tmp)

                if len(v_find) == 0:
                    continue
                v_find_ = del_ele.run_rect_lg(v_find)

                if len(v_find_) > 0:
                    pth = pth_tmp
                    break
            except Exception as e:
                logger.info('%s,%s' % (v, e))
                traceback.print_exc()

    ele_th = '/descendant::%s' % tag

    for i in range(5):
        try:
            t_find = dr.find_elements_by_xpath(pth + '/..' * i + ele_th)
            if len(t_find) == 0:
                continue

            logger.info(pth + '/..' * i + ele_th)
            logger.info(len(t_find))
            t_find_ = del_ele.run_rect_lg(t_find)
            logger.info(len(t_find_))

            if len(t_find_) > 0:
                return t_find_[-1]

            if len(t_find_) == 0 and len(t_find) == 1:
                input_find = dr.find_elements_by_xpath(pth + '/..' * i + '/descendant::input')
                input_find_ = del_ele.run_rect_lg(input_find)
                if len(input_find_) == 1:
                    return input_find_[0]

            # if len(t_find_) == 1:
            #     return t_find_[0]
            # elif len(t_find_) == 2:
            #     return t_find_[1]
            # else:
            #     for j in t_find_:
            #         logger.info(j.rect)
            #     return
        except:
            traceback.print_exc()

    return None


def right_input(dr, v):
    pth = '//*[text()="%s"]' % v
    ele_th = '/descendant::input'

    for i in range(5):
        try:
            tpath = pth + '/..' * i + ele_th
            t_find = dr.find_elements_by_xpath(tpath)
            if len(t_find) == 0:
                continue

            logger.info(pth + '/..' * i + ele_th)

            t_find_ = del_ele.run_rect_lg(t_find)

            if len(t_find_) == 0 and len(t_find) > 0:
                t_find_ = del_ele.clickIfNone(dr, tpath)

            if len(t_find_) == 1:
                return t_find[0]
            elif len(t_find_) == 2:
                return t_find_[1]
            else:
                for j in t_find_:
                    logger.info(j.rect)
                return
        except:
            traceback.print_exc()

    return None


def exc_input(dr, v, tag):
    try:
        t = '//*[text()="' + v + '："]/ancestor::div'

        t_find = dr.find_elements_by_xpath(t)

        if len(t_find) > 0:
            for i in range(len(t_find)):
                txt_find = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::*[text()="' + v + '："]')
                ele_find = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::' + tag)

                if len(txt_find) == 1 and len(ele_find) == 1:
                    return ele_find[0]

        title = "//*[text()='" + v + "：']"
        query = dr.find_elements_by_xpath(title)

        if len(query) > 0:
            eles_title_ = list()
            for i in range(6):
                title = title + '/..'
                eles_title = dr.find_elements_by_xpath(title + '/descendant::' + tag)
                if len(eles_title) == 1:
                    eles_title_.extend(eles_title)
                    break
                if len(eles_title) > 1:
                    return

            rt = list()
            if len(eles_title_) > 0:
                for i in query:
                    ir = i.rect
                    if ir['x'] < 1 or ir['y'] < 1 or ir['width'] < 1 or ir['height'] < 1:
                        continue

                    for j in eles_title_:
                        jr = j.rect

                        if ir['x'] + ir['width'] <= jr['x'] \
                                and ir['y'] < jr['y'] + jr['height'] / 2 < ir['y'] + ir['height'] \
                                and jr['y'] < ir['y'] + ir['height'] / 2 < jr['y'] + jr['height']:
                            rt.append(j)

            if len(rt) == 1:
                return rt[0]

            if len(rt) > 1:
                x_ = rt[0].rect['x']
                ele_x_max = rt[0]
                for i in rt[1:]:
                    if i.rect['x'] < x_:
                        x_ = i.rect['x']
                        ele_x_max = i
                return ele_x_max
    except:
        traceback.print_exc()


def exc_txt(dr, vI, ope):
    vI_ = vI.split('_txt_')

    ele_path = '//*[text()="' + vI_[0] + '" and not(@disabled="disabled")]'

    def f_ele(ep):
        try:
            return dr.find_elements_by_xpath(ep)
        except Exception as e:
            logger.info('%s' % e)
            traceback.print_exc()

    def get_path(eth):
        for i in range(9):
            e_path = ele_path + '/..' * i + '/descendant::*[text()="' + eth + '" and not(@disabled="disabled")]'
            eles = f_ele(e_path)
            if len(eles) == 1:
                return e_path
            if len(eles) > 1:
                return

    def get_ope():
        for i in range(9):
            s_path = ele_path + '/..' * i + '/descendant::'
            e_list = list()
            if '输入' in ope:
                e_list.append('input')
            elif '选择' == ope[:2]:
                e_list.append('select')
            elif '点击' == ope[:2] and str(vI).endswith('：'):
                e_list.append('input')
            else:
                e_list.append('input')
                e_list.append('li')
                e_list.append('button')
                e_list.append('span')

            for j in e_list:
                e_path = s_path + j
                eles = f_ele(e_path)
                if len(eles) == 1:
                    return eles[0]
                if len(eles) > 1:
                    return

    for i in vI_[1:]:
        et = get_path(i)
        if et:
            ele_path = et

    return get_ope()


def exc_save(dr, vI):
    vI_ = vI.split('_text_')
    va = vI_[0]
    vb = vI_[1]

    pth = '//*[text()="%s"]' % va
    ele_th = '/descendant::*[text()="%s"]' % vb

    for i in range(5):
        try:
            t_find = dr.find_elements_by_xpath(pth + '/..' * i + ele_th)
            if len(t_find) == 0:
                continue

            logger.info(pth + '/..' * i + ele_th)
            logger.info(len(t_find))
            if len(t_find) == 1:
                return t_find[0]

            if len(t_find) > 1:
                ele_find_del = del_ele.run_rect(t_find)
                for j in ele_find_del:
                    logger.info(j.rect)
                return ele_find_del[0]

        except Exception as e:
            logger.info('%s,%s' % (vI, e))
            traceback.print_exc()

    return None


def exc_right(dr, vI, opration_on):
    '''
    :param dr:
    :param vI:
    :param opration_on: 操作类型
    :return: 获取右侧控件
    '''

    msg_ = list()

    vI_ = vI[:len(vI) - 1]

    pth = '//*[text()="%s"]' % vI_
    pt_ = '//form/descendant::*[text()="%s"]' % vI_

    tag_list = list()

    if opration_on == '输入':
        tag_list.append('input')
        tag_list.append('textarea')
    elif opration_on == '选择':
        tag_list.append('select')
    else:
        tag_list.append('*')

    try:
        t_f = dr.find_elements_by_xpath(pt_)
        if len(t_f) > 0:
            pth = pt_
        else:
            t_f = dr.find_elements_by_xpath(pth)

        msg_.append(pth)

        t_f_ = del_ele.run_rect_lg(t_f)

        msg_.append(t_f_)

        right_ele = list()
        if len(t_f_) == 1:
            r = t_f_[0].rect
            x_ = r['x']
            y_ = r['y']
            hi = r['height']

            for i in range(5):
                if len(right_ele) > 0: break
                for pth_i in tag_list:
                    if len(right_ele) > 0: break
                    path_ele = pth + '/..' * i + '/descendant::' + pth_i

                    try:
                        t_find = dr.find_elements_by_xpath(path_ele)
                    except:
                        continue

                    ele_find_del = del_ele.run_rect_lg(t_find)
                    msg_.append(ele_find_del)

                    if len(ele_find_del) == 0:
                        continue

                    msg_.append(path_ele)
                    msg_.append(len(ele_find_del))

                    if len(ele_find_del) == 1 and pth_i != '*':
                        return ele_find_del[0]

                    for j in ele_find_del:
                        try:
                            r_ = j.rect
                            if pth_i == 'textarea':
                                if (y_ < r_['y'] + r_['height'] / 2 < y_ + hi
                                    or r_['y'] < y_ + hi / 2 < r_['y'] + r_['height']) \
                                        and r_['x'] > x_:
                                    right_ele.append(j)

                            elif pth_i in ['input', 'select']:
                                if y_ < r_['y'] + r_['height'] / 2 < y_ + hi \
                                        and r_['y'] < y_ + hi / 2 < r_['y'] + r_['height'] \
                                        and r_['x'] > x_:
                                    right_ele.append(j)

                            elif len(j.text) > 0:
                                if j.text not in vI_ \
                                        and vI_ not in j.text \
                                        and y_ < r_['y'] + r_['height'] / 2 < y_ + hi \
                                        and r_['y'] < y_ + hi / 2 < r_['y'] + r_['height'] \
                                        and r_['x'] > x_:
                                    right_ele.append(j)

                            if len(ele_find_del) > 0 and len(right_ele) == 0:
                                logger.info('%s<%s<%s' % (y_, r_['y'] + r_['height'] / 2, y_ + hi))
                                logger.info('%s<%s<%s' % (r_['y'], y_ + hi / 2, r_['y'] + r_['height']))
                                logger.info('%s>%s' % (r_['x'], x_))

                        except:
                            continue

            # for i in range(5):
            #     if len(right_ele) > 0: break
            #     for pth_i in ['input', 'textarea', 'select', '*']:
            #         if len(right_ele) > 0: break
            #         path_ele = pth + '/..' * i + '/descendant::' + pth_i
            #
            #         try:
            #             t_find = dr.find_elements_by_xpath(path_ele)
            #         except:
            #             continue
            #
            #         ele_find_del = del_ele.run_rect_lg(t_find)
            #
            #         if len(ele_find_del) == 0:
            #             continue
            #
            #         logger.info(path_ele)
            #         logger.info(len(ele_find_del))
            #
            #         for j in ele_find_del:
            #             try:
            #                 r_ = j.rect
            #                 if opration_on == '输入' and pth_i == 'textarea':
            #                     if (y_ < r_['y'] + r_['height'] / 2 < y_ + hi
            #                         or r_['y'] < y_ + hi / 2 < r_['y'] + r_['height']) \
            #                             and r_['x'] > x_:
            #                         right_ele.append(j)
            #
            #                 elif opration_on == '输入':
            #                     if y_ < r_['y'] + r_['height'] / 2 < y_ + hi \
            #                             and r_['y'] < y_ + hi / 2 < r_['y'] + r_['height'] \
            #                             and r_['x'] > x_:
            #                         right_ele.append(j)
            #
            #                 elif opration_on == '选择':
            #                     if y_ < r_['y'] + r_['height'] / 2 < y_ + hi \
            #                             and r_['y'] < y_ + hi / 2 < r_['y'] + r_['height'] \
            #                             and r_['x'] > x_:
            #                         right_ele.append(j)
            #
            #                 elif len(j.text) > 0 \
            #                         and j.text not in vI_ \
            #                         and vI_ not in j.text \
            #                         and y_ < r_['y'] + r_['height'] / 2 < y_ + hi \
            #                         and r_['y'] < y_ + hi / 2 < r_['y'] + r_['height'] \
            #                         and r_['x'] > x_:
            #                     right_ele.append(j)
            #
            #             except:
            #                 continue

        for msg in msg_:
            logger.info('msg::%s' % (msg))

        logger.info('len(right_ele)::%s' % (len(right_ele)))

        if len(right_ele) == 1:
            return right_ele[0]
        elif len(right_ele) > 1:
            x_min = 2000
            ele_x_min = None
            for k in right_ele:
                if k.rect['x'] < x_min:
                    x_min = k.rect['x']
                    ele_x_min = k
            return ele_x_min
        logger.info('t_f::%s,t_f_::%s' % (len(t_f), len(t_f_)))
    except:
        traceback.print_exc()

    return None


def exc_end(dr, vI):
    vI_ = vI.split('_end_')
    va = vI_[0]
    vb = vI_[1]

    pth = '//*[text()="%s"]' % va
    ele_th = '/descendant::*[text()="%s"]' % vb

    try:

        stand_path = None
        rect_ = None
        tag_ = None
        for i in range(5):
            t_find = dr.find_elements_by_xpath(pth + '/..' * i + ele_th)
            if len(t_find) == 0:
                continue

            stand_path = pth + '/..' * i + ele_th
            ele_find_del = del_ele.run_rect_lg(t_find)
            rect_ = ele_find_del[0].rect
            tag_ = ele_find_del[0].tag_name
        if rect_:
            x_max = rect_['x']
            y_max = rect_['y']
            h_max = rect_['height']

            for i in range(5):
                tag_find = dr.find_elements_by_xpath(stand_path + '/..' * i + '/descendant::' + tag_)
                if len(tag_find) == 0:
                    continue
                tag_find_ = del_ele.run_rect_lg(tag_find)
                ele_right = None
                for j in tag_find_:
                    tag_rect = j.rect
                    if h_max == tag_rect['height'] and y_max == tag_rect['y']:
                        if tag_rect['x'] > x_max:
                            x_max = tag_rect['x']
                            ele_right = j
                if ele_right:
                    return ele_right

    except Exception as e:
        logger.info('%s,%s' % (vI, e))
        traceback.print_exc()

    return None


def exc_select(dr, vI, tag):
    try:

        if '#' in vI and '##' not in vI:
            vI_ = vI.split('#')
            v = vI_[0]
            vi = vI_[1]
            if '#1' in vI:
                time.sleep(0.5)
        else:
            v = vI
            vi = 0

        t = '//*[text()="' + v + '："]/ancestor::div'

        t_find = dr.find_elements_by_xpath(t)

        if len(t_find) > 0:
            for i in range(len(t_find)):
                txt_find = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::*[text()="' + v + '："]')
                ele_findA = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::' + tag)
                ele_find_del = del_ele.run_rect(ele_findA)

                if len(txt_find) == 1 and len(ele_find_del) == 1:
                    er = ele_find_del[0].rect
                    if er['x'] < 5 or er['y'] < 5 or er['width'] < 5 or er['height'] < 5:
                        ele_find_ = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::' + tag + '/..')
                        return ele_find_[0]
                    return ele_find_del[0]

                if len(txt_find) == 1 and len(ele_find_del) == 2:
                    if '0' in vi:
                        return ele_find_del[0]
                    if '1' in vi:
                        return ele_find_del[1]

    except Exception as e:
        logger.info('%s' % e)
        traceback.print_exc()


def exc_3ds(dr, v):
    try:
        query = dr.find_elements_by_xpath("//*[text()='查询']")
        query_ = dr.find_elements_by_xpath("//*[text()='查 询']")

        if len(query) > 0 or len(query_) > 0:
            eles_title = dr.find_elements_by_xpath("//*[text()='" + v + "']/ancestor::th")

            ele = del_ele.run_max_rect(eles_title, v)

            if not ele:
                logger.info('query::%s,query_::%s,eles_title::%s'
                            % (len(query), len(query_), len(eles_title)))
                return
            # if not ele:
            #     eles_title_ = dr.find_elements_by_xpath("//th/../descendant::*[text()='" + v + "']")
            #     ele = del_ele.run_max_rect(eles_title_, v)

            eles_td = dr.find_elements_by_xpath("//td/../descendant::*")
            re_eles = list()

            x_ele = ele.rect['x']
            width_ele = ele.rect['width']
            xw2 = x_ele + width_ele

            for iet in eles_td:
                if iet:
                    try:
                        x_rect = iet.rect
                        x_iet = x_rect['x']
                        width_iet = x_rect['width']
                        if x_ele <= x_iet + width_iet / 2 <= xw2 or x_iet <= x_ele + xw2 / 2 <= width_iet:
                            re_eles.append(iet)
                    except:
                        continue
            if len(re_eles) == 0:
                logger.info('query::%s,query_::%s,eles_title::%s,eles_td::%s,re_eles::%s'
                            % (len(query), len(query_), len(eles_title), len(eles_td), len(re_eles)))

            return del_ele.run_max_rect(re_eles, None)

    except Exception as e:
        logger.info('exc_3ds,%s' % e)
        traceback.print_exc()


def exc(dr, v):
    try:
        tds = "//table/descendant::*[text()='" + v + "']"

        eles_tds = dr.find_elements_by_xpath(tds)
        if len(eles_tds) == 1:
            return eles_tds[0]

        tl = ["//*[text()='" + v + "']", "//*[text()='" + v + "：']"]

        re = list()

        for i in tl:
            eles = dr.find_elements_by_xpath(i)
            e_text = list()
            for j in eles:
                j_rect = j.rect
                if j_rect['width'] > 5 \
                        and j_rect['height'] > 5 \
                        and v in j.text:
                    re.append(j)
                    e_text.append(j.text)

            l_down_text = {}.fromkeys(e_text).keys()

            if len(l_down_text) == 1:
                e_down_ = None
                for k in re:
                    if e_down_:
                        if e_down_.rect['width'] < k.rect['width'] \
                                or e_down_.rect['height'] < k.rect['height']:
                            e_down_ = k
                    else:
                        e_down_ = k
                logger.info('%s,%s,%s' % (e_down_.tag_name, e_down_.text, e_down_.rect))

                return e_down_
            else:
                for id in re:
                    logger.info('%s-%s-%s' % (id.tag_name, id.text, id.rect))

    except Exception as e:
        logger.info(e)
        traceback.print_exc()


def eles2one(eles, text):
    if len(eles) == 1:
        return eles

    rect_all = list()

    for i in eles:
        if i.text == text:
            rect_all.append(i.rect)

    rect_cnt = None

    for i in rect_all:
        for j in rect_all:
            if i['x'] >= j['x'] \
                    and i['x'] + i['width'] <= j['x'] + j['width'] \
                    and i['y'] >= j['y'] \
                    and i['y'] + i['height'] <= j['y'] + j['height']:
                rect_cnt = j
                break
        if rect_cnt:
            break

    if rect_cnt:
        rect_rt = rect_cnt
        for m in rect_all:
            if rect_rt['x'] >= m['x'] \
                    and rect_rt['x'] + rect_rt['width'] <= m['x'] + m['width'] \
                    and rect_rt['y'] >= m['y'] \
                    and rect_rt['y'] + rect_rt['height'] <= m['y'] + m['height']:
                rect_rt = m

        return rect_rt


def table_count(dr):
    # tb_ = "//table/tbody/tr"
    tb_ = "//table"
    tb_find = dr.find_elements_by_xpath(tb_)
    ele_find_del = del_ele.run_rect(tb_find)
    return ele_find_del[0]


def th2mul(dr, t, v):
    try:
        th_ = "//*[text()='" + t + "']/ancestor-or-self::th[*]"
        th_find = dr.find_elements_by_xpath(th_)
        th_find_ = del_ele.run_rect_lg(th_find)

        if str(v).startswith('_'):
            v = v[1:]

        td_ = "//*[text()='" + v + "']/ancestor-or-self::td[*]"
        td_find = dr.find_elements_by_xpath(td_)
        td_find_ = del_ele.run_rect_lg(td_find)

        if len(td_find_) == 0:
            td_ = "//*[text()='" + v + "']/ancestor-or-self::td"
            td_find = dr.find_elements_by_xpath(td_)
            td_find_ = del_ele.run_rect_lg(td_find)

        if len(td_find_) == 0:
            pth = th_ + '/..'
            for i in range(9):
                pth = pth + '/..' * (i + 1)
                eles_get_d = dr.find_elements_by_xpath(pth + '/descendant::td')
                if len(eles_get_d) > 0:
                    th_eles_d = th_eles(th_find_, eles_get_d)
                    if th_eles_d:
                        return th_eles_d

        th_td = list()
        for i in th_find_:
            th_rect = i.rect
            for j in td_find_:
                td_rect = j.rect
                if j not in th_td \
                        and td_rect['x'] < th_rect['x'] + th_rect['width'] / 2 < td_rect['x'] + td_rect['width'] \
                        and th_rect['x'] < td_rect['x'] + td_rect['width'] / 2 < th_rect['x'] + th_rect['width']:
                    th_td.append(j)

        if len(th_td) == 1:
            return th_td[0]
        # else:
        #     for i in th_td:
        #         print(i.text, i.rect)

        logger.info('th_find_::%s,%s' % (len(th_find_), th_))
        logger.info('td_find_::%s,%s' % (len(td_find_), td_))

    except Exception as e:
        logger.info('th2td,%s' % e)
        traceback.print_exc()


def table2td(dr, v, ope):
    try:
        th_ = "//*[text()='%s']/ancestor::th[*]" % v

        th_find = dr.find_elements_by_xpath(th_)
        th_find_ = del_ele.run_rect_lg(th_find)

        if len(th_find_) == 1:

            if ope == '输入':
                a_xpath = '//div[*]/input[@type="text" and @style and not(@class)]'
                eles_get_a = dr.find_elements_by_xpath(a_xpath)
                th_eles_a = th_eles(th_find_, eles_get_a)
                if th_eles_a:
                    return th_eles_a

                b_xpath = '//div[*]/input[@type="text" and @style and @class="calendar"]'
                eles_get_b = dr.find_elements_by_xpath(b_xpath)
                th_eles_b = th_eles(th_find_, eles_get_b)

                if th_eles_b:
                    return th_eles_b

            elif ope == '点击':

                pth = th_ + '/..'
                eles_get_d = dr.find_elements_by_xpath(pth + '/descendant::td[*]')

                for i in range(9):
                    pth = pth + '/..' * (i + 1)
                    eles_get_d = dr.find_elements_by_xpath(pth + '/descendant::td[*]')
                    if len(eles_get_d) > 0:
                        break

                th_eles_d = th_eles(th_find_, eles_get_d)

                if th_eles_d:
                    return th_eles_d
            elif ope == '验证':
                pth = th_ + '/..'
                for i in range(9):
                    pth = pth + '/..' * (i + 1)
                    eles_get_d = dr.find_elements_by_xpath(pth + '/descendant::td')
                    if len(eles_get_d) > 0:
                        th_eles_d = th_eles(th_find_, eles_get_d)
                        if th_eles_d:
                            return th_eles_d

    except Exception as e:
        logger.info('th2td,%s' % e)
        traceback.print_exc()


def th_eles(th_find_, eles_get):
    if len(eles_get) > 0:
        eles_get_ = del_ele.run_rect_lg(eles_get)

        if len(eles_get_) > 0:
            eles_return = del_ele.ele_down(th_find_, eles_get_)

            if len(eles_return) == 1:
                return eles_return[0]
            elif len(eles_return) > 1:
                for td_i in eles_return:
                    logger.info(td_i.rect)
                    logger.info(td_i.text)


def th2td(dr, v):
    try:
        th_ = "//*[text()='" + v + "']/ancestor-or-self::th[*]"
        th_find = dr.find_elements_by_xpath(th_)

        logger.info('th_text,%s,%s' % (th_, len(th_find)))

        th_text_index = list()
        for i in range(len(th_find)):
            th_in_find_rect = th_find[i].rect
            if th_in_find_rect['x'] > 0 \
                    and th_in_find_rect['y'] > 0 \
                    and th_in_find_rect['width'] > 0 \
                    and th_in_find_rect['x'] > 0:
                th_text_index.append(i)

        if len(th_text_index) == 1:
            index = th_text_index[0]
        else:
            logger.info('th_text,%s,%s' % (th_, len(th_find)))
            logger.info('len(th_text_index),%s' % len(th_text_index))
            return

        th_one = th_find[index]

        th_index_ = th_ + "[" + str(index + 1) + "]"

        pre_th = dr.find_elements_by_xpath(th_index_ + "/preceding-sibling::*")

        pre_th_del = del_ele.run_rect(pre_th)

        th_index_fl_ = th_index_ + "/following::td[*][" + str(len(pre_th_del) + 1) + "]"

        td_list = dr.find_elements_by_xpath(th_index_fl_)
        td_one = del_ele.run_rect(td_list)

        if len(td_one) > 1 or len(td_one) == 0:
            logger.info('pre_th%s,td_list%s,td_in_list_del%s'
                        % (str(len(pre_th)), str(len(td_list)), str(len(td_one))))
            return
        td_in = td_one[0]

        td_in_rect = td_in.rect
        # print('TD', v, td_name, td_in_rect, th_index_fl_)
        td_name = td_in.get_attribute('data-column-field')
        if not td_name:
            return
        input_find = dr.find_elements_by_xpath("//input[@name='" + td_name + "']")
        input_find_ = dr.find_elements_by_xpath('//input[@name="' + td_name + '"]/../child::*/input')

        input_list = list()
        for input in input_find + input_find_:
            try:
                input_rect = input.rect

                if td_in_rect['x'] \
                        < input_rect['x'] + input_rect['width'] / 2 \
                        < td_in_rect['x'] + td_in_rect['width'] and \
                        td_in_rect['y'] \
                        < input_rect['y'] + input_rect['height'] / 2 \
                        < td_in_rect['y'] + td_in_rect['height']:
                    input_list.append(input)

            except:
                traceback.print_exc()

        if len(input_list) > 0:
            td_in = input_list[0]
        th_rect = th_one.rect
        td_rect = td_in.rect

        if th_rect['y'] + th_rect['height'] <= td_rect['y'] \
                and th_rect['x'] < th_rect['x'] + td_rect['width'] / 2 < th_rect['x'] + th_rect['width'] \
                and td_rect['x'] < th_rect['x'] + th_rect['width'] / 2 < td_rect['x'] + td_rect['width']:
            return td_in

    except Exception as e:
        logger.info('th2td,%s' % e)
        traceback.print_exc()


def exc_upload(dr, v, tag):
    try:
        t = '//*[text()="' + v + '："]/ancestor::div'

        t_find = dr.find_elements_by_xpath(t)

        if len(t_find) > 0:
            len_min = 1000
            for i in range(len(t_find)):
                txt_find = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::*[text()="' + v + '："]')
                ele_findA = dr.find_elements_by_xpath(t + '[' + str(i + 1) + ']/descendant::' + tag)

                ele_find_del = del_ele.run_rect(ele_findA)

                if len_min < len(ele_find_del):
                    continue

                len_min = len(ele_find_del)

                if len(txt_find) == 1 and len(ele_find_del) == 1:
                    return ele_find_del[0]

                if len(ele_find_del) > 1:

                    x_min = 1000
                    fu = None
                    for iee in ele_find_del:
                        iee.click()
                        import time
                        time.sleep(10)
                        x_ = iee.rect['x']
                        if x_ < x_min:
                            x_min = x_
                            fu = iee
                    return fu

    except Exception as e:
        logger.info('%s' % e)
        traceback.print_exc()


def down_em(p, v):
    try:
        menu = v.split('*')[0]
        em = v.split('*')[1]

        if menu == '多选项':
            es_sel = p[0].find_elements_by_xpath(
                '//*[@class="ant-select-selection-selected-value" and text()="' + em + '"]')
            if len(es_sel) > 0:
                return del_ele.run(es_sel)[0]

        if menu == '下拉列表':
            es_sel = p[0].find_elements_by_xpath(
                '//*[@class="ant-select-dropdown-menu-item" and text()="' + em + '"]')
            if len(es_sel) > 0:
                return del_ele.run(es_sel)[0]

        menu_em = p[0].find_elements_by_xpath(
            "//span[text()='" + menu + "']/../../ul/*/a/em[text()='" + em + "']")
        if len(menu_em) == 1:
            return del_ele.run(menu_em)[0]
        else:
            menu_em_ = p[0].find_elements_by_xpath(
                "//span[contains(text(),'" + menu + "')]/../../ul/*/a/em[text()='" + em + "']")
            del_ele_em = del_ele.run(menu_em_)
            if len(del_ele_em) > 0:
                return del_ele_em[0]
    except:
        traceback.print_exc()


def exc_table(dr, txt1, txt2):
    '''
    :param dr:webdriver
    :param txt1:th值
    :param txt2: 列中宝行的字段
    :return: txt1和txt2交叉的位置
    '''

    dt = list()
    dt_ = list()

    try:
        txt1_ = '//*[text()="%s"]/..' % (txt1)

        txt1_ele = dr.find_elements_by_xpath(txt1_)

        if len(txt1_ele) == 0:
            return

        for i in range(5):
            txt1_ = txt1_ + '/..' * i
            for j in str(txt2).split('-'):
                tpth = txt1_ + '/descendant::*[text()="%s"]' % (j)
                txt2_eles = dr.find_elements_by_xpath(tpth)
                if len(txt2_eles) == 0:
                    break
            else:
                break

        gode = dr.find_elements_by_xpath(txt1_ + '/descendant::*')

        if len(gode) == 0:
            return

        rect = gode[0].rect

        ele_find_txt_td_rect = None

        for i in gode:
            if i.rect['width'] == rect['width']:
                if len(dt_) > 0:
                    dt.append(dt_.copy())
                    dt_.clear()
                ele_find_txt_td_rect = None
                continue

            if not ele_find_txt_td_rect or i.rect['x'] >= int(ele_find_txt_td_rect['x']) + int(
                    ele_find_txt_td_rect['width']):
                ele_find_txt_td_rect = i.rect
                dt_.append(None)
                dt_.append(None)

            txt = i.text

            if txt and not dt_[-2] and not dt_[-1]:
                dt_[-2] = txt
                dt_[-1] = i

        dt.append(dt_)

        ele_index = dt[0].index(txt1)

        for i in dt:
            if set(str(txt2).split('-')) < set(i):
                return i[ele_index + 1]
    except:
        traceback.print_exc()
        print(dt)
        print(dt_)


if __name__ == '__main__':
    for i in range(9):
        print('//*[text()="ss"]/ancestor::th[*]/..' * i + '/descendant::' + '[*]')
