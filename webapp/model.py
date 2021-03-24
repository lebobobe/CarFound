from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ModelType(db.Model):
    __tablename__ = 'modeltypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    addresses = db.relationship('adverts', backref='modeltypes', lazy=True)


class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('modeltypes', backref='brands', lazy=True)


class FuelType(db.Model):
    __tablename__ = 'fueltypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='fueltypes', lazy=True)


class Transmission(db.Model):
    __tablename__ = 'transmissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='transmissions', lazy=True)


class WheelsDrive(db.Model):
    __tablename__ = 'wheelsdrives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='wheelsdrives', lazy=True)


class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='conditions', lazy=True)


class Body(db.Model):
    __tablename__ = 'bodies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='bodies', lazy=True)


class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='colors', lazy=True)


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    addresses = db.relationship('adverts', backref='cities', lazy=True)


class Advert(db.Model):
    __tablename__ = 'adverts'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
    image_url = db.Column(db.String(255))
    model_id = db.Column(db.Integer, db.ForeignKey('modeltypes.id'), nullable=False)
    engine_volume = db.Column(db.Float, index=True, nullable=False)
    horse_power = db.Column(db.Integer, index=True, nullable=False)
    fuel_type_id = db.Column(db.Integer, db.ForeignKey('fueltypes.id'), nullable=False)
    transmission_id = db.Column(db.Integer, db.ForeignKey('transmissions.id'), nullable=False)
    wheels_drive_id = db.Column(db.Integer, db.ForeignKey('wheelsdrives.id'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), nullable=False)
    owners = db.Column(db.String(2), nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    mileage = db.Column(db.Integer, index=True, nullable=False)
    body_id = db.Column(db.Integer, db.ForeignKey('bodies.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    is_left_hand_drive = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Advert:{self.id}: {self.model_id} {self.year}y, price={self.price}>"
