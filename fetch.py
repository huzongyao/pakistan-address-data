import json

import requests
import time
import xlsxwriter

requests.packages.urllib3.disable_warnings()


def fetch_some_address(addr_id=None):
    url = 'https://member.daraz.pk/locationtree/api/getSubAddressList'
    params = {}
    if addr_id:
        params['addressId'] = addr_id
    time.sleep(2)
    r = requests.get(url, params=params, verify=False)
    res_obj = json.loads(r.text, encoding='utf-8-sig')
    print('One Fetch [%s]!!' % addr_id)
    return res_obj['module']


def add_address_to_sheet(addrs, sheet):
    titles = ['id', 'name', 'nameLocal', 'parentId', 'displayName']
    line = 0
    for idx, ti in enumerate(titles):
        sheet.write(line, idx, ti)
    line += 1
    for addr in addrs:
        for idx1, it in enumerate(addr):
            sheet.write(line, idx1, addr[it])
        line += 1


workbook = xlsxwriter.Workbook('./pakistan.xlsx')
sheet1 = workbook.add_worksheet()
sheet2 = workbook.add_worksheet()
sheet3 = workbook.add_worksheet()

level1 = fetch_some_address()
add_address_to_sheet(level1, sheet1)

l2all = []
l3all = []

for lev in level1:
    level2 = fetch_some_address(lev['id'])
    l2all.extend(level2)
    for lev1 in level2:
        level3 = fetch_some_address(lev1['id'])
        l3all.extend(level3)
add_address_to_sheet(l2all, sheet2)
add_address_to_sheet(l3all, sheet3)
workbook.close()
