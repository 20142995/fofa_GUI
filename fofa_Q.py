import re
import os
import sys
import time
import base64
import requests
import threading
import datetime
import xlsxwriter
import PySimpleGUI as sg

# 设置主题
sg.theme('SystemDefaultForReal')

# 设置logo
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)
sg.set_global_icon(os.path.join(basedir, 'favicon.ico'))

global stop_flag

stop_flag = False

fields = [
    'ip',
    'port',
    'protocol',
    'country',
    'country_name',
    'region',
    'city',
    'longitude',
    'latitude',
    'as_number',
    'as_organization',
    'host',
    'domain',
    'os',
    'server',
    'icp',
    'title',
    'jarm',
    'header',
    'banner',
    'cert',
    'base_protocol',
    'link',
    'certs_issuer_org',
    'certs_issuer_cn',
    'certs_subject_org',
    'certs_subject_cn',
    'tls_ja3s',
    'tls_version',
    'product',
    'product_category',
    'version',
    'lastupdatetime',
    'cname',
    # 'icon_hash',
    # 'certs_valid',
    # 'cname_domain',
    # 'body',
    # 'icon',
    # 'fid',
    # 'structinfo'
]

fields_zh = [
    'ip地址',
    '端口',
    '协议名',
    '国家代码',
    '国家名',
    '区域',
    '城市',
    '地理位置经度',
    '地理位置纬度',
    'asn编号',
    'asn组织',
    '主机名',
    '域名',
    '操作系统',
    '网站server',
    'icp备案号',
    '网站标题',
    'jarm指纹',
    '网站header',
    '协议banner',
    '证书',
    '基础协议',
    '资产的URL链接',
    '证书颁发者组织',
    '证书颁发者通用名称',
    '证书持有者组织',
    '证书持有者通用名称',
    'ja3s指纹信息',
    'tls协议版本',
    '产品名',
    '产品分类',
    '版本号',
    'FOFA最后更新时间',
    '域名cname',
    # '返回的icon_hash值',
    # '证书是否有效',
    # 'cname的域名',
    # '网站正文内容',
    # 'icon图标',
    # 'fid',
    # '结构化信息 (部分协议支持、比如elastic、mongodb)'
]

fields_list = list(zip(fields, fields_zh))


def calculate_length(string):
    '''计算字符串长度'''
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', string))
    lowercase_count = len(re.findall(r'[a-z]', string))
    length = chinese_count + lowercase_count // 2
    return length


def parse_num(fields_list, n=20):
    '''生成复选框'''
    rows, row, current_n = [], [], 0
    for key, text in fields_list:
        if key in ['ip','host','port']:
            row.append(sg.Checkbox(text, key=key,default=True, disabled=True))
        else:
            row.append(sg.Checkbox(text, key=key))
        current_n += calculate_length(text) + 2
        if current_n >= n:
            rows.append(row)
            row, current_n = [], 0
    else:
        rows.append(row)
    return rows


def list2xlsx(excle_name, **tables):
    ''''写入xlsx文件'''
    workbook = xlsxwriter.Workbook(excle_name)
    for name, rows in tables.items():
        if not rows:
            continue
        worksheet = workbook.add_worksheet(name)
        for index, row in enumerate(rows):
            worksheet.write_row(index, 0, row)
    workbook.close()


def long_time_work(window, values):
    '''批量查询'''
    global stop_flag
    current_fields = [
        k for k in fields if k in values and values.get(k) is True]
    start_page = int(values['-NUM1-'])
    end_page = int(values['-NUM2-'])
    size = int(values['-NUM3-'])
    qs = [i.strip() for i in values['-INPUT-'].split('\n') if i.strip()]
    window['-LOG-'].print(f'{datetime.datetime.now()} 当前查询语句数: {len(qs)}')

    def fofa_query(q='', start_page=1, end_page=100, size=100):
        '''执行查询'''
        global stop_flag
        api_url = 'https://fofa.info/api/v1/search/all'
        fofa_key = os.getenv('fofa_key')
        if not fofa_key:
            window['-LOG-'].print(f'{datetime.datetime.now()} 请设置环境变量 "fofa_key"')
            stop_flag = True
            return _
        _ = []
        current_page = start_page
        while True:
            qbase64 = base64.b64encode(q.encode('utf8')).decode('utf8')
            params = {'key': fofa_key, 'qbase64': qbase64, 'fields': ','.join(
                current_fields), 'page': current_page, 'size': size, 'full': True}
            rj = requests.get(api_url, params=params).json()
            if rj['error']:
                window['-LOG-'].print(
                    f'{datetime.datetime.now()} errmsg={rj["errmsg"]}')
                return _
            else:
                window['-LOG-'].print(
                    f'{datetime.datetime.now()} query="{rj["query"]}", current_page={rj["page"]}, current_size={len(rj["results"])}, size={rj["size"]}')
                for row in rj['results']:
                    item = {'query': rj["query"], 'current_page': rj["page"]}
                    item.update(dict(zip(current_fields, row)))
                    _.append(item)
                if rj["page"] * size > rj["size"] or current_page >= end_page:
                    break
                # if rj["size"] > 800:
                #     break
                current_page += 1
            if stop_flag:
                window['-LOG-'].print(f'{datetime.datetime.now()} 结束当前页查询')
                break
        return _
    results = []
    for q in qs:
        results += fofa_query(q=q, start_page=start_page,
                              end_page=end_page, size=size)
        if stop_flag:
            window['-LOG-'].print(f'{datetime.datetime.now()} 结束当前语句查询')
            break
    else:
        window['-LOG-'].print(f'{datetime.datetime.now()} 查询完毕，结果数: {len(results)}')
    if len(results) > 0:
        rows = []
        fields_dict = dict(zip(fields, fields_zh))
        title = [fields_dict[t] for t in current_fields]
        title = ['查询语句', '查询页'] + title
        rows.append(title)
        for item in results:
            row = []
            for t in ['query', 'current_page'] + current_fields:
                row.append(str(item.get(t, '')))
            rows.append(row)
        filename = time.strftime("%Y-%m-%d-%H-%M-%S_fofa_api_results.xlsx")
        list2xlsx(filename, Sheet1=rows)
        window['-LOG-'].print(f'{datetime.datetime.now()} 导出结果到: {filename}')
        os.startfile(os.getcwd())


def main():
    global stop_flag
    layout = [
        [sg.Multiline(size=(100, 10), key='-INPUT-')],
        [sg.Text('起始页: '), sg.Input(key='-NUM1-', default_text='1', size=(10, None)), sg.Text('结束页: '), sg.Input(key='-NUM2-', default_text='1', size=(10, None)),
         sg.Text('每页数量: '), sg.Input(key='-NUM3-', default_text='100', size=(10, None)), sg.Button('开始查询', key='-START-'), sg.Button('结束查询', key='-STOP-')],
        [sg.Text('导出字段：')],
        parse_num(fields_list, n=40),
        [sg.Multiline(size=(100, 10), key='-LOG-')],
    ]

    window = sg.Window('FOFA API 数据导出', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-START-':
            window['-LOG-'].print(f'{datetime.datetime.now()} 开始查询')
            threading.Thread(target=long_time_work, args=(
                window, values), daemon=True).start()
        if event == '-STOP-':
            stop_flag = True
            window['-LOG-'].print(f'{datetime.datetime.now()} 正在结束查询')

    window.close()


if __name__ == '__main__':
    main()
