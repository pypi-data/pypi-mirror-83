#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
# author:lol
# date:2018-05-24

'''
本工程主要用于json文件的解析和读取、格式化
'''


import jsonpath_rw_ext as jp
import codecs
import json
import sys
from fuzzyInject.interface_send import assemble_params
from fuzzyInject.showData import covertToHtml, assemble_html

# reload(sys)
# sys.setdefaultencoding('UTF-8')


# 处理dict中为unicode编码的转化去掉u'
def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


# 处理list中的u'
def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(value, str):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


# 遍历文件夹内容


params_get_list = []
request_results_list = []
result_urls = []
final_results = []
result_collections = []
# 解析json文件 和报告数据组装


def parse_json_file(json_file_parse, paramsFile, phone_cookie_yaml):
    global final_results
    names = jp.match("$.item[*].name", json_file_parse)

    request_results = []
    for i in range(0, len(names)):
        request_method = jp.match(
            "$.item[" + str(i) + "].request.method", json_file_parse)[0]
        request_url = jp.match(
            "$.item[" + str(i) + "].request.url", json_file_parse)[0]
        # raw 为空情况剔除
        if isinstance(request_url, dict):
            request_url = jp.match(
                "$.item[" + str(i) + "].request.url.raw", json_file_parse)[0].split('?')[0]
            print('本次请求链接' + str(request_url))
        else:
            request_url = jp.match(
                "$.item[" + str(i) + "].request.url", json_file_parse)[0]
            print('本次请求链接' + str(request_url))
        request_query = jp.match(
            "$.item[" + str(i) + "].request.url.query[*].key", json_file_parse)
        request_formdata = jp.match(
            "$.item[" + str(i) + "].request.body.formdata[*].key", json_file_parse)
        request_raw = jp.match(
            "$.item[" + str(i) + "].request.body.raw", json_file_parse)
        if request_raw != []:
            date_json = json.loads(request_raw[0])
            # print(date_json)
            request_result_list, param_get_list, request_result_url = assemble_params_raw_other(
                request_method, request_url, date_json, paramsFile, phone_cookie_yaml)
            print(request_result_list)
            final_results = get_result_collect(request_result_list,
                                               param_get_list, request_result_url)
        if request_formdata != []:
            # print(request_formdata)
            # 避免重复覆盖
            request_query = []
            request_result_list, param_get_list, request_result_url = assemble_params_formdata(
                request_method, request_url, request_formdata, paramsFile, phone_cookie_yaml)
            print(request_result_list)
            final_results = get_result_collect(request_result_list,
                                               param_get_list, request_result_url)
        if request_query != []:
            request_result_list, param_get_list, request_result_url = assemble_params(
                request_method, request_url, request_query, request_formdata, paramsFile, phone_cookie_yaml)
            final_results = get_result_collect(request_result_list,
                                               param_get_list, request_result_url)
            print(request_result_list)
        else:
            request_result_list, param_get_list, request_result_url = assemble_params(
                request_method, request_url, request_query, request_formdata, paramsFile, phone_cookie_yaml)
            final_results = get_result_collect(request_result_list,
                                               param_get_list, request_result_url)
            print(request_result_list)

    return final_results


# 收集结果信息
def get_result_collect(request_result_list, param_get_list, request_result_url):
    if request_result_list != [] and param_get_list != [] and request_result_url != []:
        for add_index in range(0, len(request_result_list)):
            request_results_list.append(request_result_list[add_index])
            params_get_list.append(param_get_list[add_index])
            result_urls.append(request_result_url[add_index])
            if request_result_list[add_index] is None:
                result_collections.append('FAILED')
                return
            if 'status' not in request_result_list[add_index] or 'FAILED' in request_results_list[add_index] or 'error' in request_results_list[add_index]:
                result_collections.append('FAILED')
            else:
                result_collections.append(
                    'SUCCESS')

    final_results.append(result_urls)
    final_results.append(request_results_list)
    final_results.append(result_collections)
    final_results.append(params_get_list)

    request_result_list = []
    param_get_list = []
    request_result_url = []

    return final_results


# 读取文件
def read_json_file(json_file):
    with codecs.open(json_file, 'rb') as f:
        data = json.load(f)
        # print (data)
        # data = _decode_dict(data)
        # print (data)
    return data


def write_html_file(html_file):
    with codecs.open('result_alllt_show.html', 'wb') as f:
        f.write(html_file)
        f.close()


def excute_interface(file, paramsFile, phone_cookie_yaml):
    name = ['接口', '接口返回值', '结果', '参数']
    result_all = {}
    json_file = file
    json_file_parse = read_json_file(json_file)
    final_results = parse_json_file(
        json_file_parse, paramsFile, phone_cookie_yaml)
    html = covertToHtml(final_results, name)
    if final_results is None:
        return
    count_name = '请求结果总计:' + str(len(final_results[0]))
    html_file = assemble_html(count_name, html, '')
    write_html_file(html_file)


if __name__ == "__main__":
    yamFile = sys.argv[1]
    json_file = sys.argv[2]
    phone_cookie_yaml = "params_phone.yaml"
    excute_interface(json_file, yamFile, phone_cookie_yaml)
    # name = ['接口','接口返回值','结果','参数']
    # result_all = {}
    # json_file = sys.argv[1]
    # json_file_parse = read_json_file(json_file)
    # final_results = parse_json_file	(json_file_parse)
    # html = showData.covertToHtml(final_results,name)
    # count_name = '请求结果总计:' + str(len(final_results[0]))
    # html_file = showData.assemble_html(count_name,html,'http://10.106.164.66:9907/jenkins/job/interface_params_required/HTML_20Report/')
    # write_html_file(html_file)
    # print html
