from bs4 import BeautifulSoup
import requests
import autoru_config
from time import sleep
from random import uniform
from datetime import datetime


class AutoruParser:

    def __init__(self):
        self.max_page = autoru_config.PAGES_RANGE
        self.min_delay = autoru_config.MIN_DELAY
        self.max_delay = autoru_config.MAX_DELAY
        self.urls_to_parse = []
        self.listings = []
        self.url = 'https://auto.ru/cars/used/'
        self.page = 1
        self.links_class = {"class": "Link ListingItemTitle-module__link"}
        self.months = autoru_config.MONTHS

    def handler(self, listing):
        """
        Добавляет новые параметры для двигателя,
        приводит все параметры к принятому в проекте виду.
        """
        listing['engine_volume'] = None
        listing['horse_power'] = None
        listing['fuel_type'] = None
        for k, v in listing.items():
            if v == 'роботизированная':
                listing[k] = 'робот'

            elif k == 'owners':
                if v == '3 или более':
                    listing[k] = '3+'
                else:
                    listing[k] = v.strip(' ')[0]

            elif k == 'price':
                listing[k] = int(v.replace('₽', ''))

            elif v == 'Левый':
                listing[k] = True
            elif v == 'Правый':
                listing[k] = False

            elif k == 'mileage':
                listing[k] = int(v.replace('км', ''))

            elif k == 'body':
                listing[k] = v.split(' ')[0]

            elif k == 'engine_params':
                values = v.split(' / ')
                for param in values:
                    if ' л' in param:
                        listing['engine_volume'] = float(param.split(' ')[0])
                    elif 'л.с.' in param:
                        listing['horse_power'] = int(param.replace('л.с.', ''))
                    else:
                        listing['fuel_type'] = param.strip()

            elif k == 'price' or k == 'year':
                listing[k] = int(v)

            elif k == 'fuel_type':
                if 'оборудование' in v:
                    listing[k] = 'газ'
                listing[k] = v.lower()

            elif v == 'Не требует ремонта':
                    listing[k] = 'не битый'
            elif v == 'Битый / не на ходу':
                listing[k] = 'битый'

            elif k == 'date':
                for dk, dv in autoru_config.MONTHS.items():
                    if dk == v.split(' ')[1]:
                        listing[k] = v.split(' ')[0] + '/' + str(dv)
                date_now = datetime.now()
                publicate_date = datetime.strptime(listing.get('date'), '%d/%m')
                month, day = publicate_date.month, publicate_date.day
                year, hour, minute = date_now.year, date_now.hour, date_now.minute
                publication_date = datetime(year, month, day, hour, minute)
                listing[k] = publication_date
        del listing['engine_params']

    def get_image(self, soup, listing):
        images = soup.select('img.ImageGalleryDesktop__image')
        for image in images:
            string_image = str(image)
            if 'avatars' in string_image:
                listing['image_url'] = f"https:{image['src']}"
                break

    def get_links(self):
        """
        Проходит по указанному диапазону страниц и
        собирает ссылки на обьявления с каждой из них
        """
        while self.page <= self.max_page:
            delay = uniform(self.min_delay, self.max_delay)
            params = {'page': self.page,
                      'sort': 'cr_date-desc',
                      'top_days': '14'}
            try:
                response = requests.get(self.url, params=params)
                response.raise_for_status()
                response.encoding = 'utf-8'
            except (requests.RequestException, ValueError):
                continue
            soup = BeautifulSoup(response.text, 'lxml')
            all_links = soup.find_all('a', self.links_class, href=True)
            for listing_title in all_links:
                self.urls_to_parse.append(listing_title['href'])
            print(f'Страница номер {self.page} пройдена')
            print(f'Задержка {delay} с.')
            sleep(delay)
            self.page += 1

    def get_specs(self, soup, url):
        """
        Получает на вход ссылку на обьявление, парсит параметры из обьявления,
        вызывает обработчик параметров и записывает результаты работы.
        """
        listing = {}
        listing['url'] = url
        for key, value in autoru_config.FIND_DICT.items():
            if key == 'image_url':
                self.get_image(soup, listing)
                continue
            results = soup.select(value)
            for result in results:
                result = result.text
                listing[key] = result.replace('\xa0', '')
        self.handler(listing)
        print(listing)
        self.listings.append(listing)

    def check_urls(self):
        """
        Проходит по списку собранных методом get_links ссылок,
        вызывает для каждой ссылки check_url
        """
        for url in self.urls_to_parse:
            self.check_url(url)

    def check_url(self, url):
        """
        Делает запрос на страницу обьявления и вызывает get_specs
        """
        waiting = uniform(self.min_delay, self.max_delay)
        try:
            response = requests.get(url)
            response.raise_for_status()
            response.encoding = 'utf-8'
        except (requests.RequestException, ValueError):
            return
        soup = BeautifulSoup(response.text, 'lxml')
        self.get_specs(soup, url)
        print(f'Обьяление добавлено в список. Жду {waiting} с.')
        sleep(waiting)

    def run(self):
        """
        Запускает метод получения ссылок на обьявления,
        после получения всех ссылок запускается их обработка.
        """
        self.get_links()
        self.check_urls()


if __name__ == '__main__':
    parser = AutoruParser()
    parser.run()
