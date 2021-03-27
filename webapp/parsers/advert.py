from datetime import datetime, timedelta


class Advert:
    url = None
    price = None
    currency = None
    publication_date = None
    image_url = None
    brand = None
    model = None
    engine_volume = None
    horse_power = None
    fuel_type = None
    transmission = None
    wheels_drive = None
    condition = None
    owners = None
    year = None
    mileage = None
    body = None
    color = None
    city = None
    hand_drive = None

    def __init__(self, url):
        self.url = url

    def set_img_url(self, url: str):
        self.image_url = url

    def set_price(self, price: int, currency: str):
        self.price = price
        self.currency = currency

    def set_publication_date(self, publication_date: str) -> datetime:
        now_date = datetime.utcnow()
        publication_str_time = publication_date.split('в')[-1].strip()
        publication_time = datetime.strptime(publication_str_time, '%H:%M')

        if 'вчера' in publication_date:
            now_date -= timedelta(days=1)

        day, month, year = now_date.day, now_date.month, now_date.year
        hour, minute = publication_time.hour, publication_time.minute

        publication_date = datetime(year, month, day, hour, minute)

        self.publication_date = publication_date
        return self.publication_date

    def set_params(self, params: list):
        avito_params = {
            'Марка': self._set_brand,
            'Модель': self._set_model,
            # 'Поколение': 'E30 (1982—1991)',
            'Модификация': self._set_modification,
            'Год выпуска': self._set_year,
            'Пробег': self._set_mileage,
            'Состояние': self._set_condition,
            'Владельцев по ПТС': self._set_owners,
            'Тип кузова': self._set_body,
            # 'Количество дверей': 4,
            'Тип двигателя': self._set_fuel_type,
            'Коробка передач': self._set_transmission,
            'Привод': self._set_wheels_drive,
            'Руль': self._set_hand_drive,
            'Цвет': self._set_color,
            # 'Комплектация': 'Базовая'
        }
        for param in params:
            name, value = param
            try:
                avito_params[name.strip()](value.strip())
            except KeyError:
                pass  # необрабатываемые параметры

    def set_address(self, address):
        city = address.split(',')[0].strip()
        self._set_city(city)

    def _set_modification(self, modification):
        engine_volume = float(modification.split()[0])
        horse_power = int(modification.split('(')[-1].strip().split()[0])
        self._set_engine_volume(engine_volume)
        self._set_horse_power(horse_power)

    def _set_brand(self, brand):
        self.brand = brand

    def _set_model(self, model):
        self.model = model

    def _set_engine_volume(self, engine_volume):
        self.engine_volume = float(engine_volume)

    def _set_horse_power(self, horse_power):
        self.horse_power = int(horse_power)

    def _set_fuel_type(self, fuel_type):
        self.fuel_type = fuel_type

    def _set_transmission(self, transmission):
        self.transmission = transmission

    def _set_wheels_drive(self, wheels_drive):
        self.wheels_drive = wheels_drive

    def _set_condition(self, condition):
        self.condition = condition

    def _set_owners(self, owners):
        self.owners = owners

    def _set_year(self, year):
        self.year = int(year)

    def _set_mileage(self, mileage):
        mileage = mileage.split()[0].strip()
        self.mileage = int(mileage)

    def _set_body(self, body):
        self.body = body

    def _set_color(self, color):
        self.color = color

    def _set_city(self, city):
        self.city = city

    def _set_hand_drive(self, hand_drive):
        self.hand_drive = hand_drive

    def get_params(self):
        return (
            self.url, self.price, self.currency, self.publication_date, self.image_url,
            self.brand, self.model, self.engine_volume, self.horse_power, self.fuel_type,
            self.transmission, self.wheels_drive, self.condition, self.owners, self.year,
            self.mileage, self.body, self.color, self.city, self.hand_drive,
        )

    def __repr__(self):
        return f"<Advert:{self.brand} {self.model}, price: {self.price}{self.currency}, {self.publication_date}, {self.image_url}>"
