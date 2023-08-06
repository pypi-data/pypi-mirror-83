# coding: utf-8
import configparser
import logging
from seleniumqt.ezUi import run_config

logger = logging.getLogger(__name__)


def init():
    cfgpath = run_config.report_path + "/date/exec.ini"
    conf = configparser.ConfigParser()
    conf.write(open(cfgpath, 'w'))


def write_case(s, k, v):
    cfgpath = run_config.report_path + "/date/exec.ini"
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding="utf-8")
    sections = conf.sections()
    if s not in sections:
        conf.add_section(s)
        conf.write(open(cfgpath, "r+"))
        conf.read(cfgpath, encoding="utf-8")
    conf.set(s, k, v)
    conf.write(open(cfgpath, "r+"))


def init_function_report():
    cfgpath = run_config.report_path + "/date/function_report.ini"
    conf = configparser.ConfigParser()
    conf.write(open(cfgpath, 'w'))


def write_function_report(s, k, v):
    cfgpath = run_config.report_path + "/date/function_report.ini"
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding="utf-8")
    sections = conf.sections()
    if s not in sections:
        conf.add_section(s)
        conf.write(open(cfgpath, "r+"))
        conf.read(cfgpath, encoding="utf-8")
    conf.set(s, k, v)
    conf.write(open(cfgpath, "r+"))


def read_ini():
    f = open(run_config.report_path + '/date/exec.ini', 'r', encoding='utf-8')

    all_pass = list()
    b2b_pass = list()
    b2b_fail = list()

    b2c_pass = list()
    b2c_fail = list()

    for line in f.readlines():
        t = line.replace('\n', '').replace('\r', '')
        if len(t) > 9:
            if 'b2b' in str(t):
                if '= 0' in t:
                    b2b_fail.append(t + ' (验证未通过)')
                else:
                    b2b_pass.append(t)

            if 'b2c' in str(t):
                if '= 0' in t:
                    b2c_fail.append(t + ' (验证未通过)')
                else:
                    b2c_pass.append(t)

            if '***' in str(t):
                all_pass.append(t)

    f.close()

    if b2b_pass or b2b_fail or b2c_pass or b2c_fail:
        logger.info('查询周期|业务类型|通道名 = 交易数量 ')

        logger.info('* ' * 30)
        for i in all_pass:
            logger.info(i)
        logger.info('* ' * 30)
        for i in b2b_pass:
            logger.info(i)
        for i in b2b_fail:
            logger.info(i)
        logger.info('* ' * 30)
        for i in b2c_pass:
            logger.info(i)
        for i in b2c_fail:
            logger.info(i)
        logger.info('* ' * 30)


if __name__ == '__main__':
    init()
    write_case('q', 'e', 'w')
    write_case('q', 't', 'd')
