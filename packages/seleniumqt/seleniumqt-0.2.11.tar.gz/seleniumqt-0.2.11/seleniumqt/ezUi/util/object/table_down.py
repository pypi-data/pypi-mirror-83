# coding: utf-8
import logging
from seleniumqt.ezUi.util.object import get_ele, get_path, return_ele, down_right

logger = logging.getLogger(__name__)


def run(dr, text):
    try:

        xpath_form_span = get_path.exit_xpath(dr, text, ['table', 'thead'], ['form'])
        if xpath_form_span:
            down, right = down_right.run(dr, xpath_form_span)
            if down:
                return [down[0]]

        xpath_form_span = get_path.exit_xpath(dr, text, ['table', 'tbody'], ['form'])

        if xpath_form_span:
            down, right = down_right.run(dr, xpath_form_span)
            if right:
                return [right[0]]

        end_text = "//*[text()='" + text + "']"
        if_thead = get_ele.run(dr, end_text, ['table', 'thead'])
        if if_thead:
            ele_r = return_ele.run(dr, if_thead.rect, True)
            if ele_r:
                return ele_r

        if_tbody = get_ele.run(dr, end_text, ['table', 'tbody'])

        if if_tbody:
            ele_r = return_ele.run(dr, if_tbody.rect, False)
            if ele_r:
                return ele_r

        if '：' in text:
            t = "//label[text()='" + text + "']"
            es = dr.find_elements_by_xpath(t)
            if len(es) == 1:
                xpath = get_path.run(dr, t)

                xpath_span = xpath[:-5] + 'span'
                es_span = dr.find_elements_by_xpath(xpath_span)
                if len(es_span) == 1:
                    return es_span
            return

        t = "//thead/descendant::*[text()='" + text + "']"

        es = dr.find_elements_by_xpath(t)
        logger.info(t)
        logger.info(len(es))
        if len(es) == 1:
            xpath = get_path.run(dr, t)
            if 'table/thead/tr/th[' in xpath:
                xp_index = xpath.split('table/thead/tr/th[')[1]
                xp_index = xp_index.split(']')[0]

                nodes = dr.find_elements_by_xpath('//table/tbody/tr/td[' + xp_index + ']')

                if len(nodes) == 1:
                    return nodes
                else:
                    node_get = list()
                    nodes_ = dr.find_elements_by_xpath('//table/tbody/tr[*]/td[' + xp_index + ']')
                    for i_nodes_ in nodes_:
                        if len(i_nodes_.text) > 0:
                            node_get.append(i_nodes_)
                    if len(node_get) == 1:
                        return node_get

                    if len(node_get) > 1:
                        logger.info("查询条件太多，请设置一条查询%s", len(nodes_))

                    logger.info('<span>2页签文字对象获取数量::%s', len(nodes_))

                    '''
                    父（Parent）：每个元素以及属性都有一个父。
                    子（Children）：元素节点可有零个、一个或多个子。
                    同胞（Sibling）：拥有相同的父的节点。
                    先辈（Ancestor）：某节点的父、父的父，等等。
                    后代（Descendant）：某个节点的子，子的子，等等。
                    '''
        logger.info('<span>1页签文字对象获取数量::%s', len(es))

        t_ = "//*[text()='" + text + "']"
        es_ = dr.find_elements_by_xpath(t_)
        mul_obj = list()
        xp_str_l_rep = list()

        for ies_ in es_:
            if ies_.text != text:
                continue

            ies_rect = ies_.rect

            x = ies_rect['x']
            y = ies_rect['y']
            w = ies_rect['width']
            h = ies_rect['height']

            xpath_ = get_path.run(dr, t_)
            xp_str_l = list()

            if 'table' in xpath_:
                xp_table = '//table/tbody/*/td[*]/child::*'
                xp_str_l.append(xp_table)
            elif 'html' in xpath_:
                xp_html = xpath_.replace('[', '|[').replace(']', ']|')
                xp_l = xp_html.split('|')
                for il in range(int(len(xp_l) / 2)):
                    xp_l_tmp = xp_l.copy()
                    xp_l_tmp[il * 2 + 1] = '[*]'

                    xp_str_l.append(''.join(xp_l_tmp))

            xp_str_l_rep = list(set(xp_str_l))
            for xp_i in xp_str_l_rep:
                es_xp_ = dr.find_elements_by_xpath(xp_i)
                for i_es_xp_ in es_xp_:
                    rect_ = i_es_xp_.rect

                    if rect_['height'] < 12 or rect_['width'] < 12:
                        continue

                    xm_ = rect_['x'] + rect_['width'] / 2
                    if x < xm_ < x + w and rect_['y'] >= y + h:
                        mul_obj.append(i_es_xp_)
        if len(mul_obj) == 1:
            return mul_obj
        elif len(mul_obj) > 1:
            eq_obj = mul_obj[0]
            x_eq = mul_obj[0].rect['x']
            y_eq = mul_obj[0].rect['y']
            for i_mul in mul_obj:
                if i_mul.rect['x'] != x_eq:
                    continue

                if i_mul.rect['y'] < y_eq:
                    y_eq = i_mul.rect['y']
                    eq_obj = i_mul
            return [eq_obj]

        zt_ = "//label[text()='" + text + "']"
        es_zt_ = dr.find_elements_by_xpath(zt_)
        if len(es_zt_) == 0:
            zt_ = "//label[text()='" + text + "：']"
            es_zt_ = dr.find_elements_by_xpath(zt_)
            # if len(es_zt_) == 0:
            #     zt_ = "//label[contains(text(),'" + text + "')]"
            #     es_zt_ = dr.find_elements_by_xpath(zt_)

        if len(es_zt_) > 0:
            xpath_label = get_path.run(dr, zt_)

            if xpath_label \
                    and xpath_label.endswith('label'):

                ret_span = str(xpath_label).replace('label', 'span')
                ele_span = dr.find_elements_by_xpath(ret_span)
                if len(ele_span) == 1:
                    return ele_span

        if text == '复制浮窗':
            es_top = dr.find_elements_by_xpath(
                '//*[@class="ant-popover-content"]/descendant::input')
            if len(es_top) > 0:
                return es_top

        for ie in es_:
            logger.info('查找文本::%s 坐标::%s', ie.text, ie.rect)

        for ix in xp_str_l_rep:
            logger.info('已搜索控件属性::%s', ix)

        for im in mul_obj:
            logger.info('已获取 控件文本::%s,控件坐标::%s', im.text, im.rect)

        for ix in xp_str_l_rep:
            ixe = dr.find_elements_by_xpath(ix)
            for ixei in ixe:
                logger.info('未获取 控件文本::%s,控件坐标::%s', ixei.text, ixei.rect)

    except Exception as e:
        logger.info(text, e)
