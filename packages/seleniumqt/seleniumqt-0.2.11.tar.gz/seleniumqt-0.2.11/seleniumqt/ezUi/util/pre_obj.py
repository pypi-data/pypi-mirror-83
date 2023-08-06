#coding: utf-8
def run(l):
    obj = list()
    for i in l:
        if (i.tag_name == 'span' and i.get_attribute("class") == '') \
                or i.tag_name in ['button']:
            obj.append(i)
    if len(obj) == 1:
        return True, obj[0]
    else:
        return False, None
