# coding: utf-8
import base64
import os
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


def screen2base64(w, d, xy):
    p = './report/temp/screen_tmp.png'

    ifpass = os.system(
        'screencapture -R %s,%s,%s,%s %s' % (d['x'], w['y'] + w['height'] - d['height'], d['width'], d['height'], p))
    if ifpass == 0:
        with open(p, "rb") as fl:
            screenshot = Image.open(fl)
            im = screenshot.convert('RGB')
            im.thumbnail((xy, xy))
            output_buffer = BytesIO()
            im.save(output_buffer, format='JPEG')
            base64_data = base64.b64encode(output_buffer.getvalue())
            t = base64_data.decode()
            return t


def wd2base64(wd, ele_rect):
    try:
        pscreen = './report/temp/screen_tmp_wd.png'

        wd.save_screenshot(pscreen)
        print('ele_rect', ele_rect)

        wrct = wd.get_window_rect()
        x = int(ele_rect['x'])
        y = int(ele_rect['y'])
        width = int(ele_rect['width'])
        height = int(ele_rect['height'])

        left = x if x > 0 else 0
        top = y if y > 0 else 0
        right = x + width if x + width > int(wrct['width']) else int(wrct['width'])
        bottom = y + height if y + height > int(wrct['height']) else int(wrct['height'])

        print('get_window_rect', left, top, right, bottom)

        with open(pscreen, "rb") as fl:
            screenshot = Image.open(fl)
            im = screenshot.crop((left, top, right, bottom)).convert('RGB')  # 对浏览器截图进行裁剪
            # im = screenshot.convert('RGB')
            output_buffer = BytesIO()
            im.save(output_buffer, format='JPEG')
            base64_data = base64.b64encode(output_buffer.getvalue())
            t = base64_data.decode()
            return t
    except Exception as e:
        logger.info('%s' % (e))


def img2base64(p, xy):
    screenshot = Image.open(BytesIO(p))
    im = screenshot.convert('RGB')
    im.thumbnail((xy, xy))
    output_buffer = BytesIO()
    im.save(output_buffer, format='JPEG')
    base64_data = base64.b64encode(output_buffer.getvalue())
    t = base64_data.decode()
    return t
