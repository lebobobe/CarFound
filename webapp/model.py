from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ModelType(db.Model):
    __tablename__ = 'modeltype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    addresses = db.relationship('advert', backref='modeltype', lazy=True)


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('modeltype', backref='brand', lazy=True)


class FuelType(db.Model):
    __tablename__ = 'fueltype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='fueltype', lazy=True)


class Transmission(db.Model):
    __tablename__ = 'transmission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='transmission', lazy=True)


class WheelsDrive(db.Model):
    __tablename__ = 'wheelsdrive'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='wheelsdrive', lazy=True)


class Condition(db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='condition', lazy=True)


class Body(db.Model):
    __tablename__ = 'body'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='body', lazy=True)


class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='color', lazy=True)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('advert', backref='city', lazy=True)


class Advert(db.Model):
    __tablename__ = 'advert'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('modeltype.id'), nullable=False)
    engine_volume = db.Column(db.Float, index=True, nullable=False)
    horse_power = db.Column(db.Integer, index=True, nullable=False)
    fuel_type_id = db.Column(db.Integer, db.ForeignKey('fueltype.id'), nullable=False)
    transmission_id = db.Column(db.Integer, db.ForeignKey('transmission.id'), nullable=False)
    wheels_drive_id = db.Column(db.Integer, db.ForeignKey('wheelsdrive.id'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'), nullable=False)
    owners = db.Column(db.String(2), nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    mileage = db.Column(db.Integer, index=True, nullable=False)
    body_id = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return f"<Advert:{self.id}: {self.model_id} {self.year}y, price={self.price}>"