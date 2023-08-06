#coding: utf-8
from configparser import ConfigParser
from seleniumqt.ezUi import run_config

def init():
    cfg = ConfigParser()
    pth = run_config.report_path + '/conf/db_ip.ini'

    cfg.read(pth)
    cfg.set('host', 'connect', '')
    cfg.set('host', 'disconnect', '')
    cfg.write(open(pth, 'w'))


def r():
    cfg = ConfigParser()
    pth = run_config.report_path + '/conf/db_ip.ini'

    cfg.read(pth)
    cn = cfg.get('host', 'connect')
    dcn = cfg.get('host', 'disconnect')
    return cn, dcn


def w(connect_ip, if_connect):
    cfg = ConfigParser()
    pth = run_config.report_path + '/conf/db_ip.ini'

    cfg.read(pth)

    if if_connect:
        cn = cfg.get('host', 'connect')
        cn_ = cn + '|' if cn else ''
        cfg.set('host', 'connect', cn_ + connect_ip)
    else:
        dcn = cfg.get('host', 'disconnect')
        dcn_ = dcn + '|' if dcn else ''
        cfg.set('host', 'disconnect', dcn_ + connect_ip)

    cfg.write(open(pth, 'w'))


if __name__ == '__main__':
    init()
    g = r()
    w('1.1.1.1', True)
    w('1.2.1.1', False)
    g_ = r()
    print(g, g_)
