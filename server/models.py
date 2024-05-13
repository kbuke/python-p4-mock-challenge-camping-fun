from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, and_
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship; Activity has many campers through Signups
    signups = db.relationship('Signup', backref='activity', lazy=True, cascade='all, delete-orphan')
    
    # Add serialization rules
    serialize_rules = ('-signups.activity',)
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

    # Add relationship; a camper has many activities through Signups
    signups = db.relationship('Signup', backref='camper', lazy=True, cascade=('all, delete-orphan'))
    
    # Add serialization rules
    serialize_rules = ('-signups.camper',) 
    
    # Add validation
    @validates('name')
    def validate_camper(self, key, camper_name):
        if not camper_name:
            raise ValueError('The camper must have a name')
        return camper_name 

    @validates('age')
    def validate_age(self, key, camper_age):
        if 8 <= camper_age <= 18:
            return camper_age 
        raise ValueError('The age must be between 8 and 18')

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # Add relationships; A Signup belongs to a Camper and belongs to an Activity
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    # Add serialization rules
    serialize_rules = ('-camper.signups', '-activity.signups',)
    
    # Add validation
    @validates('time')
    def validate_time(self, key, signup_time):
        if 0 <= signup_time <= 23:
            return signup_time
        raise ValueError("Time must be between 0 and 23")

    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.

