from collections import defaultdict

import bs4
import requests


class Advert:
    title = None
    price = None
    currency = None
    publication_date = None
    params = defaultdict(str)

    def __init__(self, url):
        self.url = url

    def set_title(self, title: str):
        self.title = title

    def set_price(self, price: int, currency: str):
        self.price = price
        self.currency = currency

    def set_publication_date(self, publication_date: str):
        self.publication_date = publication_date    # надо добавить переработку в datetime

    def set_params(self, params: bs4.ResultSet):
        for param in params:
            name, value = param.text.split(':')
            self.params[name.strip()] = value.strip()


class AvitoParser:
    category = 'avtomobili'
    params = {
        'cd': 1,  # непонятно что это, но есть только если не выбрана марка авто
        'radius': 0,  # Радиус поиска вокруг города в км
        's': 104,  # Сортировка (104 по дате, 1 дешевле, 2 дороже)
    }

    def __init__(self):
        self._url = 'https://www.avito.ru'
        self.new_urls = []
        self.adverts = defaultdict(Advert)

    def _get_page(self, city: str, model: str = None, radius: int = 0, page: int = None):
        """
        Возвращает html списка объявлений отсортированных по дате
        Все параметры необходимо передавать в нижнем регистре
        """
        url = f'{self._url}/{city}/{self.category}'
        self.params['radius'] = radius

        if page and page > 1:
            self.params['p'] = page

        if model:
            url = f'{url}/{model}'
            self.params.pop('cd')    # когда добавляется модель из url пропадает параметр сd

        try:
            r = requests.get(url, params=self.params)
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
        # date = soup.find_all('span', class_='tooltip-target-wrapper-XcPdv') # тут надпись по типу (3 минуты назад)

        for item in titles:
            url = item.find('a').get('href')
            self.new_urls.append(url)

        return self.new_urls

    def _parse_advert_page(self, url: str) -> defaultdict or None:
        """
        Парсит страницу объявления. Создаёт объект объявления, записывает в него все найденные параметры
        и добавляет в словарь self.adverts
        """
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = 'utf-8'
        except (requests.RequestException, ValueError):
            return None

        soup = bs4.BeautifulSoup(r.text, 'lxml')
        title = soup.find('span', class_='title-info-title-text').text.strip()
        price = soup.find('span', class_='js-item-price').get('content')
        currency = soup.find('span', class_='price-value-prices-list-item-currency_sign').span.text.strip()
        publication_date = soup.find('div', class_='title-info-metadata-item-redesign').text.strip()
        params = soup.find('ul', class_='item-params-list').find_all('li')

        advert = Advert(url)
        advert.set_title(title)
        advert.set_price(int(price), currency)
        advert.set_publication_date(publication_date)
        advert.set_params(params)

        self.adverts[url] = advert
        return self.adverts

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
            self._parse_advert_page(url)
            break   # пока обрабатываем одну ссылку
        for advert_url, advert_param in self.adverts.items():
            print('url', advert_url)
            print('param:', advert_param.params)


if __name__ == '__main__':
    parser = AvitoParser()
    parser.run(city="rossiya")


