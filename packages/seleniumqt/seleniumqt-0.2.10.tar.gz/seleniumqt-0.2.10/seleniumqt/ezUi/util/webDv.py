# coding: utf-8
import os
import run_config
import platform
from selenium import webdriver


def run():
    dr = None
    system_run = platform.system()
    if system_run == 'Darwin':
        os.system("ps x|grep Firefox|grep -v grep |awk '{print $1}'|xargs kill -9")
        os.system("ps x|grep Firefox|grep -v grep |awk '{print $1}'|xargs kill -9")
        profile = webdriver.FirefoxProfile(run_config.conf_path + '/about_support')
        dr = webdriver.Firefox(executable_path=run_config.geckodriver_path, firefox_profile=profile)
    elif system_run == 'Windows':
        dr = webdriver.Chrome()

    dr.delete_all_cookies()
    dr.maximize_window()
    dr.set_page_load_timeout(15)
    dr.set_script_timeout(15)

    return dr


if __name__ == '__main__':
    print()
