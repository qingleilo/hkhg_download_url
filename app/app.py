from flask import Flask, request, jsonify
import openpyxl
import random

app = Flask(__name__)

# 读取 xls 文件并获取下载链接列表
def get_download_links():
    workbook = openpyxl.load_workbook('河口海关.xlsx')
    sheet = workbook.active
    download_links = [cell.value for row in sheet.iter_rows(values_only=True) for cell in row]
    return download_links

download_links = get_download_links()

# 记录已返回的下载链接和已使用的下载链接
used_links = set()
returned_links = []

@app.route('/get_download_link', methods=['GET'])
def get_random_download_link():
    if not download_links:
        return jsonify({'error': 'No download links available'})

    # 查找尚未使用的链接
    available_links = [link for link in download_links if link not in used_links]

    if not available_links:
        return jsonify({'error': 'All download links have been used'})

    # 随机选择一个未使用的下载链接
    selected_link = random.choice(available_links)

    # 标记链接为已使用
    used_links.add(selected_link)

    # 将链接添加到已返回的链接列表
    returned_links.append(selected_link)

    return jsonify({'download_link': selected_link})

if __name__ == '__main__':
    app.run(debug=True)

