# coding: utf-8
import logging

logger = logging.getLogger(__name__)


def run(dr, pth):
    e_down_ = None
    e_right_ = None

    try:
        e_down_text = list()
        e_right_text = list()
        e_down = list()
        e_right = list()

        ed = dr.find_element_by_xpath(remove_child(pth))

        ed_rect = ed.rect

        x = ed_rect['x']
        y = ed_rect['y']
        w = ed_rect['width']
        h = ed_rect['height']

        cld_path = '//table//tbody//*'

        ed = dr.find_elements_by_xpath(cld_path)

        for i in ed:
            i_rect = i.rect

            x_ = i_rect['x']
            y_ = i_rect['y']
            w_ = i_rect['width']
            h_ = i_rect['height']

            if w_ < 10 or h_ < 10:
                continue

            if x_ >= x and y_ >= y + h and x_ + w_ <= x + w:
                if y + h + h_ > y_:
                    e_down.append(i)
                    e_down_text.append(i.text)

            if y_ >= y and x_ >= x + w and y_ + h_ <= y + h:
                if x + w + w_ > x_:
                    e_right.append(i)
                    e_right_text.append(i.text)

        l_down_text = {}.fromkeys(e_down_text).keys()
        l_right_text = {}.fromkeys(e_right_text).keys()

        if len(l_down_text) == 1:
            e_down_ = e_down
        else:
            for id in e_down:
                print(id.tag_name, id.text, id.rect)

        if len(l_right_text) == 1:
            e_right_ = e_right
            for id in e_right:
                print(id.tag_name, id.text, id.rect)

    except Exception as e:
        print(e)

    return e_down_, e_right_


def exc(dr, ele):
    e_down_ = None
    e_right_ = None

    try:
        e_down_text = list()
        e_right_text = list()
        e_down = list()
        e_right = list()

        ed_rect = ele.rect

        x = ed_rect['x']
        y = ed_rect['y']
        w = ed_rect['width']
        h = ed_rect['height']

        cld_path = '//table//tbody//*'

        ed = dr.find_elements_by_xpath(cld_path)

        for i in ed:
            i_rect = i.rect

            x_ = i_rect['x']
            y_ = i_rect['y']
            w_ = i_rect['width']
            h_ = i_rect['height']

            if w_ < 10 or h_ < 10:
                continue

            if x_ >= x and y_ >= y + h and x_ + w_ <= x + w:
                if y + h + h_ > y_:
                    e_down.append(i)
                    e_down_text.append(i.text)

            if y_ >= y and x_ >= x + w and y_ + h_ <= y + h:
                if x + w + w_ > x_:
                    e_right.append(i)
                    e_right_text.append(i.text)

        l_down_text = {}.fromkeys(e_down_text).keys()
        l_right_text = {}.fromkeys(e_right_text).keys()

        if len(l_down_text) == 1:
            e_down_ = e_down
        else:
            for id in e_down:
                print(id.tag_name, id.text, id.rect)

        if len(l_right_text) == 1:
            e_right_ = e_right
            for id in e_right:
                print(id.tag_name, id.text, id.rect)

    except Exception as e:
        print(e)

    return e_down_, e_right_


def exc_(dr, txt1, txt2):
    t1_ = "//table[*]/descendant::*[text()='" + txt1 + "']/ancestor::th"
    t2_ = "//table[*]/descendant::*[text()='" + txt2 + "']/ancestor-or-self::td/../td"

    ele_txt1_list = dr.find_elements_by_xpath(t1_)
    x_txt1 = 0
    w_txt1 = 0

    for i in ele_txt1_list:
        if i.text == txt1 and i.rect['x'] > x_txt1 and i.rect['width'] > w_txt1:
            x_txt1 = i.rect['x']
            w_txt1 = i.rect['width']

    txt2_eles = dr.find_elements_by_xpath(t2_)

    for i in txt2_eles:
        if i.rect['x'] == x_txt1 and i.rect['width'] == w_txt1:
            return i
        if len(ele_txt1_list) > 0 and len(txt2_eles) > 0 and i.rect['x'] == x_txt1:
            print(i.text, len(ele_txt1_list), len(txt2_eles), i.rect)

    t1_ = "//*[text()='" + txt1 + "']"
    t2_ = "//*[text()='" + txt2 + "']"

    ele_txt1_list__ = dr.find_elements_by_xpath(t1_)

    for i in ele_txt1_list__:
        if i.text == txt1 and i.rect['x'] > 10 and i.rect['width'] > 10:
            txt2_eles__ = dr.find_elements_by_xpath(t2_ + '/following-sibling::*')
            for j in txt2_eles__:
                if j.text == txt2 \
                        and j.rect['x'] == i.rect['x'] \
                        and j.rect['width'] == i.rect['width']:
                    return j

    for i in range(5):
        t = dr.find_elements_by_xpath(t1_ + '/..')
        if len(t) > 0 and t[0].text != txt1 and txt1 in t[0].text:
            break
        t1_ = t1_ + '/..'
    else:
        return

    for i in range(5):
        t = dr.find_elements_by_xpath(t2_ + '/..')
        if len(t) > 0 and t[0].text != txt2 and txt2 in t[0].text:
            break
        t2_ = t2_ + '/..'
    else:
        return

    tr = dr.find_elements_by_xpath(t2_ + '/following-sibling::*')

    ele1 = dr.find_elements_by_xpath(t1_)

    x = ele1[0].rect['x']
    width = ele1[0].rect['width']

    for i in tr:
        if i.rect['x'] == x and i.rect['width'] == width:
            return i


def remove_child(pth):
    d = ['th', 'td', 'tr']

    p_l = str(pth).split('/')
    p_l.reverse()

    p_r = list()

    for j in p_l:
        s = j.split('[')[0]
        if s in d:
            break
        p_r.append(j)

    p_r.reverse()
    p_l.reverse()
    pr = '/'.join(p_r)
    pl = '/'.join(p_l)

    if pl.endswith(pr):
        pl = pl[:-len(pr) - 1]
    return pl


if __name__ == '__main__':
    remove_child('//body/div[1]/div[4]/div[1]/div/div[2]/div/table/thead/tr/th[7]/div/span[1]')
