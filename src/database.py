import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Uuser(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __repr__(self):
        return f"{self.username}"
    
    

class Vendor(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4)
    user = db.Column(db.String(100), db.ForeignKey("uuser.id"), nullable=False)
    shop_name = db.Column(db.String(100), nullable=False)
    shop_description = db.Column(db.Text(), nullable=True)
    
    def __repr__(self):
        return f"{self.shop_name}"
    

class Store(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), db.ForeignKey("vendor.id"), nullable=False)
    

class Item(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    status_ = db.Column(db.String(50), nullable=False)