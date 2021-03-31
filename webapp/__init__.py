from flask import Flask
from webapp.model import (
    db, Advert, Brand, ModelType, FuelType, Transmission, WheelsDrive, Condition, Body, Color, City
)
from webapp.parsers.parser_avito import AvitoParser


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'CarFound'
        return title

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
