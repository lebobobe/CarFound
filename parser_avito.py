from collections import defaultdict
import time

import bs4
import requests


class Advert:
    title = None
    params = defaultdict(str)

    def __init__(self, url):
        self.url = url

    def set_params(self, tag: str):
        name, value = tag.split(':')
        self.params[name.strip()] = value.strip()


class AvitoParser:
    def __init__(self):
        self._url = 'https://www.avito.ru'
        self.adverts = defaultdict(Advert)

    def _get_page(self, city: str, category: str = 'avtomobili', model: str = None, radius: int = 0, page: int = None):
        """
        Возвращает html списка объявлений отсортированных по дате
        Все параметры необходимо передавать в нижнем регистре
        """
        url = f'{self._url}/{city}/{category}'
        params = {
            'cd': 1,            # непонятно что это, но есть только если не выбрана марка авто
            'radius': radius,   # Радиус поиска вокруг города в км
            's': 104,           # Сортировка (104 по дате, 1 дешевле, 2 дороже)
        }

        if page and page > 1:
            params['p'] = page

        if model:
            url = f'{url}/{model}'
            params.pop('cd')

        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            return r.text
        except (requests.RequestException, ValueError):
            return False

    def _get_new_links(self, city: str):
        """
        заполняет список links ссылками на новые объявления c первой страницы в городе city
        """
        text = self._get_page(city=city)
        # time.sleep(5)
        soup = bs4.BeautifulSoup(text, 'lxml')
        titles = soup.find_all('div', class_='iva-item-titleStep-2bjuh')
        for item in titles:
            url = item.find('a').get('href')
            self.adverts[url] = Advert(url)
        for link in self.adverts:
            url = f'{self._url}{link}'
            print(url)
            self._parse_advert_page(url)
            break

        return True

    def run(self, city: str):
        self._get_new_links(city=city)
        for advert_url, advert_param in self.adverts.items():
            # print(advert_url)
            # print(advert_param.params)
            pass


    def _parse_advert_page(self, url):
        r = requests.get(url)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        title = soup.find('span', class_='title-info-title-text')
        print(title.text)
        params = soup.find('ul', class_='item-params-list').find_all('li')
        print(params)
        for param in params:
            print(type(param))
            print(param.text)
            print(param.text.split(':'))
            self.adverts[]





if __name__ == '__main__':
    parser = AvitoParser()
    parser.run(city="tomsk")


