from webapp.models import (
    db, get_or_create, Advert, Brand, ModelType, FuelType,
    Transmission, WheelsDrive, Condition, Body, Color, City
)


class RepeatedAdvert(Exception):
    def __init__(self, text):
        self.txt = text


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
        from webapp import create_app
        app = create_app()
        app.app_context().push()

        if db.session.query(Advert).filter(Advert.url == self.url).count() > 0:
            raise RepeatedAdvert

        brand = get_or_create(db.session, Brand, name=self.brand)
        model = get_or_create(db.session, ModelType, name=self.model, brand_id=brand.id)
        fuel_type = get_or_create(db.session, FuelType, name=self.fuel_type)
        transmission = get_or_create(db.session, Transmission, name=self.transmission)
        wheels_drive = get_or_create(db.session, WheelsDrive, name=self.wheels_drive)
        condition = get_or_create(db.session, Condition, name=self.condition)
        body = get_or_create(db.session, Body, name=self.body)
        color = get_or_create(db.session, Color, name=self.color)
        city = get_or_create(db.session, City, name=self.city)

        advert = Advert(
            url=self.url,
            price=self.price,
            date=self.publication_date,
            image_url=self.image_url,
            engine_volume=self.engine_volume,
            horse_power=self.horse_power,
            owners=self.owners,
            year=self.year,
            mileage=self.mileage,
            is_left_hand_drive=self.hand_drive,

            model_id=model.id,
            fuel_type_id=fuel_type.id,
            transmission_id=transmission.id,
            wheels_drive_id=wheels_drive.id,
            condition_id=condition.id,
            body_id=body.id,
            color_id=color.id,
            city_id=city.id
        )
        db.session.add(advert)
        db.session.commit()

    def __repr__(self):
        return f"<Advert:{self.brand} {self.model}, price: {self.price}, {self.publication_date}, {self.image_url}>"
