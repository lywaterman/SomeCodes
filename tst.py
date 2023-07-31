import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

def extract_urls(xml_file):
    # 解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    urls = []

    # 遍历所有的<string>元素
    for elem in root.iter('string'):
        if elem.text:
            # 替换 &amp; 为 &
            potential_url = elem.text.replace('&amp;', '&')
            parsed = urlparse(potential_url)
            # 检查是否为有效的URL
            if bool(parsed.netloc) and bool(parsed.scheme):
                urls.append(potential_url)

    return urls

def download_images(urls, dir_path='./'):
    # 创建文件夹
    os.makedirs(dir_path, exist_ok=True)
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i, url in enumerate(urls):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content_type = response.headers['content-type']
            print(content_type)
            ext = '.jpg' if 'jpg' in content_type else '.gif' if 'octet-stream' in content_type else '.png'

            filename = f'image_{i}{ext}'
            file_path = os.path.join(dir_path, filename)

            with open(file_path, 'wb') as f:
                f.write(response.content)
urls = extract_urls('./fav.archive.plist')
print(urls)
# 调用函数，传入你的XML文件路径和图片保存路径
download_images(urls, 'stickers')

