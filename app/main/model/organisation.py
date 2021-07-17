import datetime
import uuid

from app.main.config import key
from app.main.services import db, flask_bcrypt


class Organisation(db.Model):
    """ Organisation Model for storing company related details """
    __tablename__ = "organisation"

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), unique=True, nullable=False)
    vat_number = db.Column(db.String(100), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_own = db.Column(db.Boolean, nullable=False, default=False)
    base_url = db.Column(db.String(100))
    public_key = db.Column(db.String(100))

    
    def __repr__(self):
        return "<Organisation '{}', vat '{}'>".format(self.name, self.vat_number)

    