import os
import requests
from lxml import etree
from datetime import datetime
from xml.etree import ElementTree

config_file = 'config.xml'
api_key = ''

if not os.path.exists(config_file):
    root_ = etree.Element('config')
    line_ = etree.SubElement(root_, 'api-key')
    line_.text = 'api-key'

    xml_data = etree.tostring(root_, pretty_print=True, xml_declaration=True, encoding='utf-8').decode('utf-8')

    with open(config_file, 'w') as xml_config:
        xml_config.write(xml_data)
        quit(f'Отсутствует конфигурационный файл: {config_file}.\nСоздан новый файл, заполните конфигурационные данные в файле: {config_file}.')

with open(config_file) as f:
    doc = ElementTree.parse(f)
    data = doc.getroot()

    api_key = data.find('./api-key').text

org_id = ""

url = 'https://ofd.astralnalog.ru/api/v4.2/users.getMe'
params = dict(api_key=api_key)

url = 'https://ofd.astralnalog.ru/api/v4.2/kkt.alias'
params = dict(api_key=api_key, organizationId=org_id)

res = requests.get(url, params=params)
print(res.text)
