DEFAULT_URL = 'https://auto.ru/cars/used/?page={page}&sort=cr_date-desc&top_days=14'
PAGES_RANGE = 1
MAX_DELAY = 1
MIN_DELAY = 0
FIND_DICT = {
        'brand': 'div > h1 > div > div:nth-child(2) > div > a',
        'model': 'div > h1 > div > div:nth-child(4) > div > a',
        'city': 'span.MetroListPlace__regionName.MetroListPlace_nbsp', 
        'price': 'div.InfoPopup.InfoPopup_theme_plain.InfoPopup_withChildren'
        '.PriceUsedOffer-module__price > span > span', 
        'color': 'li.CardInfoRow.CardInfoRow_color > span:nth-child(2)', 
        'publication_date': 'div[title^="Дата размещения"]',
        'manufactured_year': 'li.CardInfoRow.CardInfoRow_year > span:nth-child(2)', 
        'mileage': 'li.CardInfoRow.CardInfoRow_kmAge > span:nth-child(2)', 
        'body': 'li.CardInfoRow.CardInfoRow_bodytype > span:nth-child(2)', 
        'engine_params': 'li.CardInfoRow.CardInfoRow_engine > span:nth-child(2) > div',
        'transmission_type': 'li.CardInfoRow.CardInfoRow_transmission > span:nth-child(2)',
        'wheels_drive': 'li.CardInfoRow.CardInfoRow_drive > span:nth-child(2)', 
        'is_left_hand_drive': 'li.CardInfoRow.CardInfoRow_wheel > span:nth-child(2)',
        'condition': 'li.CardInfoRow.CardInfoRow_state > span:nth-child(2)',
        'owners': 'li.CardInfoRow.CardInfoRow_ownersCount > span:nth-child(2)', 
        'image_url': 'ImageGalleryDesktop__image'
        }
