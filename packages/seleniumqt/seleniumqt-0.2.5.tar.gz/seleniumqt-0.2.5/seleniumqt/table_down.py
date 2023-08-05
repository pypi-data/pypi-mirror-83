def run(dr, text):
    t = "//span[text()='" + text + "']"

    es = dr.find_elements_by_xpath(t)
    if len(es) == 1:
        xpath = get_path(dr, t)
        xpath = xpath.replace('thead', 'tbody').replace('th', 'td')
        nodes = dr.find_element_by_xpath(xpath)
        return nodes


def get_path(dr, t):
    xpath = ''

    for i in range(100):
        ele = dr.find_element_by_xpath(t)
        tn = ele.tag_name
        if tn == 'html':
            break
        be = dr.find_elements_by_xpath(t + '/preceding-sibling::' + tn)
        af = dr.find_elements_by_xpath(t + '/following-sibling::' + tn)
        t = t + '/..'

        split_tag = '/'
        if len(be) > 0:
            split_tag = '[' + str(len(be) + 1) + ']/'
        elif len(af) > 0:
            split_tag = '[1]/'

        xpath = tn + split_tag + xpath

    xpath = '/html/' + xpath[:-6]
    return xpath
