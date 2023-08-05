# coding: utf-8

import logging
import traceback

logger = logging.getLogger(__name__)


def verify(p):
    try:
        try:
            txt_value = p[1].text
            if not txt_value:
                txt_value = p[1].get_attribute("value")
        except:
            traceback.print_exc()
            return

        if txt_value:
            v = str(txt_value)
            if is_number(str(p[2])) or is_number(v):
                if is_number(str(p[2])) and is_number(v):
                    t = float(p[2].replace(',', '')) - float(v.replace(',', ''))
                    if 0.001 > t >= 0:
                        info = ('[INFO:]***测试通过*** ', str(p[2]), v)
                        return True, info
                    print(0.001 > t)
                    print(t >= 0)
                print(str(p[2]), is_number(str(p[2])))
                print(v, is_number(v))

                logger.info('%s,%s' % (p[2].replace(',', ''), v.replace(',', '')))

            elif str(p[2]).replace(' ', '') == v.replace(' ', ''):
                info = ('[INFO:]***测试通过*** ', str(p[2]), v)
                return True, info
            elif '|' in str(p[2]):
                if v in str(p[2]).split('|'):
                    info = ('[INFO:]***测试通过*** ', str(p[2]), v)
                    return True, info
            logger.info('%s,%s' % (str(p[2]), v))

            info = ('[INFO:]***测试失败*** 关系:等于,预期结果:', str(p[2]), '实际结果', str(v))
            return False, info
        elif txt_value == '' and str(p[2]) == '_':
            info = ('[INFO:]***测试通过*** ', str(p[2]), txt_value)
            return True, info
    except:
        traceback.print_exc()


def is_number(number):
    num = number.replace(',', '')
    flt = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-', ',']
    for i in num[1:]:
        if i not in flt[:-1]:
            return False
    else:
        if num[0] in flt:
            return True
    return False
