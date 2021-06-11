import os
import json
import requests
from kkt import Kkt
from store import Store
from lxml import etree
from datetime import datetime
from xml.etree import ElementTree


config_file = 'config.xml'
main_url = 'https://ofd.astralnalog.ru/api/v4.2/'
organization_id = ''
api_key = ''
inn = ''
all_kkt = []
store = []


if not os.path.exists(config_file):
    root_ = etree.Element('config')
    line_ = etree.SubElement(root_, 'api-key')
    line_.text = 'api-key'
    line_ = etree.SubElement(root_, 'inn')
    line_.text = '1234567890'
    line_ = etree.SubElement(root_, 'organization_id')
    line_.text = '12345'


    mainLine_ = etree.SubElement(root_, 'all-kkt')
    for i in range(2):
        subLine_ = etree.SubElement(mainLine_, 'kkt')
        line_ = etree.SubElement(subLine_, 'kkt_num')
        line_.text = '123456789456123'
        line_ = etree.SubElement(subLine_, 'kkt_name')
        line_.text = 'kassa_' + str(i+1)

    xml_data = etree.tostring(root_, pretty_print=True, xml_declaration=True, encoding='utf-8').decode('utf-8')

    with open(config_file, 'w') as xml_config:
        xml_config.write(xml_data)
        quit(f'Отсутствует конфигурационный файл: {config_file}.\nСоздан новый файл, заполните конфигурационные данные в файле: {config_file}.')

with open(config_file, encoding='utf-8') as f:
    doc = ElementTree.parse(f)
    data = doc.getroot()

    api_key = data.find('./api-key').text
    inn = data.find('./inn').text
    organization_id = data.find('./organization_id').text
    
    for item in data.findall('./all-kkt/kkt'):
        all_kkt.append(Kkt(kkt_num=str(item.find('kkt_num').text), kkt_name=item.find('kkt_name').text))

# Запрос данных об организации
if organization_id == '' or organization_id == None:
    url = main_url + 'users.getMe'
    params = dict(api_key=api_key)
    res = requests.get(url, params=params)

    data = json.loads(res.text)
    for item in data['result']['organization']:
        if item.get('inn') == inn:
            organization_id = item.get('id')

    #Внесение в config.xml файл id организации
    tree = ElementTree.parse(config_file)
    root = tree.getroot()
    element = root.find('./organization_id')
    element.text = organization_id
    tree.write(config_file)


url = main_url + 'kkt.alias'
params = dict(api_key=api_key, organizationId=organization_id)
res = requests.get(url, params=params)
data = json.loads(res.text)
for item in data['result']:
    store.append(Store(id=item.get('id'), alias=item.get('alias')))


for i in range(len(store)):
    url = main_url + 'kkt.listByAlias'
    params = dict(api_key=api_key, page=1, count='10', order='asc', organizationId=organization_id, aliasId=store[i].id)
    res = requests.get(url, params=params)
    data = json.loads(res.text)
    for item in data['result']['kkts']:
        for kkt in all_kkt:
            if kkt.kkt_num == item.get('numberKKT'):
                kkt.kkt_ofd_id = item.get('id')
                print(kkt.kkt_ofd_id)

# for kkt in all_kkt:
#     print(kkt.kkt_name)




