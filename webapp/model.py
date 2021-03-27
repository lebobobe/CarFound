from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ModelType(db.Model):
    __tablename__ = 'modeltypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    brand = db.relationship('brands', backref='model_types')


class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class FuelType(db.Model):
    __tablename__ = 'fueltypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class Transmission(db.Model):
    __tablename__ = 'transmissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class WheelsDrive(db.Model):
    __tablename__ = 'wheelsdrives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class Body(db.Model):
    __tablename__ = 'bodies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)


class Advert(db.Model):
    __tablename__ = 'adverts'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
    image_url = db.Column(db.String(255))
    engine_volume = db.Column(db.Float, index=True, nullable=False)
    horse_power = db.Column(db.Integer, index=True, nullable=False)
    owners = db.Column(db.String(2), nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    mileage = db.Column(db.Integer, index=True, nullable=False)
    is_left_hand_drive = db.Column(db.Boolean, nullable=False)

    model_id = db.Column(db.Integer, db.ForeignKey('modeltypes.id'), nullable=False)
    model = db.relationship('modeltype', backref='adverts')

    fuel_type_id = db.Column(db.Integer, db.ForeignKey('fueltypes.id'), nullable=False)
    fuel_type = db.relationship('fueltype', backref='adverts')

    transmission_id = db.Column(db.Integer, db.ForeignKey('transmissions.id'), nullable=False)
    transmission = db.relationship('transmission', backref='adverts')

    wheels_drive_id = db.Column(db.Integer, db.ForeignKey('wheelsdrives.id'), nullable=False)
    wheels_drive = db.relationship('wheelsdrive', backref='adverts')

    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), nullable=False)
    condition = db.relationship('condition', backref='adverts')

    body_id = db.Column(db.Integer, db.ForeignKey('bodies.id'), nullable=False)
    body = db.relationship('body', backref='adverts')

    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    color = db.relationship('color', backref='adverts')

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    city = db.relationship('city', backref='adverts')

    def __repr__(self):
        return f"<Advert:{self.id}: {self.model_id} {self.year}y, price={self.price}>"
