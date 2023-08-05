# coding: utf-8
from util.object import del_ele

import logging
import time

logger = logging.getLogger(__name__)


def verify(p):
    if str(p[2]).startswith('tr_'):
        try:
            len_tr = int(str(p[2]).replace('tr_', ''))
            len_find = -1

            for i in range(20):
                tb_find = p[0].find_elements_by_xpath("//table/tbody/tr")
                ele_find_del = del_ele.run_rect_lg(tb_find)
                len_find = len(ele_find_del)

                if len_find == 0 and len_tr > 0:
                    time.sleep(1)
                    continue

                if len_tr == len_find:
                    info = ('[INFO:]***测试通过*** 关系:查询记录数量相同,预期结果:', str(len_tr), '实际结果', str(len_find))
                    return True, info

                if len_find>0 and len_tr==0:
                    info = ('[INFO:]***测试通过*** 关系:查询记录数量相同,预期结果:', str(len_tr), '实际结果', str(len_find))
                    return True, info

                logger.info('查询记录数量相同%s,%s' % (str(len_tr), str(len_find)))

            info = ('[INFO:]***测试失败*** 关系:查询记录数量不同,预期结果:', str(len_tr), '实际结果', str(len_find))
            return False, info

        except Exception as e:
            logger.info(e)
