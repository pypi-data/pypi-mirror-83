# coding: utf-8
import logging

logger = logging.getLogger(__name__)


def elements(p):
    try:
        if p[1][1] in ['验证2', '取参2'] \
                and u'\u9fa5' >= p[1][0][0] >= u'\u4e00':
            er = list()
            for ri in range(2):
                try:
                    eg = p[0].find_elements_by_xpath("//*[text()='" + p[1][0] + "']/following-sibling::td[1]")

                    if len(eg) > 0 and eg[0].text:
                        logger.info('v:%s,tag:%s,rect:%s' % (p[1][0], str(eg[0].tag_name), str(eg[0].rect)))

                        return eg[0]

                    eg = p[0].find_elements_by_xpath("//*[text()='" + p[1][0] + "']")
                    if len(eg) > 0 and eg[0].tag_name in ['span', 'a']:
                        eg = p[0].find_elements_by_xpath("//*[text()='" + p[1][0] + "']/parent::*")

                    if len(eg) > 0:
                        rg = eg[0].rect

                        if eg[0].tag_name == 'th':
                            erl = p[0].find_elements_by_tag_name('td')
                        else:
                            erl = p[0].find_elements_by_tag_name('div')

                        for i in erl:
                            ri = i.rect
                            if rg['x'] + rg['width'] / 2 == ri['x'] + ri['width'] / 2:
                                if ri['y'] + ri['height'] / 2 - rg['y'] - rg['height'] / 2 > rg['height'] / 2:
                                    if i.text != p[1][0]:
                                        er.append([ri['y'], i])

                        er.sort()

                        logger.info('v:%s,tag:%s,rect:%s' % (p[1][0], str(er[0][1].tag_name), str(er[0][1].rect)))

                        return er[0][1]
                except Exception as e:
                    logger.info('eg%s' % e)
                    continue

    except Exception as e1:
        logger.info('%s' % (e1))

    return None
