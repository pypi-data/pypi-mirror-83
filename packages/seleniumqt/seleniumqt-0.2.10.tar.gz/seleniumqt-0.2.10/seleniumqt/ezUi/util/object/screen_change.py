from PIL import ImageChops, Image
import traceback
import time
import os
from seleniumqt.ezUi import run_config


def img_flag(fn):
    image_one = Image.open(fn)

    x, y = image_one.size

    x_list = list()
    y_list = list()

    for i in range(x):
        t = image_one.getpixel((i, int(y / 2)))
        x_list.append(t)

    for j in range(y):
        t = image_one.getpixel((int(x / 2), j))
        y_list.append(t)

    return x_list, y_list


def screenshot_img(wd, fname):
    fn = run_config.report_path + '/Img/' + fname
    if os.path.exists(fn):
        os.remove(fn)

    d = wd.get_window_rect()
    os.system('screencapture -R %s,%s,%s,%s %s' % (d['x'], d['y'], d['width'], d['height'], fn))


def wd_img(wd, fname):
    fn = run_config.report_path + '/Img/wd_' + fname

    if os.path.exists(fn):
        os.remove(fn)

    wd.get_screenshot_as_file(fn)
    time.sleep(0.5)


def wd_change(wd):
    wd_img(wd, 'one.png')
    image_one = Image.open(run_config.report_path + '/Img/wd_one.png')

    for i in range(60):
        try:
            time.sleep(1)
            wd_img(wd, 'two.png')
            image_two = Image.open(run_config.report_path + '/Img/wd_two.png')

            diff = ImageChops.difference(image_one, image_two)

            gb = diff.getbbox()
            if gb:
                image_one = image_two
                continue
            else:
                return True
        except:
            traceback.print_exc()


def box_change(wd):
    x_one, y_one = img_flag(run_config.report_path + '/Img/one.png')

    for i in range(60):
        try:
            screenshot_img(wd, 'two.png')
            x_two, y_two = img_flag(run_config.report_path + '/Img/two.png')
            if x_one != x_two and y_one != y_two:
                time.sleep(0.5)
                return
        except:
            traceback.print_exc()
