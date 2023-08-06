#coding: utf-8
#  run to case
import logging

logger = logging.getLogger(__name__)


def run(rpt_step_list):
    rpt = rpt_step_list
    rpt.append({'step': ['url', 'test_end']})
    rpt_index = 0
    rpt_sys_dict = dict()
    step_list = list()
    step_fail = False

    try:
        for isl in rpt:

            if type(isl) is not dict:
                continue

            if isl['step'][0] == 'url' and len(step_list) > 0:
                rpt_index = rpt_index + 1
                rpt_sys_dict[rpt_index] = dict()
                rpt_sys_dict[rpt_index]['sys'] = step_list[0]['step']
                # 追加测试步骤
                rpt_sys_dict[rpt_index]['step_list'] = step_list[1:]
                if 'error_info' in isl.keys():
                    rpt_sys_dict[rpt_index]['error_info'] = isl['error_info']

                rpt_sys_dict[rpt_index]['ifpass'] = not step_fail

                step_list.clear()
                step_fail = False

            step_list.append(isl)

            if 'ifpass' in isl.keys() and isl['ifpass'] == False:
                step_fail = True

    except Exception as e:
        logger.info(rpt_step_list)
        logger.info(e)

    return rpt_sys_dict
