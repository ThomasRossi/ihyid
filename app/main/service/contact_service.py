import datetime
import os

from app.main.model.contact import Contact
from app.main.services import db
from app.main.util.eonerror import EonError

from app.main.util.hashutils import HashUtils


def save_new_contact(data):
    try:
        date_of_birth = None
        if(type(data["date_of_birth"]) is str ):
            try:
                date_of_birth =  datetime.datetime.strptime(data["date_of_birth"], '%Y-%m-%d')
            except Exception as e:
                print(e)
                raise EonError('Wrong datetime format, please use UTC and this format %Y-%m-%d', 409)

        new_contact = Contact(
            first_name=data["first_name"],
            last_name=data["last_name"],
            mother_first_name=data.get("mother_first_name",None),
            father_first_name=data.get("father_first_name",None),
            date_of_birth=date_of_birth,
            secret=os.urandom(32),
            created_on=datetime.datetime.utcnow()
        )
        # concetto di lista - import e collegamento contatti lista
        # 
        new_contact.phonetic_id = new_contact.fresh_phonetic_id
        new_contact.uscadi = new_contact.fresh_uscadi
        save_changes(new_contact) 
        return generate_creation_ok_message(new_contact)
    except Exception as e:
        db.session.rollback()
        raise EonError('Another contact already exists with the given data.', 409)

def update_contact(data):
    try:
        contact = Contact.query.filter_by(id=data["id"]).first()
        if not contact:
            raise EonError('Contact does not exist.', 404)
        contact.first_name=data["first_name"]
        contact.last_name=data["last_name"]
        contact.mother_first_name=data.get("mother_first_name",None)
        contact.father_first_name=data.get("father_first_name",None)
        contact.date_of_birth=data["date_of_birth"]
        contact.phoenetic_id = contact.fresh_phonetic_id;
        contact.uscadi = contact.fresh_uscadi
        save_changes(contact) 
        return generate_update_ok_message(contact)
    except:
        db.session.rollback()
        raise EonError('Another contact already exists with the given data.', 409)


def save_new_contacts(data):
    """
    Receive an array of contacts and try to insert them, for each contact prepare a response which says ok/ko 

    For instance we expect a CSV upload, this function is executed by the node admin while loading a new contact list,
    not to be confused with the peer to peer way to exchange lists.
    """
    try:
        response_array = [];
        for contact in data:
            try:
                new_contact = save_new_contact(contact)
                response_array.append(new_contact[0])
            except:
                duplicate_contact = generate_creation_duplicate_message(contact)
                response_array.append(duplicate_contact[0])
        return response_array, 200
    except:
       raise EonError('Internal Server Error.', 500)    

def check_contacts(data):
    """
    Receive a list of uscadi and secrets, check which ones you know

    Load all contacts, get their phoenetic ids, concatenate with each secret and see if there's a match
    """
    try:
        response_array = []
        known_uscadis = []
        used_secrets = []
        used_phonetics = []
        contacts = get_all_contacts();
        local_phonetics = list(map(get_phonetic_id, contacts))
        for secret in data["secrets"]:
            if secret in used_secrets: #make it pseudo-log(n), can't modify the array while looping
                continue
            for phonetic in local_phonetics:
                if(phonetic in used_phonetics): #make it pseudo-log(m), can't modify the array while looping
                    continue
                b = bytearray(phonetic.encode()) #defaults to utf-8, should also this one be hex for uniformity?
                b+=(bytearray(bytes.fromhex(secret))) #default from hex, random bytes can generate non utf-8 compliant sequences
                message = bytes(b)
                hu = HashUtils()
                hex_uscadi = hu.digest(message).hex()
                if hex_uscadi in data["uscadis"]:
                    known_uscadis.append(hex_uscadi)
                    used_secrets.append(secret)
                    used_phonetics.append(phonetic)
                    response_array.append({"uscadi":hex_uscadi, "known":"true"})

        if(len(known_uscadis)<len(data["uscadis"])):
            #add response for unknown uscaids
            for uscadi in data["uscadis"]:
                if not(uscadi in known_uscadis):
                    response_array.append({"uscadi":uscadi, "known":"false"})
        
        return response_array, 200
    except Exception as e:
        print(e)
        raise EonError('Internal Server Error.', 500)    

def get_phonetic_id(contact):
    return contact.phonetic_id

def get_all_contacts():
    return Contact.query.filter_by().all()

def get_a_contact(public_id):
    return Contact.query.filter_by(id=public_id).first()

def get_contacts_of_an_organisation(org_id):
    return Contact.query.filter_by(organisation_id=org_id).all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_creation_ok_message(contact):
    response_object = {
        'status': 'success',
        'message': 'New contact created.',
        'public_id': contact.id
    }
    return response_object, 201

def generate_creation_duplicate_message(contact):
    response_object = {
        'status': 'fail',
        'message': 'Duplicate contact.',
        'public_id': ''
    }
    return response_object, 409

def generate_update_ok_message(contact):
    response_object = {
        'status': 'success',
        'message': 'Contact updated.',
        'public_id': contact.id
    }
    return response_object, 200