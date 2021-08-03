from bs4 import BeautifulSoup
import requests
import lxml
import unicodedata
import time
import json
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.275'
}
all_data = [ ]
for number_page in range(1, 17):
    url = f'https://www.labirint.ru/genres/2308/?display=table&page={number_page}'
    req = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')
    all_items = soup.find(class_='products-table__body').find_all('tr')
    for components in range(0, len(all_items)):
        try:
            name = all_items [ components ].find(class_='book-qtip').get('title')
        except:
            name = 'none name'
        try:
            author = all_items [ components ].find(class_='col-sm-2').find(class_='mt3').text
            author=author.replace(u'\xa0', u'')
        except:

            author = 'none author'
        try:
            publisher_series = all_items [ components ].find(class_='products-table__pubhouse').find_all('a')
            try:
                publisher_series = publisher_series [ 0 ].text + ':' + publisher_series [ 1 ].text
            except:
                publisher_series = publisher_series [ 0 ].text

        except:
            author = 'none publisher_series'
        try:
            new_price = all_items [ components ].find(class_='price-val').find('span').text.replace(' ', '')
        except:

            new_price = 'None'
        try:
            old_price = all_items [ components ].find('span', class_='price-old').find('span', class_="price-gray")
            old_price = old_price.text
            old_price = old_price.replace(' ', '')
        except:
            old_price = 'Нет старой цены'
        try:
            Availability = all_items [ components ].find('td', class_='product-table__available').find('div', class_="mt3 rang-available")
            Availability = Availability.text.replace(u'\xa0', u'')

        except:
            Availability='Неизвестно'

        if old_price != 'Нет старой цены':
            dis = int(old_price) - int(new_price)
            discount = round(dis / int(old_price) * 100)

            data = {
                'name': name,
                'author': author,
                'publisher_series': publisher_series,
                'old_price': old_price,
                'new_price': new_price,
                'discount': f"{discount}%",
                'Availability':Availability

            }

        else:
            data = {
                'name': name,
                'author': author,
                'publisher_series': publisher_series,
                'new_price': new_price,
                'Availability': Availability

            }

        all_data.append(data)
    time.sleep(1)
    print(f'Обработана страница номер:{number_page}')
print(all_data)
with open('data/all_data.json','w',encoding='utf-8') as file:
    json.dump(all_data,file,ensure_ascii=False,indent=4)