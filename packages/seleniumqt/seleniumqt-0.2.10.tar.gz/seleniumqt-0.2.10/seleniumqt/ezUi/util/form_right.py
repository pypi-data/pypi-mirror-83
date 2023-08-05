# coding: utf-8
import logging
import time

logger = logging.getLogger(__name__)


def run(p, v, t_):
    '''
    /html/body/div[3]/div[3]/div/div/div/div/div[1]/div[1]/form/div[3]/div/div[3]/label/span[1]
    /html/body/div[3]/div[3]/div/div/div/div/div[1]/div[1]/form/div[3]/div/div[3]/label/span[2]/input
    '''
    try:
        txt_ = "[text()='" + v + "']"
        e_sdk_0 = p[0].find_elements_by_xpath("//*" + txt_)
        if len(e_sdk_0) == 0:
            txt_ = "[text()='" + v + "：']"
            e_sdk_0 = p[0].find_elements_by_xpath("//*" + txt_)

            if len(e_sdk_0) == 0:
                txt_ = "[contains(text(),'" + v + "')]"
                e_sdk_0 = p[0].find_elements_by_xpath("//*" + txt_)

        for i_e in e_sdk_0:

            if i_e.rect['width'] < 10 or i_e.rect['height'] < 10:
                if i_e.rect['width'] > 1:
                    logger.info(i_e.rect)
                continue

            if v not in i_e.text:
                logger.info(txt_)
                logger.info(i_e.text)
                continue

            if i_e.tag_name == 'td':
                if p[1][1] in ['输入']:
                    td_se_1 = p[0].find_elements_by_xpath(
                        "//td" + txt_ + "/following-sibling::*[1]/descendant::input")
                    if len(td_se_1) == 1:
                        time.sleep(t_)
                        return td_se_1[0]

                    td_se_2 = p[0].find_elements_by_xpath(
                        "//td" + txt_ + "/following-sibling::*[1]/descendant::textarea")
                    if len(td_se_2) == 1:
                        time.sleep(t_)
                        return td_se_2[0]

                if p[1][1] in ['选择']:
                    e_sdk_2 = p[0].find_elements_by_xpath(
                        "//td" + txt_ + "/following-sibling::*[1]/descendant::select")
                    if len(e_sdk_2) == 1:
                        time.sleep(t_)
                        return e_sdk_2[0]
            if i_e.tag_name == 'label':
                if p[1][1] in ['选择']:
                    e_sdk_3 = p[0].find_elements_by_xpath(
                        "//label" + txt_ + "/following-sibling::*[1]/descendant::select")
                    if len(e_sdk_3) == 1:
                        time.sleep(t_)
                        return e_sdk_3[0]
                if p[1][1] in ['输入']:
                    e_sdk_4 = p[0].find_elements_by_xpath(
                        "//label" + txt_ + "/following-sibling::*[1]")

                    if len(e_sdk_4) == 0:
                        e_sdk_4 = p[0].find_elements_by_xpath(
                            "//label" + txt_ + "/parent::*/following-sibling::*[1]")
                    for el in e_sdk_4:
                        el.click()
                        e_sdk_cld = el.find_elements_by_tag_name('input')

                        if len(e_sdk_cld) == 1:
                            time.sleep(t_)
                            return e_sdk_cld[0]

            if p[1][1] in ['输入']:

                txt_re = i_e.tag_name + "[text()='" + i_e.text + "']"

                td_se_6 = p[0].find_elements_by_xpath(
                    "//" + txt_re + "/following-sibling::*[1]/descendant::input")

                if len(td_se_6) == 1:
                    time.sleep(t_)
                    return td_se_6[0]

                td_se_7 = p[0].find_elements_by_xpath(
                    "//" + txt_re + "/following-sibling::*[1]/descendant::textarea")
                if len(td_se_7) == 1:
                    time.sleep(t_)
                    return td_se_7[0]

                logger.info(txt_)
                logger.info(len(td_se_6))
                logger.info(len(td_se_7))

            if p[1][1] in ['验证']:

                txt_re = i_e.tag_name + "[text()='" + i_e.text + "']"

                e_sdk_5 = p[0].find_elements_by_xpath(
                    "//" + txt_re + "/following-sibling::*[1]/descendant::*[1]")
                if len(e_sdk_5) == 1:
                    time.sleep(t_)
                    return e_sdk_5[0]
        logger.info('%s,%s' % (txt_, len(e_sdk_0)))
        time.sleep(1)
    except Exception as e:
        logger.info('%s,%s' % (__name__, e))
    return False
