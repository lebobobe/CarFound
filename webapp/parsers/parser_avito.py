from collections import defaultdict
import logging

import bs4
import requests

from webapp.parsers.advert import Advert


class AvitoParser:
    category = 'avtomobili'
    request_parameters = {
        'cd': 1,  # непонятно что это, но есть только если не выбрана марка авто
        'radius': 0,  # Радиус поиска вокруг города в км
        's': 104,  # Сортировка (104 по дате, 1 дешевле, 2 дороже)
    }

    def __init__(self):
        self._url = 'https://www.avito.ru'
        self.new_urls = []
        self.adverts = defaultdict(Advert)
        self.advert_params = []

    def _get_page(self, city: str, model: str = None, radius: int = 0, page: int = None) -> str or None:
        """
        Возвращает html списка объявлений отсортированных по дате
        Все параметры необходимо передавать в нижнем регистре
        """
        url = f'{self._url}/{city}/{self.category}'
        self.request_parameters['radius'] = radius

        if page and page > 1:
            self.request_parameters['p'] = page

        if model:
            url = f'{url}/{model}'
            self.request_parameters.pop('cd')  # когда добавляется модель из url пропадает параметр сd

        try:
            r = requests.get(url, params=self.request_parameters)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text
        except (requests.RequestException, ValueError):
            return None

    def _get_new_links(self, city: str) -> list or None:
        """
        заполняет список links ссылками на новые объявления c первой страницы поиска по city
        """
        text = self._get_page(city=city)

        if not text:
            return None

        soup = bs4.BeautifulSoup(text, 'lxml')
        titles = soup.find_all('div', class_='iva-item-titleStep-2bjuh')

        for item in titles:
            url = item.find('a').get('href')
            self.new_urls.append(url)

        return self.new_urls

    def _parse_advert_page(self, url: str) -> Advert or None:
        """
        Парсит страницу объявления. Создаёт объект объявления, записывает в него все найденные параметры
        и возвращает
        """
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = 'utf-8'
        except (requests.RequestException, ValueError) as exc:
            logging.info(f'BAD URL {url}', exc_info=exc)
            return None

        soup = bs4.BeautifulSoup(r.text, 'lxml')
        price = soup.find('span', class_='js-item-price').get('content')
        currency = soup.find('span', class_='price-value-prices-list-item-currency_sign').span.text.strip()
        publication_date = soup.find('div', class_='title-info-metadata-item-redesign').text.strip()
        img_url = soup.select('div.gallery-img-frame.js-gallery-img-frame')[0].get('data-url')
        params = soup.find('ul', class_='item-params-list').find_all('li')
        address = soup.find('span', class_='item-address__string').text

        advert = Advert(url)
        advert.set_img_url(img_url)
        advert.set_price(int(price), currency)
        advert.set_publication_date(publication_date)
        advert.set_params(self._pars_params(params))
        advert.set_address(address)
        print(advert)
        return advert

    def _pars_params(self, params: bs4.ResultSet) -> list:
        self.advert_params = []
        for param in params:
            name, value = param.text.split(':')
            self.advert_params.append((name.strip(), value.strip()))
        return self.advert_params

    def run(self, city: str):
        """
        Запускает парсинг, находит ссылки с первой страницы поиска отсортированного по времени
        и парсит самое новое объявление, создаёт объект Advert и сохраняет в него данные по объявлению
        Добавляет в словарь с объявлениями где ключ url а значение объект Advert
        """
        if not self._get_new_links(city=city):
            raise ValueError("Нет новых объявлений")

        for link in self.new_urls:
            url = f'{self._url}{link}'
            print(url)
            self.adverts[url] = self._parse_advert_page(url)
            print()
            print(self.adverts[url].get_params())
            break  # пока обрабатываем одну ссылку


if __name__ == '__main__':
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', filename='parser.log', level=logging.INFO)
    parser = AvitoParser()
    parser.run(city="rossiya")
