# coding: utf-8
import logging
import time
import os
import traceback

logger = logging.getLogger(__name__)


def operate(p):
    if '上传文件' == p[2]:
        try:
            wd = p[0]
            ele = p[1]

            dir_path = os.path.dirname(os.path.abspath(__file__)) + '/../../conf/data_file/' + p[3]
            logger.info('上传文件路径::' + dir_path)
            ele.send_keys(dir_path)

            for i in range(30):
                '''[@class="anticon anticon-spin anticon-loading"]'''
                ele_class_ = wd.find_elements_by_xpath('//i[contains(@class,"anticon-loading")]')  # 控件加载图标消失判断
                if len(ele_class_) == 0:
                    break
                time.sleep(1)
            return True, 1
        except:
            traceback.print_exc()
