# coding: utf-8
import os

geckodriver_path = '/usr/local/bin/geckodriver'
firefox_path = '/Applications/Firefox.app/Contents/MacOS/firefox'

run_path = os.getcwd()

report_path = run_path + '/report'
conf_path = run_path + '/conf'
log_path = run_path + '/conf/log.conf'

wd_list_run = [1, 2, 3, 4, 5, 18, 96]
# wd_list_run = [5]

run_case = []

# run_case = [
#     # run_path,
#     # 'ehking-agreement',
#     # 'onlinepay_B2B+B2C',
#     # 'MerchantAccess',
#     # 'ehking-b2b',
#     # 'ehking-express',
#     # 'ehking-b2c',
#     'ehking-scanCodeUnion',
#     # 'ehking-scanCodeAlipay',
#     # 'ehking-scanCodeWechat',
#     # 'ehking-transfer',
#     # 'ehking-QA-transfer-system',
#     #
#     # 'ehking-uat-agreement',
#     # 'ehking-uat-express',
#     # 'ehking-uat-expressUnionPay',
#     # 'ehking-uat-scanCode',
#     # 'ehking-uat-transfer',
#     # 'ehking-uat-wapUnionPay',
#     # 'ehking-uat-b2b'
# ]
