import requests


class AvitoParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'
                'AppleWebKit/537.36 (KHTML, like Gecko)'
                'Chrome/88.0.4324.190 Mobile Safari/537.36'
            ),
            'Accept-Language': 'ru',
        }

    def get_page(self, city: str, category: str = 'avtomobili', model: str = None, page: int = None):
        params = {
            'cd': 1,            # непонятно, есть если не выбрана марка авто
            'radius': 200,      # Радиус поиска вокруг города в км
            's': 104,           # Сортировка (104 по дате, 1 дешевле, 2 дороже)
        }
        if page and page > 1:
            params['p'] = page

        url = f'https://www.avito.ru/{city}/{category}'
        if model:
            url = f'{url}/{model}'

        r = self.session.get(url, params=params)
        return r.text


if __name__ == '__main__':
    parser = AvitoParser()
    print(parser.get_page(city="Tomsk"))

