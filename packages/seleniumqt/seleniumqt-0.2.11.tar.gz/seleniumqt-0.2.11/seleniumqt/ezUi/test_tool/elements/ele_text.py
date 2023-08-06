# coding: utf-8
import logging
import time
import traceback
from seleniumqt.ezUi.util import obj_sleep
from seleniumqt.ezUi.util.object import del_ele

logger = logging.getLogger(__name__)


def elements(p):
    wd = p[0]
    opr = p[1][1]
    text_value = p[1][0]

    if not opr == '验证' and u'\u9fa5' >= text_value[0] >= u'\u4e00' and not str(text_value).startswith('//'):
        try:
            v, t_ = obj_sleep.run(text_value)

            ell_ = wd.find_elements_by_xpath("//*[text()='" + v + "']")

            if len(ell_) > 0 and ell_[0].tag_name == 'span' and ell_[0].get_attribute("class") == '':
                ell_ = wd.find_elements_by_xpath("//*[text()='" + v + "']/parent::*")

            ell = del_ele.run_rect_lg(ell_)

            if len(ell) == 1:
                return ell[0]

            eg = list()

            for i in ell:
                logger.info('%s,%s,%s' % (i.tag_name, i.text, v))
                if i.tag_name == 'em' and i.text == '查询':
                    continue
                elif v in str(i.text):
                    eg.append(i)

            if len(eg) == 1:
                time.sleep(t_)
                return eg[0]
            else:

                logger.info('__原有控件::%s,%s,%s' % (len(ell_), len(eg), len(ell)))

                ell_all = wd.find_elements_by_xpath("//*[text()='" + v + "']")
                ell_all_del = del_ele.run_rect(ell_all)

                ell_table = wd.find_elements_by_xpath("//table/descendant::*[text()='" + v + "']")

                ell_table_tmp = del_ele.run_del_same_rect(ell_all_del, ell_table)
                ell_table_ = del_ele.run_rect_lg(ell_table_tmp)

                if len(ell_table_) == 1:
                    return ell_table_[0]

                ell_form = wd.find_elements_by_xpath("//form/descendant::*[text()='" + v + "']")

                ell_form_tmp = del_ele.run_del_same_rect(ell_table_, ell_form)
                ell_form_ = del_ele.run_rect_lg(ell_form_tmp)

                if len(ell_form_) == 1:
                    return ell_form_[0]

                logger.info('ell_form::%s,%s,ell_table::%s,%s' % (
                    len(ell_form), len(ell_form_), len(ell_table), len(ell_table_)))

                ele_n = list()
                for i in ell:
                    if i.rect['width'] > 0 and i.rect['height'] > 0:

                        logger.info('v:%s,tag:%s,rect:%s' % (v, str(i.tag_name), str(i.rect)))
                        if i.tag_name == 'em' and i.text == '查询':
                            continue
                        elif i.tag_name in ['a', 'span', 'button']:
                            ele_n.insert(0, i)
                        else:
                            ele_n.append(i)

                if len(ele_n) == 1:
                    time.sleep(t_)
                    return ele_n[0]
                if len(ele_n) > 1:

                    t0 = ele_n[0]
                    t1 = ele_n[1]
                    t_1 = ele_n[-1]

                    if t0.rect['x'] == t1.rect['x'] == t_1.rect['x'] \
                            and t0.rect['width'] == t1.rect['width'] == t_1.rect['width'] \
                            and t0.rect['height'] == t1.rect['height'] == t_1.rect['height']:
                        tf = t0 if t0.rect['y'] < t1.rect['y'] else t1
                        tr = tf if tf.rect['y'] < t_1.rect['y'] else t_1

                        return tr
                    else:
                        return t0

        except:
            traceback.print_exc()

    return None
