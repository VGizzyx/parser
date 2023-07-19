import json
import random
import time
import csv
import requests

headers = {
    'authority': 'web-gateway.middle-api.magnit.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://magnit.ru',
    'referer': 'https://magnit.ru/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-app-version': '0.1.0',
    'x-client-name': 'magnit',
    'x-device-id': 's34jra96em',
    'x-device-platform': 'Web',
    'x-device-tag': 'disabled',
    'x-platform-version': 'window.navigator.userAgent',
}

json_data = {
    'categoryIDs': [
        18433,
        18437,
        18435,
        18123,
        18345,
        18339,
        18343,
        18341,
        5273,
        5275,
        5271,
    ],
    'includeForAdults': True,
    'onlyDiscount': False,
    'order': 'desc',
    'pagination': {
        'number': 1,
        'size': 36,
    },
    'shopType': '6',
    'sortBy': 'price',
    'storeCodes': [
        '992301',
    ],
}

BASE_URL = 'https://web-gateway.middle-api.magnit.ru/v3/goods'


def get_json(url):
    time.sleep(random.randint(3, 5))
    r = requests.post(url, headers=headers, json=json_data)
    print('...')
    if r.status_code == 200:
        return r.json()
    else:
        return "ERROR"


def get_all_goods():
    all_goods = {}
    json = get_json(BASE_URL)
    while json != "ERROR" and len(json.get('goods')) != 0:
        for good in json.get('goods'):
            all_goods[good['name']] = good['offers'][0]['price']
        json_data['pagination']['number'] += 1
        json = get_json(BASE_URL)

    return all_goods


def write_to_csv():
    records = get_all_goods()

    with open('products.csv', 'w', encoding='UTF8') as f:
        w = csv.DictWriter(f, records.keys())
        w.writeheader()
        w.writerow(records)


def ui():
    print("Идет подготовка вашего файла. Пожалуйста, подождите...")
    write_to_csv()
    print("Готово")
ui()