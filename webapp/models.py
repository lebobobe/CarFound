from flask_sqlalchemy import SQLAlchemy

from webapp import config

db = SQLAlchemy()


class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('ModelType.id'), nullable=False)
    engine_volume = db.Column(db.Float, index=True, nullable=False)
    horse_power = db.Column(db.Integer, index=True, nullable=False)
    fuel_type_id = db.Column(db.Integer, db.ForeignKey('FuelType.id'), nullable=False)
    transmission_id = db.Column(db.Integer, db.ForeignKey('Transmission.id'), nullable=False)
    wheels_drive_id = db.Column(db.Integer, db.ForeignKey('WheelsDrive.id'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('Condition.id'), nullable=False)
    owners = db.Column(db.String(2), nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    mileage = db.Column(db.Integer, index=True, nullable=False)
    body_id = db.Column(db.Integer, db.ForeignKey('Body.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('Color.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)

    def __repr__(self):
        return f"<Advert:{self.id}: {self.model_id} {self.year}y, price={self.price}>"


class Params(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"<{self.id}: {self.__tablename__} {self.name}>"


class ModelType(Params):
    __tablename__ = 'ModelType'
    brand_id = db.Column(db.Integer, db.ForeignKey('Brand.id'), nullable=False)


class Brand(Params):
    __tablename__ = 'Brand'
    addresses = db.relationship('Model', backref='brand', lazy=True)


class FuelType(db.Model):
    __tablename__ = 'FuelType'


class Transmission(db.Model):
    __tablename__ = 'Transmission'


class WheelsDrive(db.Model):
    __tablename__ = 'WheelsDrive'


class Condition(db.Model):
    __tablename__ = 'Condition'


class Body(db.Model):
    __tablename__ = 'Body'


class Color(db.Model):
    __tablename__ = 'Color'


class City(db.Model):
    __tablename__ = 'City'


