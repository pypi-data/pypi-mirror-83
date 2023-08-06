#coding: utf-8
import string


def run(str):
    _en = _dg = _sp = _zh = _pu = 0

    for s in str:
        # 英文
        if s in string.ascii_letters:
            _en += 1
        # 数字
        elif s.isdigit():
            _dg += 1
        # 空格
        elif s.isspace():
            _sp += 1
        # 中文
        elif s.isalpha():
            _zh += 1
        # 特殊字符
        else:
            _pu += 1

    '''找出字符串中的英文、数字、空格、中文、标点符号个数'''
    return _en, _dg, _sp, _zh, _pu
