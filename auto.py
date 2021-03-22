from bs4 import BeautifulSoup
import requests
import autoru_config
from time import sleep
from random import uniform


def get_specs():
    for selector in autoru_config.FIND_LIST:
        results = soup.select(selector)
        for result in results:
            result = result.text
            if '/' in result:
                engine_specs = result.split('/')
                for spec in engine_specs:
                    params.append(spec.replace('\xa0', ' ').strip())
            else:
                params.append(result.replace('\xa0', ' '.strip()))


def get_image():
    images = soup.find_all(class_='ImageGalleryDesktop__image')
    for image in images:
        if 'Panorama' in str(image):
            pass
        elif 'avatars' in str(image):
            params.append((image['src'])[2::])
            pass


urls_to_parse = []


def get_links():
    for x in range(autoru_config.PAGES_RANGE):
        delay = uniform(autoru_config.MIN_DELAY, autoru_config.MAX_DELAY)
        try:
            response = requests.get(autoru_config.DEFAULT_URL)
            response.raise_for_status()
            response.encoding = 'utf-8'
        except (requests.RequestException, ValueError):
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        all_listings = soup.find_all('a', {"class": "Link ListingItemTitle-module__link"}, href=True)
        for i in all_listings:
            urls_to_parse.append(i['href'])
        print(f'Страница номер {autoru_config.PAGES_RANGE} пройдена')
        print(f'Задержка {delay} с.')
        sleep(delay)
        autoru_config.PAGES_RANGE -= 1
    return(urls_to_parse, len(urls_to_parse))


listings = []
get_links()

for url in urls_to_parse:
    params = []
    waiting = uniform(autoru_config.MIN_DELAY, autoru_config.MAX_DELAY)
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except (requests.RequestException, ValueError):
        print(None)
    soup = BeautifulSoup(response.text, 'lxml')
    get_specs()
    get_image()
    listings.append(dict(zip(autoru_config.KEYS, params)))
    print(f'Обьяление добавлено в список. Жду {waiting} с.')
    sleep(waiting)
