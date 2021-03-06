from flask import Flask, render_template, request
from webapp.models import (
    db, Advert, Brand, ModelType, FuelType, Transmission, WheelsDrive, Condition, Body, Color, City
)
from webapp.parsers.parser_avito import AvitoParser


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    @app.route('/index', methods=['GET', 'POST'])
    def index():
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        brands = Brand.query.all()
        model_types = ModelType.query.all()
        transmissions = Transmission.query.all()
        cities = City.query.all()
        colors = Color.query.all()
        wheels_drives = WheelsDrive.query.all()
        bodies = Body.query.all()
        conditions = Condition.query.all()

        adverts = Advert.query.order_by(Advert.date.desc())
        pages = adverts.paginate(page=page, per_page=12)

        volumes = [round(x * 0.1, 1) for x in range(2, 80)]

        return render_template(
            'index.html', brands=brands, model_types=model_types, transmissions=transmissions,
            cities=cities, colors=colors, wheels_drives=wheels_drives, bodies=bodies,
            conditions=conditions, pages=pages, volumes=volumes
        )

    @app.route('/authentication')
    def authentication():
        return render_template('login.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
