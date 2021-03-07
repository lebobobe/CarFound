from collections import namedtuple

import bs4
import requests


class AvitoParser:
    def __init__(self):
        self.url = 'https://www.avito.ru'

    def _get_page(self, city: str, category: str = 'avtomobili', model: str = None, radius: int = 0, page: int = None):
        """
        Возвращает html списка объявлений отсортированных по дате
        Все параметры необходимо передавать в нижнем регистре
        """
        url = f'{self.url}/{city}/{category}'
        params = {
            'cd': 1,            # непонятно, есть если не выбрана марка авто
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
        text = self._get_page(city=city)
        soup = bs4.BeautifulSoup(text, 'lxml')
        titles = soup.find_all('div', class_='iva-item-titleStep-2bjuh')
        for item in titles:
            block = item.find('a')
            item_url = f"https://www.avito.ru{block.get('href')}"
            print(item_url)


if __name__ == '__main__':
    parser = AvitoParser()
    parser._get_new_links(city="tomsk")


