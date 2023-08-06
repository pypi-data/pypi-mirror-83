#coding: utf-8
import logging

logger = logging.getLogger(__name__)


def run(dr, text):
    try:
        text_1 = text.split('||')[0]
        t_label = "//*[contains(text(),'" + text_1 + "')]"

        ele_t1 = dr.find_elements_by_xpath(t_label)

        eles = list()
        for i in ele_t1:
            for j in text.split('||')[1:]:
                if j not in i.text:
                    break
            else:
                eles.append(i)

        if len(eles) > 1:
            logger.info('获取::%s,%s个', text, len(eles))

        return eles[0]
    except Exception as e:
        logger.info(e)
