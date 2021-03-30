from bs4 import BeautifulSoup
import requests
import autoru_config
from time import sleep
from random import uniform


class AutoruParser:

    def __init__(self):
        self.max_page = autoru_config.PAGES_RANGE
        self.min_delay = autoru_config.MIN_DELAY
        self.max_delay = autoru_config.MAX_DELAY
        self.urls_to_parse = []
        self.listings = []
        self.page = 1

    def get_links(self):
        while self.page <= self.max_page:
            self.url = f'https://auto.ru/cars/used/?page={self.page}&sort=cr_date-desc&top_days=14'
            delay = uniform(self.min_delay, self.max_delay)
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                response.encoding = 'utf-8'
            except (requests.RequestException, ValueError):
                return None
            soup = BeautifulSoup(response.text, 'lxml')
            all_links = soup.find_all('a', {"class": "Link ListingItemTitle-module__link"}, href=True)
            for listing_title in all_links:
                self.urls_to_parse.append(listing_title['href'])
            print(f'Страница номер {self.page} пройдена')
            print(f'Задержка {delay} с.')
            sleep(delay)
            self.page += 1

    def get_image(self, soup, listing, key):
        images = soup.find_all(class_=autoru_config.FIND_DICT['image_url'])
        for image in images:
            if 'avatars' in str(image):
                listing[key] = image['src'][2:]
                continue
        return listing

    def get_specs(self, soup):
        listing = {}
        for key, value in autoru_config.FIND_DICT.items():
            if key == 'image_url':
                self.get_image(soup, listing, key)
            else:
                results = soup.select(value)
                for result in results:
                    result = result.text
                    listing[key] = result.replace('\xa0', ' ')
        self.listings.append(listing)

    def check_url(self, url):
        waiting = uniform(self.min_delay, self.max_delay)
        try:
            response = requests.get(url)
            response.raise_for_status()
            response.encoding = 'utf-8'
        except (requests.RequestException, ValueError):
            print(None)
        soup = BeautifulSoup(response.text, 'lxml')
        self.get_specs(soup)
        print(f'Обьяление добавлено в список. Жду {waiting} с.')
        sleep(waiting)

    def check_urls(self):
        for url in self.urls_to_parse:
            self.check_url(url)

    def run(self):
        self.get_links()
        self.check_urls()


if __name__ == '__main__':
    parser = AutoruParser()
    parser.run()
