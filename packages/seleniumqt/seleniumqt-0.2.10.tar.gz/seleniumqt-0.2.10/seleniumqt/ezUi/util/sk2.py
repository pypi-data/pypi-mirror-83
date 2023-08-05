# coding: utf-8
# scroll to view
import logging

logger = logging.getLogger(__name__)


def gte(d, p):
    try:

        wind = d.get_window_size()
        obj = p.rect

        d.execute_script("arguments[0].scrollIntoView(false);", p)

        if obj['y'] > wind['height'] * 2 / 3:
            y_ = wind['height'] - obj['y'] + 200
            d.execute_script("window.scrollBy(0,%s)" % (y_))
        if obj['y'] < wind['height'] / 3:
            y_ = wind['height'] - obj['y'] + 200
            d.execute_script("window.scrollBy(0,-%s)" % (y_))
        if obj['x'] > wind['width'] * 4 / 5:
            x_ = wind['width'] - obj['x'] + 100
            d.execute_script("window.scrollBy(%s,0)" % (x_))
        if obj['x'] < wind['width'] / 5:
            x_ = wind['width'] - obj['x'] + 100
            d.execute_script("window.scrollBy(-%s,0)" % (x_))
    except:
        logger.info('控件无法显示')

    return True
