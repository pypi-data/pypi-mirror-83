# coding: utf-8
import os
import logging
from seleniumqt.ezUi import run_config

logger = logging.getLogger(__name__)


def run():

    dir_ = [run_config.report_path+'/',
            run_config.report_path + '/temp/',
            run_config.report_path + '/email/']

    for i in dir_:
        if not os.path.exists(i):
            os.makedirs(i)
        else:
            for j in os.listdir(i):
                if j.endswith('html') or j.endswith('png'):
                    os.remove(i + j)

    logger.info('移除后 [./report] 目录下有文件：%s' % os.listdir('./report'))
