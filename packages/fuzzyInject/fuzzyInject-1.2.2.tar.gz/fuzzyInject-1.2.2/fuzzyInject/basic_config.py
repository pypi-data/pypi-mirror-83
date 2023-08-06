#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
# author:lol
# date:2018-05-24

'''
本工程主要用于接口请求、cookie解析等
'''
import jsonpath_rw_ext as jp
import codecs
import json
# import sys
# reload(sys)
# sys.setdefaultencoding('UTF-8')
import yaml
import requests


# cookie 的公共方法
def get_cookie():

    cookies = {'login_sess': 'c1LCPDHdqCAY6V2lw6Kx6HgrUwusV9OpESSBoBPpr33CeWQ',
               'phone': '13716054767'}

    return cookies


# 读取yaml接口字段
def read_yaml(yamlFile):
    f = open(yamlFile)
    f = yaml.load(f)
    return f


if __name__ == "__main__":
    # json_file = sys.argv[1]
    f = read_yaml("params.yaml")
    print(f)
    # assemble_request(json_file)
    # send_post_method('http://microloan-operating-activity.yxapp.xyz/wallet/internal/depositRecord/updateAll','{}')
