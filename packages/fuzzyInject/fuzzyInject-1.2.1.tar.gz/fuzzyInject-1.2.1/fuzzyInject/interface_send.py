
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
import main_entry
import yaml
import requests
from requests import exceptions
import basic_config


# 组装get的请求方法
def send_get_method(url, params, cookies):
    req = {}
    params_str = ''
    if params != '{}':
        for params_key, params_value in params.items():
            params_str = params_str + params_key + \
                '=' + str(params[params_key]) + '&'
            params_str = params_str[:-1]
            # print params_str
            url = url + '?' + params_str
    req = requests.get(url, cookies=cookies, timeout=2)
    print("*****************************")
    print(url)
    req = getGetReq(req)

    return req


# 组装post的请求方法
def send_post_method(url, params, cookies):
    headers = {}
    headers = {'Content-Type': 'application/json'}
    req = {}
    params = json.dumps(params)
    print(params)
    params = params.replace('\"[', '["')
    params = params.replace(']\"', '"]')
    params = params.replace('\"false\"', 'false')
    params = params.replace('\"true\"', 'true')
    params = json.loads(params)
    req = requests.post(url, data=params, headers=headers,
                        cookies=cookies, timeout=2)
    req = getGetReq(req)

    return req

# 组装post的请求方法


def send_post_method(url, params, cookies):
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    req = {}
    params = json.dumps(params)
    # print(params)
    req = requests.post(url, data=params, headers=headers,
                        cookies=cookies, timeout=2)
    req = getGetReq(req)
    return req


# 接口请求逻辑相关代码
def assemble_request(request_method, request_url, params_get, cookies):
    req_post = ''
    req_get = ''

    try:
        if request_method == 'GET':
            if params_get != {}:
                req_get = send_get_method(request_url, params_get, cookies)
                return req_get
            else:
                req_get = send_get_method(request_url, '{}', cookies)
                return req_get
        if request_method == 'POST':
            if params_get != {}:
                req_post = send_post_method(request_url, params_get, cookies)
                return req_post
            else:
                req_post = send_post_method(request_url, '{}', cookies)
                return req_post
    except exceptions.Timeout as e:
        if request_method == 'POST':
            req_post = '{ "data":' + str(req_post) + \
                ',"msg":"FAILED","status":' + str(e) + '}'
            return req_post
        if request_method == 'GET':
            req_get = '{ "data":' + str(req_get) + \
                ',"msg":"FAILED","status":' + str(e) + '}'
            return req_get
        print(str(e))
    except Exception as e:
        if request_method == 'POST':
            req_post = '{ "data":' + str(req_post) + \
                ',"msg":"FAILED","status":' + str(e) + '}'
            return req_post
        if request_method == 'GET':
            req_get = '{ "data":' + str(req_get) + \
                ',"msg":"FAILED","status":' + str(e) + '}'
            return req_get
        print(e)


# 组装请求参数和fuzzy的分配逻辑相关代码
def assemble_params(request_method, request_url, request_query, request_formdata, params_yaml, phone_cookie_yaml):
    request_result_list = []
    params_get = {}
    params_get_list = []
    params_test = read_yaml(params_yaml)
    cookies = get_cookie(phone_cookie_yaml)
    request_result_url = []
    if len(request_query) > 0:
        result = assemble_request(request_method, request_url, '{}', cookies)
        params_get_list.append(str('{}'))
        request_result_list.append(result)
        request_result_url.append(request_url + "\n\t请求方法:" + request_method)
        for params_index in range(0, len(params_test)):
            params_get.clear()
            for query_index in range(0, len(request_query)):
                params_get[request_query[query_index]
                           ] = params_test[params_index]
                result = assemble_request(
                    request_method, request_url, params_get, cookies)
                params_get_list.append(str(params_get))
                request_result_list.append(result)
                request_result_url.append(
                    request_url + str(params_get) + "\n请求方法:" + request_method)
                result = ''
    elif len(request_formdata) > 0:
        result = assemble_request(request_method, request_url, '{}', cookies)
        params_get_list.append(str('{}'))
        request_result_list.append(result)
        request_result_url.append(request_url + "\n\t请求方法:" + request_method)
        for params_index in range(0, len(params_test)):
            params_get.clear()
            for query_index in range(0, len(request_formdata)):
                params_get[request_formdata[query_index]
                           ] = params_test[params_index]
                result = assemble_request(
                    request_method, request_url, params_get, cookies)
                params_get_list.append(str(params_get))
                request_result_list.append(result)
                request_result_url.append(
                    request_url + str(params_get) + "\n请求方法:" + request_method)
                result = ''
    else:
        result = assemble_request(
            request_method, request_url, params_get, cookies)
        params_get_list.append(str(params_get))
        request_result_list.append(result)
        request_result_url.append(request_url + "\n\t请求方法:" + request_method)
        result = ''

    return request_result_list, params_get_list, request_result_url


# 处理为raw的post请求

