# coding: utf-8
import time
from seleniumqt.ezUi.util import select_count, form_right
import logging
import traceback
from seleniumqt.ezUi.util.object import del_ele
from seleniumqt.ezUi.util import obj_sleep, v_alpha
from seleniumqt.ezUi.util.object import get_path, table_down, get_ele, down_right

logger = logging.getLogger(__name__)


def elements(p):
    try:
        wd = p[0]
        text_value = p[1][0]
        opration_on = p[1][1]
        exc_value = p[1][2]

        _en, _dg, _sp, _zh, _pu = v_alpha.run(text_value)
        if _dg > 1 and (_zh == 0 and _en == 0):
            logger.info(_dg)
            return

        if str(text_value).startswith('/'):
            return

        v, t_ = obj_sleep.run(text_value)

        if str(v) == 'TABLE_COUNT':
            tb_ = "//table"
            try:
                tb_find = wd.find_elements_by_xpath(tb_)
                if len(tb_find) > 0:
                    return tb_find[0]
            except:
                traceback.print_exc()

        if str(v).startswith('TD'):
            return get_ele.table2td(wd, str(v).replace('TD', ''), opration_on)

        if str(v).startswith('TT'):
            if opration_on == '验证':
                t_th2mul = get_ele.th2mul(wd, str(v).replace('TT', ''), exc_value)
                if t_th2mul:
                    logger.info('th2mul')
                    return t_th2mul

            return get_ele.th2td(wd, str(v).replace('TT', ''))

        if '_txt_' in text_value:
            return get_ele.exc_txt(wd, text_value, opration_on)

        if '_text_' in text_value and opration_on[:2] in ['验证', '点击']:
            return get_ele.exc_save(wd, text_value)

        if '_end_' in text_value:
            return get_ele.exc_end(wd, text_value)

        if '||' in v:
            return select_count.run(wd, v)

        if str(text_value).endswith('L'):
            return get_ele.exc_right(wd, text_value, opration_on)

        if opration_on in ['选择', '点击选择'] and _zh > 1 >= _pu:

            select_ele = get_ele.right_ele_by_tag(wd, v, 'select')
            if select_ele:
                logger.info('right_ele_by_tag%s' % (select_ele.rect))
                return select_ele

            select_ele_ = get_ele.exc_select(wd, v, 'select')
            if select_ele_:
                logger.info('exc_select')
                return select_ele_

        if opration_on in ['输入']:
            if _zh > 1:
                input_ele = get_ele.right_ele_by_tag(wd, v, 'input')
                if input_ele:
                    logger.info('right_ele_by_tag::%s' % (input_ele.rect))
                    return input_ele

                if not input_ele:
                    input_sdk = get_ele.right_input(wd, v)
                    if input_sdk:
                        logger.info('right_input')
                        return input_sdk

                if 1 >= _pu:
                    input_ele_ = get_ele.exc_input(wd, v, 'input')
                    if input_ele_:
                        logger.info('exc_input')
                        return input_ele_

        if opration_on in ['点击'] and '*' in v and _zh + _pu == len(text_value):
            return get_ele.down_em(p, v)

        if opration_on in ['点击上传']:
            input_ele = get_ele.exc_upload(wd, v, 'input')
            logger.info('exc_upload')
            return input_ele

        # if opration_on in ['输入', '选择'] and u'\u9fa5' >= v[0] >= u'\u4e00':
        #     return form_right.run(p, v, t_)

        elif opration_on in ['验证', '取参', '鼠标悬停']:
            if '@' in v and opration_on in ['取参', '验证', '鼠标悬停']:
                if '-' in v:
                    v1, v2 = v.split('@')
                    return get_ele.exc_table(wd, v1, v2)
                else:
                    v1, v2 = v.split('@')
                    return down_right.exc_(wd, v1, v2)

            if opration_on in ['验证', '取参']:

                table_ele = get_ele.exc_3ds(wd, v)
                if table_ele:
                    logger.info('exc_3ds')
                    return table_ele

            if opration_on in ['验证']:

                xpath_ele = get_ele.exc(wd, v)
                if xpath_ele:
                    d, r = down_right.exc(wd, xpath_ele)
                    if r:
                        return r

                xpath_form_span = get_path.exit_xpath(wd, v, ['form'], ['table'])

                if xpath_form_span:
                    t = form_right.run(p, v, t_)
                    if t:
                        return t

                return

            objects = table_down.run(wd, v)

            if objects and len(objects) == 1:
                time.sleep(t_)
                return del_ele.run(objects)[0]

    except:
        traceback.print_exc()
