DEFAULT_URL = 'https://auto.ru/cars/used/?page={PAGES_RANGE}&sort=cr_date-desc&top_days=14'
PAGES_RANGE = 2
MAX_DELAY = 3
MIN_DELAY = 0
FIND_LIST = [
            'div > h1 > div > div:nth-child(2) > div > a',
            'div > h1 > div > div:nth-child(4) > div > a',
            'span.MetroListPlace__regionName.MetroListPlace_nbsp',
            'div.InfoPopup.InfoPopup_theme_plain.InfoPopup_withChildren'
            '.PriceUsedOffer-module__price > span > span',
            'li.CardInfoRow.CardInfoRow_color > span:nth-child(2)',
            'div[title^="Дата размещения"]',
            'li.CardInfoRow.CardInfoRow_year > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_kmAge > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_bodytype > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_engine > span:nth-child(2) > div',
            'li.CardInfoRow.CardInfoRow_transmission > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_drive > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_wheel > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_state > span:nth-child(2)',
            'li.CardInfoRow.CardInfoRow_ownersCount > span:nth-child(2)',
            ]
KEYS = ['brand', 'model', 'city', 'price', 'color', 'publication_date',
        'manufactured_year', 'mileage', 'body', 'engine_volume', 'horse_power',
        'fuel_type', 'transmission_type', 'wheels_drive', 'is_left_hand_drive',
        'condition', 'owners', 'image_url']
