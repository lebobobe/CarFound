from webapp.model import db, Advert, Brand, ModelType, FuelType, Transmission, WheelsDrive, Condition, Body, Color, City


class AdvertData:

    def __init__(self, params: dict):
        self.url = params['url']
        self.price = params['price']
        self.publication_date = params['date']
        self.image_url = params['image_url']
        self.engine_volume = params['engine_volume']
        self.horse_power = params['horse_power']
        self.owners = params['owners']
        self.year = params['year']
        self.mileage = params['mileage']
        self.hand_drive = params['is_left_hand_drive']
        self.brand = params['brand']
        self.model = params['model']
        self.fuel_type = params['fuel_type']
        self.transmission = params['transmission']
        self.wheels_drive = params['wheels_drive']
        self.condition = params['condition']
        self.body = params['body']
        self.color = params['color']
        self.city = params['city']

    def add_to_database(self):
        print('Тут будет добавление в БД')

    def __repr__(self):
        return f"<Advert:{self.brand} {self.model}, price: {self.price}, {self.publication_date}, {self.image_url}>"
