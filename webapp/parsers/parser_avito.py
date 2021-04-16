from datetime import datetime, timedelta
import logging
import random
import re
from time import sleep
from typing import Optional

import bs4
import requests

from webapp.parsers.advert_data import AdvertData, RepeatedAdvert


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

    def _get_page(self, city: str, model: str = None, radius: int = 0, page: int = None) -> Optional[str]:
        """
        Возвращает html страницы списка объявлений отсортированных по дате
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
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
            }
            r = requests.get(url, params=self.request_parameters, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text
        except (requests.RequestException, ValueError):
            return None

    def _get_new_links(self, city: str) -> Optional[list]:
        """
        заполняет список new_urls ссылками на новые объявления со страницы поиска по city
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

    def _parse_advert_page(self, url: str) -> Optional[dict]:
        """
        Парсит страницу объявления. Создаёт словарь,
        записывает в него все найденные параметры и возвращает
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
        publication_date = soup.find('div', class_='title-info-metadata-item-redesign').text.strip()
        img_url = soup.select('div.gallery-img-frame.js-gallery-img-frame')[0].get('data-url')
        city = soup.find('div', class_='item-navigation').find('span').find('a').find('span').text
        params = soup.find('ul', class_='item-params-list').find_all('li')

        advert = self._create_advert_with_extra_params(params)
        advert['url'] = url
        advert['price'] = int(price)
        advert['date'] = self._set_publication_date(publication_date)
        advert['image_url'] = img_url
        advert['city'] = city
        logging.info(advert)
        return advert

    def _create_advert_with_extra_params(self, params: bs4.ResultSet) -> dict:
        """
        Добавляет в словарь advert с дополнительные параметры авто из объявления
        """
        extra_params = {}

        for param in params:
            name, value = param.text.split(':')
            extra_params[name.strip()] = value.strip()

        advert = {
            'engine_volume': self._parse_engine_volume(extra_params['Модификация']),
            'horse_power': self._parse_horse_power(extra_params['Модификация']),
            'year': int(extra_params['Год выпуска']),
            'is_left_hand_drive': self._parse_hand_drive(extra_params['Руль']),
            'brand': extra_params['Марка'].strip(), 'model': extra_params['Модель'].strip(),
            'fuel_type': extra_params['Тип двигателя'].strip(),
            'transmission': extra_params['Коробка передач'].strip(),
            'wheels_drive': extra_params['Привод'].strip(),
            'body': extra_params['Тип кузова'].strip(), 'color': extra_params['Цвет'].strip()
        }

        try:
            advert['owners'] = extra_params['Владельцев по ПТС']
            advert['condition'] = extra_params['Состояние'].strip()
            advert['mileage'] = int(extra_params['Пробег'].split()[0].strip())
        except KeyError:
            advert['owners'] = '0'
            advert['condition'] = 'новая'
            advert['mileage'] = 0
        return advert

    def _parse_engine_volume(self, modification: str) -> float:
        engine_volume = re.search(r'\d\.\d', modification).group(0)
        return float(engine_volume)

    def _parse_horse_power(self, modification: str) -> int:
        horse_power = re.search(r'[\d]{2,4}\sл\.с\.', modification).group(0)
        horse_power = int(horse_power.replace('л.с.', '').strip())
        return horse_power

    def _parse_hand_drive(self, hand_drive: str) -> bool:
        if 'правый' in hand_drive:
            return False
        return True

    def _set_publication_date(self, publication_date: str) -> datetime:
        now_date = datetime.utcnow()
        publication_str_time = publication_date.split('в')[-1].strip()
        publication_time = datetime.strptime(publication_str_time, '%H:%M')

        if 'вчера' in publication_date:
            now_date -= timedelta(days=1)

        day, month, year = now_date.day, now_date.month, now_date.year
        hour, minute = publication_time.hour, publication_time.minute
        publication_date = datetime(year, month, day, hour, minute)

        return publication_date

    def run(self, city: str):
        """
        Запускает парсинг, находит ссылки с первой страницы поиска отсортированного по времени
        и парсит их поочереди, создаёт объект AdvertData и через него записывает данные в БД
        """
        if not self._get_new_links(city=city):
            raise ValueError("Нет новых объявлений")

        for link in self.new_urls:
            url = f'{self._url}{link}'
            logging.info(url)
            try:
                sleep_time = random.randint(500, 1700)
                sleep(sleep_time/9)
                advert = AdvertData(self._parse_advert_page(url))
            except AttributeError as error:
                logging.info(f'BAD URL {url}', exc_info=error)
                continue

            logging.info(f'Add advert from avito: {advert}')
            try:
                advert.add_to_database()
            except RepeatedAdvert:
                logging.info(f'Repeat advert: {url}')
                break


if __name__ == '__main__':
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', filename='avito_parser.log', level=logging.INFO)
    parser = AvitoParser()
    parser.run(city="rossiya")
