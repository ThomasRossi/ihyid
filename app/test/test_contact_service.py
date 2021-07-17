import datetime
import unittest
from sqlalchemy import exc
import os
import random

from app.test.base import BaseTestCase
from app.main.services import db
from app.main.model.contact import Contact
from app.main.service.contact_service import (save_new_contact, update_contact, save_new_contacts, check_contacts, get_all_contacts, get_a_contact)
from app.main.util.eonerror import EonError

class TestContactService(BaseTestCase):

    DEBUG = False
    
    def test_new_contact(self):
        """
        insert a single new contact and check against expects data
        """
        payload = {
            'first_name': 'Houman',
            'last_name' : 'Haddad',
            'mother_first_name' : 'Barbara',
            'father_first_name' : 'Michael',
            'date_of_birth' : datetime.datetime(1976, 5, 7)
        }
        insert_response = save_new_contact(payload)
        self.assertTrue(insert_response[0]['status'] == 'success')
        self.assertTrue(insert_response[1]==201)
        doc = get_a_contact(insert_response[0]['public_id'])
        self.assertTrue(doc.phonetic_id == "H550-H330-B616-M240-19760507")
        #try to insert again and check a doc with the same data cannot be inserted
        try:
            insert_response = save_new_contact(payload)
        except EonError as e:
            self.assertTrue(e.code == 409)
            self.assertTrue(e.message == 'Another contact already exists with the given data.')

    def test_new_contacts(self):
        """
        insert an array fo contacts, wiht one phonetic dublicate, and check the result array
        """
        contact1 = {
            'first_name': 'Houman',
            'last_name' : 'Haddad',
            'mother_first_name' : 'Barbara',
            'father_first_name' : 'Michael',
            'date_of_birth' : datetime.datetime(1976, 5, 7)
        }
        contact2 = {
            'first_name': 'Hooman',
            'last_name' : 'Haddad',
            'mother_first_name' : 'Barbara',
            'father_first_name' : 'Michael',
            'date_of_birth' : datetime.datetime(1976, 5, 7)
        }
        contact3 = {
            'first_name': 'Herman',
            'last_name' : 'Niederkoffler',
            'mother_first_name' : 'Marta',
            'father_first_name' : 'Hans',
            'date_of_birth' : datetime.datetime(1976, 5, 7)
        }
        payload = [contact1, contact2, contact3]
        insert_response = save_new_contacts(payload)
        self.assertTrue(insert_response[1]==200)
        self.assertTrue(insert_response[0][0]["status"]=='success')
        self.assertTrue(insert_response[0][1]["status"]=='fail')
        self.assertTrue(insert_response[0][2]["status"]=='success')

    def test_check_contacts(self):
        """
        Insert a couple fo contacts, then get 3 anon contacts and check if you know them
        """
        contact1 = {
            'first_name': 'Houman',
            'last_name' : 'Haddad',
            'mother_first_name' : 'Barbara',
            'father_first_name' : 'Michael',
            'date_of_birth' : datetime.datetime(1976, 5, 7)
        }
        contact2 = {
            'first_name': 'Herman',
            'last_name' : 'Niederkoffler',
            'mother_first_name' : 'Marta',
            'father_first_name' : 'Hans',
            'date_of_birth' : datetime.datetime(1976, 5, 7)
        }
        payload = [contact1, contact2]
        insert_response = save_new_contacts(payload)

        """
        Prepare anon contacts:
        same anagraphic data for 2, but different secrets, thus differenct uscadi
        """
        arandom1 = os.urandom(32)
        acontact1 = Contact(
            first_name="Houman",
            last_name="Haddad",
            mother_first_name="Barbara",
            father_first_name="Michael",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=arandom1,
            created_on=datetime.datetime.utcnow()
        )
        acontact1.phonetic_id = acontact1.fresh_phonetic_id
        acontact1.uscadi = acontact1.fresh_uscadi
        arandom2 = os.urandom(32)
        acontact2 = Contact(
            first_name="Herman",
            last_name="Niederkoffler",
            mother_first_name="Marta",
            father_first_name="Hans",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=arandom2,
            created_on=datetime.datetime.utcnow()
        )
        acontact2.phonetic_id = acontact2.fresh_phonetic_id
        acontact2.uscadi = acontact2.fresh_uscadi
        arandom3 = os.urandom(32)
        acontact3 = Contact(
            first_name="Victor",
            last_name="Niederhoffler",
            mother_first_name="Gemma",
            father_first_name="Artie",
            date_of_birth=datetime.datetime(1976, 5, 7),
            secret=arandom3,
            created_on=datetime.datetime.utcnow()
        )
        acontact3.phonetic_id = acontact3.fresh_phonetic_id
        acontact3.uscadi = acontact3.fresh_uscadi

        """
        The payload has 2 array: uscadis, secrets with unordered lists of uscadi and secret respectively
        """

        uscadis = [acontact1.uscadi, acontact2.uscadi, acontact3.uscadi]
        random.shuffle(uscadis)
        secrets = [arandom1.hex(), arandom2.hex(), arandom3.hex()]
        random.shuffle(secrets)

        payload = {"secrets":secrets, "uscadis":uscadis}
        check_response = check_contacts(payload)
        self.assertTrue(check_response[1]==200)
        for res in check_response[0]:
            if res["uscadi"] == acontact1.uscadi:
                self.assertTrue(res["known"]=="true")
            if res["uscadi"] == acontact2.uscadi:
                self.assertTrue(res["known"]=="true")
            if res["uscadi"] == acontact3.uscadi:
                self.assertTrue(res["known"]=="false")
    
if __name__ == '__main__':
    unittest.main()
