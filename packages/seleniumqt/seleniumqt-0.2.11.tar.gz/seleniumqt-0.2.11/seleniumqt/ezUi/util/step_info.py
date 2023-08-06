# coding: utf-8
from seleniumqt.ezUi.util import compress_image
import logging
import traceback

logger = logging.getLogger(__name__)


def run(t, so, exit_code, screen_d, screen_w, err_info):
    try:
        rpt_step_dict = dict()
        rpt_step_dict['step'] = so

        if so[0] != 'url':
            rpt_step_dict['ifpass'] = True if t else False
            rpt_step_dict['info'] = '执行成功' if t else (
                '执行失败' if exit_code == 0 else '重试失败')
            rpt_step_dict['img'] = \
                compress_image.screen2base64(screen_w, screen_d, 128 if t else 64)  # 128 if t else 512
            if not t:
                rpt_step_dict['error_info'] = err_info
                logger.info('error step_run')

        return rpt_step_dict
    except:
        traceback.print_exc()


def runWD(t, so, exit_code, err_info):
    try:
        rpt_step_dict = dict()
        rpt_step_dict['step'] = so

        if so[0] != 'url':
            rpt_step_dict['ifpass'] = True if t else False
            rpt_step_dict['info'] = '执行成功' if t else (
                '执行失败' if exit_code == 0 else '重试失败')
            # rpt_step_dict['img'] = compress_image.wd2base64(wd,ele_rect)
            if not t:
                rpt_step_dict['error_info'] = err_info
                logger.info('error runWD step_run::%s')

        return rpt_step_dict
    except:
        traceback.print_exc()


def exRun(step_, screen_w, screen_d, e0):
    try:
        rpt_step_dict = dict()
        rpt_step_dict['step'] = step_
        rpt_step_dict['img'] = compress_image.screen2base64(screen_w, screen_d, 64)  # 512
        rpt_step_dict['error_info'] = ('[INFO:]***测试Exception***', '', '', e0)
        rpt_step_dict['ifpass'] = False
        rpt_step_dict['info'] = '异常报错系统截图'

        return rpt_step_dict
    except:
        traceback.print_exc()


def exWdRun(step_, wd, e0):
    try:
        screen_d = wd.find_element_by_tag_name('body').rect
        screen_w = wd.get_window_rect()

        rpt_step_dict = dict()
        rpt_step_dict['step'] = step_
        rpt_step_dict['img'] = compress_image.screen2base64(screen_w, screen_d, 64)  # 512
        rpt_step_dict['error_info'] = ('[INFO:]***测试Exception***', '', '', e0)
        rpt_step_dict['ifpass'] = False
        rpt_step_dict['info'] = '异常报错系统截图'
        return rpt_step_dict
    except:
        traceback.print_exc()


def pamRun(pam):
    try:
        keys = list()
        for k, v in pam.items():
            logger.info('key::%s,value::%s' % (k, v))
            if len(str(v)) < 100:
                keys.append(str(k) + '==' + str(v))
            else:
                keys.append(str(k) + '==' + str(v)[:10])

        rpt_step_dict = dict()
        rpt_step_dict['step'] = ['', '', '', '当前参数内容']
        rpt_step_dict['img'] = None
        rpt_step_dict['error_info'] = ('执行成功', '参数', '值', keys)
        rpt_step_dict['ifpass'] = True
        rpt_step_dict['info'] = '执行成功'

        return rpt_step_dict
    except:
        traceback.print_exc()
