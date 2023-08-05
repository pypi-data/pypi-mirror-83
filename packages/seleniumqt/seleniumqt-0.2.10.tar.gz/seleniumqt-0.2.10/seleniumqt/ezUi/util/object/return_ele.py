#coding: utf-8
import logging

logger = logging.getLogger(__name__)


def run(dr, rect, if_down):
    try:
        path = '//table/tbody'

        for i in range(9):
            path = path + '/child::*'
            ed = dr.find_elements_by_xpath(path)

            if ed and ed[0].tag_name == 'td':
                break
        else:
            return None

        eles = dr.find_elements_by_xpath(path)

        mul_obj = list()

        x = rect['x']
        y = rect['y']
        w = rect['width']
        h = rect['height']

        if if_down:
            for ele in eles:
                ele_rect = ele.rect
                x_ = ele_rect['x']
                y_ = ele_rect['y']
                w_ = ele_rect['width']
                h_ = ele_rect['height']

                if h_ < 12 or w_ < 12:
                    continue

                # logger.info('###', x, y, w, h)
                # logger.info('###', x_, y_, w_, h_)

                _x = x - x_ if x > x_ else x_ - x
                if _x > w / 2 + w_ / 2:
                    continue

                xm = x + w / 2
                xm_ = x_ + w_ / 2

                if y_ >= y + h:
                    if x < xm_ < x + w:
                        mul_obj.append(ele)
                    elif x_ < xm < x_ + w_:
                        mul_obj.append(ele)

            # logger.info('mul_obj', len(mul_obj))

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

                # logger.info('*' * 88, eq_obj.rect)

                return [eq_obj]
            else:
                logger.info('%s%s%s%s%s' % (if_down, x, y, w, h))

                for ele in eles:
                    logger.info('return_ele:%s,%s' % (ele.text, ele.rect))

        else:
            for ele in eles:
                ele_rect = ele.rect

                '''
                /table/tbody/tr[6]/td[1]/p/span
                /table/tbody/tr[6]/td[2]
                '''
                # logger.info('return_ele', ele.text, ele.rect)

                if ele_rect['height'] < 12 or ele_rect['width'] < 12:
                    continue

                yh_ = ele_rect['y'] + ele_rect['height'] / 2
                if y < yh_ < y + h and ele_rect['x'] >= x + w:
                    mul_obj.append(ele)

            if len(mul_obj) == 1:
                return mul_obj
            elif len(mul_obj) > 0:

                eq_obj = mul_obj[0]
                x_eq = mul_obj[0].rect['x']
                y_eq = mul_obj[0].rect['y']
                for i_mul in mul_obj:
                    if i_mul.rect['y'] != y_eq:
                        continue

                    if i_mul.rect['x'] < x_eq:
                        x_eq = i_mul.rect['x']
                        eq_obj = i_mul

                return [eq_obj]
            else:
                logger.info('%s%s%s%s%s' % (if_down, x, y, w, h))
                for ele in eles:
                    logger.info('return_ele:%s,%s' % (ele.text, ele.rect))

    except Exception as e:
        logger.info('rect:%s,%s' % (rect, if_down, e))

    return None
