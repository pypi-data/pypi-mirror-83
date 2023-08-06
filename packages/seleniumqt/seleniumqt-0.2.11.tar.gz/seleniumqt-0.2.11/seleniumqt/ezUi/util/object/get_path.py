# coding: utf-8
import logging

logger = logging.getLogger(__name__)


def run(dr, t):
    xpath = ''
    try:
        for i in range(100):
            ele = dr.find_element_by_xpath(t)
            tn = ele.tag_name
            if tn == 'html':
                xpath = '/html/' + xpath[:-1]
                break
            if tn == 'table':
                xpath = '//table/' + xpath[:-1]
                break

            if tn == 'form':
                xpath = '//form/' + xpath[:-1]
                break

            _be = dr.find_elements_by_xpath(t + '/preceding-sibling::' + tn)
            af = dr.find_elements_by_xpath(t + '/following-sibling::' + tn)

            be_len = len(_be)

            if 'th' == tn and len(_be) > 0:
                be_ = 0
                for i in _be:
                    if i and i.rect['width'] == 0 or i.rect['height'] == 0:
                        be_ = be_ + 1
                be_len = be_len - be_

            t = t + '/..'

            split_tag = '/'
            if be_len > 0:
                split_tag = '[' + str(be_len + 1) + ']/'
            elif len(af) > 0:
                split_tag = '[1]/'

            xpath = tn + split_tag + xpath

        return xpath
    except Exception as e:
        logger.info('run_error::%s' % e)


def exc(dr, txt, e_rect):
    xpath = ''
    try:
        txt_ = None

        eles = dr.find_elements_by_xpath(txt)
        for ele in eles:
            if e_rect['x'] == ele.rect['x'] and e_rect['y'] == ele.rect['y']:
                text = ele.text.replace(' ', '')
                tag = ele.tag_name
                txt_ = "//" + tag + "[text()='" + text + "']"

        es = dr.find_elements_by_xpath(txt_)

        if len(es) != 1:
            logger.info(txt_)
            if len(es) > 0:
                for i in es:
                    logger.info('%s,%s' % (i.rect, i.text))

            logger.info(len(es))
            return
        t = txt_
        for i in range(100):

            ele = dr.find_element_by_xpath(t)

            tn = ele.tag_name
            if tn == 'body':
                xpath = '//body/' + xpath[:-1]
                break

            _be = dr.find_elements_by_xpath(t + '/preceding-sibling::' + tn)
            af = dr.find_elements_by_xpath(t + '/following-sibling::' + tn)

            be_len = len(_be)

            if 'th' == tn and len(_be) > 0:
                be_ = 0
                for i in _be:
                    if i.rect['width'] == 0 or i.rect['height'] == 0:
                        be_ = be_ + 1
                be_len = be_len - be_

            t = t + '/..'

            split_tag = '/'
            if be_len > 0:
                split_tag = '[' + str(be_len + 1) + ']/'
            elif len(af) > 0:
                split_tag = '[1]/'

            xpath = tn + split_tag + xpath

        return xpath
    except Exception as e:
        logger.info('exc_error::%s' % e)


def exit_xpath(dr, v, all_in, not_in):
    try:
        tl = ["//*[text()='" + v + "']", "//*[text()='" + v + "：']"]

        for i in tl:
            ele = dr.find_elements_by_xpath(i)

            for j in ele:
                if j.rect['width'] < 10 or j.rect['height'] < 10:
                    continue
                if v not in j.text:
                    continue

                xpath = exc(dr, i, j.rect)

                logger.info('xpath::%s' % xpath)

                if xpath == None:
                    return
                el = dr.find_elements_by_xpath(xpath)

                if len(el) != 1:
                    logger.info('exit_xpath控件数量' + str(len(el)))
                    logger.info('xpath::' + xpath)
                    continue
                for k in not_in:
                    if k in xpath:
                        logger.info('not_in::' + k)
                        logger.info('not_in::' + xpath)
                        break
                else:
                    for l in all_in:
                        if l not in xpath:
                            logger.info('in::' + l)
                            logger.info('in::' + xpath)
                            break
                    else:
                        return xpath

                logger.info('exit_xpath no::' + i + str(j.rect) + j.text)
    except Exception as e:
        logger.info('exit_xpath_error::%s' % e)
