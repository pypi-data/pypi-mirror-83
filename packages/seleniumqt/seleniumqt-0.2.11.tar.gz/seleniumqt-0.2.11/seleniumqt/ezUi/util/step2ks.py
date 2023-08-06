#coding: utf-8
def run(sv):
    case_retry = list()
    c = list()
    for j in sv:
        if j[0] == 'url':
            if len(c) > 0:
                t = c.copy()
                case_retry.append(t)
            c.clear()
        c.append(j)
    else:
        case_retry.append(c)

    return case_retry
