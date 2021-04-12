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
    @app.route('/index')
    def index():
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        adverts = Advert.query.order_by(Advert.date.desc())
        pages = adverts.paginate(page=page, per_page=10)

        return render_template('index.html', pages=pages)

    @app.route('/authentication')
    def authentication():
        return render_template('login.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