def assemble_params_formdata(request_method, request_url, request_formdata, params_yaml, phone_cookie_yaml):
    request_result_list = []
    params_get = {}
    params_get_list = []
    params_test = read_yaml(params_yaml)
    cookies = get_cookie(phone_cookie_yaml)
    request_result_url = []
    params_get_child = {}
    params_get_list.append(str('{}'))
    result = assemble_request(request_method, request_url, {}, cookies)
    request_result_list.append(result)
    request_result_url.append(request_url + "\n\t请求方法:" + request_method)
    if len(request_formdata) > 0:
        result = assemble_request(request_method, request_url, '{}', cookies)
        params_get_list.append(str('{}'))
        request_result_list.append(result)
        request_result_url.append(request_url + "\n\t请求方法:" + request_method)
        for params_index in range(0, len(params_test)):
            params_get.clear()
            for query_index in range(0, len(request_formdata)):
                params_get[request_formdata[query_index]
                           ] = params_test[params_index]
                result = assemble_request(
                    request_method, request_url, params_get, cookies)
                params_get_list.append(str(params_get))
                request_result_list.append(result)
                request_result_url.append(
                    request_url + str(params_get) + "\n请求方法:" + request_method)
                result = ''
    else:
        params_get_list.append(str('{}'))
        result = assemble_request(request_method, request_url, {}, cookies)
        request_result_list.append(result)
        request_result_url.append(request_url + "\n\t请求方法:" + request_method)

    return request_result_list, params_get_list, request_result_url
    # if len(request_raw) > 0:
    #     for params_index in range(0, len(params_test)):
    #         params_get.clear()
    #         # 字典需要copy(),否则clear影响原字典
    #         params_get = request_raw.copy()
    #         for key, value in list(request_raw.items()):
    #             if '{' in str(request_raw[key]):
    #                 if (isinstance(request_raw[key], list)):
    #                     request_raw[key] = listToJson(request_raw[key])

    #                 child_json = json.loads(str(request_raw[key]))
    #                 for child_key, child_value in list(child_json.items()):
    #                     child_json[child_key] = params_test[params_index]
    #                     params_get[key] = child_json
    #             else:
    #                 params_get[key] = params_test[params_index]
    #         # print(params_get)
    #         result = send_post_raw_method(request_url, params_get, cookies)
    #         params_get_list.append(str(params_get))
    #         request_result_url.append(
    #             request_url + "\n\t请求方法:" + request_method)
    #         request_result_list.append(result)
    #         result = ''


# 处理为外部api 渠道 （小米、墨智）raw的post请求

def assemble_params_raw_other(request_method, request_url, request_raw, params_yaml, phone_cookie_yaml):
    request_result_list = []
    params_get = {}
    params_get_list = []
    child_json = {}
    params_test = read_yaml(params_yaml)
    cookies = get_cookie(phone_cookie_yaml)
    request_result_url = []
    params_get_child = {}
    params_get_list.append(str('{}'))
    result = assemble_request(request_method, request_url, {}, cookies)
    request_result_list.append(result)
    request_result_url.append(request_url + "\n\t请求方法:" + request_method)
    print("****************")
    print(request_url)
    if len(request_raw) > 0:
        for params_index in range(0, len(params_test)):
            params_get.clear()
            child_json.clear()
            # 字典需要copy(),否则clear影响原字典
            params_get = request_raw.copy()
            # print("here,here")
            # print(params_get)
            child_json = check_json_value(
                params_get, str(params_test[params_index]))

            # print(child_json)
            result = assemble_request(
                request_method, request_url, child_json, cookies)
            params_get_list.append(str(child_json))
            request_result_url.append(
                request_url + "\n\t请求方法:" + request_method)
            request_result_list.append(result)
            result = ''
    else:
        params_get_list.append(str('{}'))
        result = assemble_request(request_method, request_url, {}, cookies)
        request_result_list.append(result)
        request_result_url.append(request_url + "\n\t请求方法:" + request_method)

    return request_result_list, params_get_list, request_result_url


# 请求参数json自由赋值

def check_json_value(dic_json, v):
    if isinstance(dic_json, dict):
        for key in dic_json:
            if isinstance(type(dic_json[key]), str):
                dic_json[key] = eval(dic_json[key])
            if key != 'method' and key != 'params' and key != 'hashcode':
                dic_json[key] = v
            elif isinstance(dic_json[key], dict):
                check_json_value(dic_json[key], v)
    # print(dic_json)
    return dic_json


# 读取yaml接口字段


def read_yaml(yamlFile):
    f = open(yamlFile)
    f = yaml.safe_load(f)
    return f


# raw转换字典
dic = {}


def json_txt(dic_json):
    if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
        for key in dic_json:
            if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                # print("****key--：%s value--: %s" % (key, dic_json[key]))
                json_txt(dic_json[key])
                dic[key] = dic_json[key]
            else:
                # print("****key--：%s value--: %s" % (key, dic_json[key]))
                dic[key] = dic_json[key]
                # print(dic)
    return dic


# list 转成Json格式数据
def listToJson(lst):
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2,
                          ensure_ascii=False)  # json转为string
    return str_json


# 接口响应结果响应处理
def getGetReq(req):
    print(req.status_code)
    if req.status_code == 200 and str(req.content, 'utf-8') != "":
        req = req.json()
        req = json.dumps(req, sort_keys=True, indent=2,
                         separators=(',', ': '), ensure_ascii=False)
    else:
        req = '{ "data":' + str(req.content, 'utf-8') + ',"msg":"FAILED","status":' + \
            str(req.status_code) + '}'
    return req

# cookie 的公共方法


def get_cookie(phone_cookie_yaml):
    cookies = read_yaml(phone_cookie_yaml)
    return cookies

if __name__ == "__main__":
    # json_file = sys.argv[1]
    f = read_yaml("params.yaml")
    print(f)
    # assemble_request(json_file)
    # send_post_method('http://microloan-operating-activity.yxapp.xyz/wallet/internal/depositRecord/updateAll','{}')
