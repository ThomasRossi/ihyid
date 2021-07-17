import datetime
import unittest
from sqlalchemy import exc
import os

from app.main.services import db
from app.main.model.contact import Contact
from app.test.base import BaseTestCase


class TestContactModel(BaseTestCase):

    DEBUG = False
    
    def test_soundex_tokens(self):
        contact = Contact(
            first_name="Houman",
            last_name="Haddad",
            mother_first_name="Barbara",
            father_first_name="Michael",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=os.urandom(32),
            created_on=datetime.datetime.utcnow()
        )
        contact.phonetic_id = contact.fresh_phonetic_id
        contact.uscadi = contact.fresh_uscadi
        db.session.add(contact)
        db.session.commit()
        self.assertTrue(contact.fresh_phonetic_id == "H550-H330-B616-M240-19760507")  

    def test_uscadi(self):
        contact = Contact(
            first_name="Houman",
            last_name="Haddad",
            mother_first_name="Barbara",
            father_first_name="Michael",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=b'Y\xc5Zr\x99g\x03W\x02qn\xf6\xec&\tOe\xc77`^B g\x99\x13\xcewm5Z:',
            created_on=datetime.datetime.utcnow()
        )
        contact.phonetic_id = contact.fresh_phonetic_id
        contact.uscadi = contact.fresh_uscadi
        db.session.add(contact)
        db.session.commit()
        self.assertTrue(contact.uscadi == '94be4bebeb7946215f0a41f049eac92ae639d3cf5d14f40f213d3aac42a963fc')

    def test_phoenetic_uniqueness(self):
        contact = Contact(
            first_name="Houman",
            last_name="Haddad",
            mother_first_name="Barbara",
            father_first_name="Michael",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=os.urandom(32),
            created_on=datetime.datetime.utcnow()
        )
        contact.phonetic_id = contact.fresh_phonetic_id
        contact.uscadi = contact.fresh_uscadi
        db.session.add(contact)
        db.session.commit()

        contact2 = Contact(
            first_name="Homan",
            last_name="Haddad",
            mother_first_name="Barbara",
            father_first_name="Michael",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=os.urandom(32),
            created_on=datetime.datetime.utcnow()
        )
        contact2.phonetic_id = contact2.fresh_phonetic_id
        contact2.uscadi = contact2.fresh_uscadi
        hadError = False
        try:
            db.session.add(contact2)
            db.session.commit()
        except exc.IntegrityError as err:
            hadError = True
            db.session.rollback()
            self.assertTrue("UNIQUE constraint failed" in str(err))

        self.assertTrue(hadError)    

if __name__ == '__main__':
    unittest.main()
