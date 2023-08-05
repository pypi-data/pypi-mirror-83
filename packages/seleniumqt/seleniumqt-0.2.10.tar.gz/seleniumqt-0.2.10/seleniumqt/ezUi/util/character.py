# coding: utf-8
import re
import traceback


def rmv_pam(step, pam_dict):
    try:
        jl = step
        pam_in = False
        if len(step) > 2:
            pam = str(step[2])
            if '<' in pam and '>' in pam:
                for k, v in pam_dict.items():
                    if '<' + k + '>' in pam:
                        pam = pam.replace('<' + k + '>', str(v))
                        pam_in = True
            if '[' in pam and ']' in pam:
                rlt = re.findall('\[(.*)\]', pam)
                for i in rlt:
                    f = 0
                    if '-' in i:
                        t = i.split('-')
                        f = float(t[0]) if t[0] else f
                        for tId in t[1:]:
                            f = f - float(tId)

                    elif '+' in i:
                        f = float(i.split('+')[0]) + float(i.split('+')[1])

                    if f:
                        b_str = str(round(f, 2))
                        if b_str.endswith('.00'):
                            b_str = b_str.replace('.00', '')
                        if b_str.endswith('.0'):
                            b_str = b_str.replace('.0', '')
                        if b_str:
                            pam = pam.replace('[' + i + ']', b_str)
                            pam_in = True
            jl[2] = pam
        return jl, pam_in
    except:
        print(step)
        print(pam_dict)
        traceback.print_exc()
