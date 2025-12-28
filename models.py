from marshmallow_sqlalchemy import fields
from config import db, ma


user_activity = db.Table('user_activity',
    db.Column('user_id', db.Integer, db.ForeignKey('CW2.user.user_id'), primary_key=True),
    db.Column('activity_id', db.Integer, db.ForeignKey('CW2.activity.activity_id'), primary_key=True),
    schema='CW2' 
)

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {"schema": "CW2"} 
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)

class Location(db.Model):
    __tablename__ = 'location'
    __table_args__ = {"schema": "CW2"} 

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(100))
    default_units = db.Column(db.String(20))
    default_language = db.Column(db.String(20))

class Activity(db.Model):
    __tablename__ = 'activity'
    __table_args__ = {"schema": "CW2"} 

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_name = db.Column(db.String(100), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {"schema": "CW2"} 

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    location_id = db.Column(db.Integer, db.ForeignKey('CW2.location.location_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('CW2.role.role_id'), nullable=False)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True) 
    about_me = db.Column(db.Text, nullable=True)
    activity_time_preference = db.Column(db.String(10), nullable=True) 
    height = db.Column(db.Numeric(5, 2), nullable=True)
    weight = db.Column(db.Numeric(5, 2), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(255), nullable=True) 

    role = db.relationship("Role")
    location = db.relationship("Location")
    activities = db.relationship("Activity", secondary=user_activity, backref="users")

# --- SCHEMAS ---

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session

class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        load_instance = True
        sqla_session = db.session

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_fk = True 

    role = fields.Nested(RoleSchema, only=('role_name',))
    location = fields.Nested(LocationSchema, only=('location_name',))
    activities = fields.Nested(ActivitySchema, many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)