import datetime
import uuid

from app.main.model.organisation import Organisation
from app.main.services import db
from app.main.util.tasks import validate_new_org
from app.main.util.eonerror import EonError
from app.main.util.keymanagementutils import KeyManagementClient


def save_new_org(data):
    organisation = Organisation.query.filter_by(vat_number=data['vat_number']).first()
    if not organisation:

        new_org = Organisation(
            name=data['name'],
            vat_number=data['vat_number'],
            created_on=datetime.datetime.utcnow(),
            is_own=False,
            base_url=data['base_url'],
            public_key=data.get('public_key', None)
        )
        save_changes(new_org) 

        #GET data from the new base_url and check if it matches
        if(data['base_url']):
            base_url = data['base_url'] if data['base_url'][-1]=='/' else data['base_url']+'/'
            _task = validate_new_org.delay(base_url+'organisation/node-owner', new_org.public_id)
            #call without the queue system:
            #validate_new_org(base_url+'organisation/node-owner', new_org.public_id)

        return generate_creation_ok_message(new_org)
    else:
       raise EonError('Another company already exists with the given data.', 409)


def get_all_organisations():
    return Organisation.query.filter_by(is_own=False).all()

def get_node_owner():
    """ 
    Gets the details of the company owning the node, 

    Passed to the DTO in the controller which filters fields, the key is retrieved via KMC, so it's returned in bytes and thus decoded.

    """
    owner = Organisation.query.filter_by(is_own=True).first()
    kmc = KeyManagementClient()
    owner.public_key = kmc.get_serialized_pub_key().decode('utf-8')
    return owner

def get_an_organisation(public_id):
    return Organisation.query.filter_by(public_id=public_id).first()

def get_locations_of_a_company(company_id):
    return Location.query.filter_by(company_id=company_id).all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_creation_ok_message(org):
    try:
        response_object = {
            'status': 'success',
            'message': 'New organisation created and currently being checked.',
            'public_id': org.public_id
        }
        return response_object, 201
    except Exception:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
