from bs4 import BeautifulSoup
import requests
import autoru_config
from time import sleep
from random import uniform


class AutoruParser:

    def __init__(self):
        self.url = autoru_config.DEFAULT_URL
        self.max_page = autoru_config.PAGES_RANGE
        self.page = 1
        self.urls_to_parse = []
        self.listings = []

    def get_links(self):
        while self.page <= autoru_config.PAGES_RANGE:
            delay = uniform(autoru_config.MIN_DELAY, autoru_config.MAX_DELAY)
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
        return self.urls_to_parse

    def get_image(self, soup, listing, key):
        images = soup.find_all(class_=autoru_config.FIND_DICT['image_url'])
        for image in images:
            string_image = str(image)
            if 'Panorama' in string_image:
                continue
            elif 'avatars' in string_image:
                listing[key] = image['src'][2::]
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
        return self.listings

    def check_urls(self):
        for url in self.urls_to_parse:
            waiting = uniform(autoru_config.MIN_DELAY, autoru_config.MAX_DELAY)
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

    def run(self):
        self.get_links()
        self.check_urls()


if __name__ == '__main__':
    parser = AutoruParser()
    parser.run()
