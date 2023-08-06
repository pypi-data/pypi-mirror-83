#coding: utf-8
from seleniumqt.ezUi.util import v_alpha
import time

def run(txt):
    ts = 0

    if '___' in txt:
        _text = txt.split('___')[0].replace('_', ' ')
        tt = txt.split('___')[1]
        time.sleep(int(tt))
    elif '---' in txt:
        _text = txt.split('---')[0].replace('_', ' ')
        ts = txt.split('---')[1]
    else:
        _text = txt

    _en, _dg, _sp, _zh, _pu = v_alpha.run(_text)
    if _zh > 0 or _en == 0:
        _text = _text.replace('_', ' ')

    return _text, int(ts)
