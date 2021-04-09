from flask import Flask, render_template
from webapp.models import (
    db, Advert, Brand, ModelType, FuelType, Transmission, WheelsDrive, Condition, Body, Color, City
)
from webapp.parsers.parser_avito import AvitoParser


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    @app.route('/index')
    def index():
        # volumes = [round(x * 0.2, 1) for x in range(1, 40)]
        adverts = db.session.query(Advert).all()
        print(adverts)
        volumes = []

        for advert in adverts:
            advert_data = {
                'brand': advert.model.brand.name,
                'model': advert.model.name,
                'price': advert.price,
                'city': advert.city.name,
                'year': advert.year,
                'mileage': advert.mileage,
                'volume': advert.engine_volume,
                'hp': advert.horse_power,
                'fuel_type': advert.fuel_type.name,
                'transmission': advert.transmission.name,
                'WD': advert.wheels_drive.name,
                'wheel_drive': 'Левый' if advert.is_left_hand_drive else 'Правый',
                'body': advert.body.name,
                'color': advert.color.name,
                'condition': advert.condition.name,
                'owners': advert.owners,
                'pic_url': advert.image_url,
                'listing_url': advert.url
            }
            volumes.append(advert_data)
        print(volumes)

        return render_template('index.html', len=len(volumes), volumes=volumes)

    @app.route('/authentication')
    def authentication():
        return render_template('login.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
