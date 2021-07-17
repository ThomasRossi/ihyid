from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True,
                               description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier')
    })
    new_user = api.model('new_user', {
        'email': fields.String(required=True,
                               description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True,
                                  description='The user password'),
    })


class OrganisationDto:
    api = Namespace('organisation', description='organisation related operations')
    organisation = api.model('organisation', {
        'public_id': fields.String(description='organisation local Identifier'),
        'name': fields.String(required=True,
                              description='organisation name'),
        'vat_number': fields.String(required=True,
                                description='organisation identificaiton number'),
        'base_url': fields.String(required=True,
                                description='base url of the node controlled by the organisation'),
        'public_key': fields.String(required=False,
                                description='public key of the node controlled by the organisation')
    })
    new_organisation = api.model('new_organisation', {
        'name': fields.String(required=True,
                              description='organisation name'),
        'vat_number': fields.String(required=True,
                                description='organisation identificaiton number'),
        'base_url': fields.String(required=True,
                                description='base url of the node controlled by the organisation'),
        'public_key': fields.String(required=False,
                                description='public key of the node controlled by the organisation')
    })
    node_owner_organisation = api.model('node_owner_organisation', {
        'public_id': fields.String(description='organisation local Identifier'),
        'name': fields.String(required=True,
                              description='organisation name'),
        'vat_number': fields.String(required=True,
                                description='organisation identificaiton number'),
        'base_url': fields.String(required=True,
                                description='base url of the node controlled by the organisation'),
        'public_key': fields.String(required=True,
                                description='public key of the node controlled by the organisation')
    })

class ContactDto:
    api = Namespace('contact', description='contact related operations')
    contact = api.model('contact', {
        'id': fields.String(description='contact local identifier'),
        'uscadi': fields.String(required=True,
                              description='global uscadi identifier'),
        'created_on': fields.Date(required=True,
                                description='created on date'),
        'first_name': fields.String(required=True,
                                description='First name of the contact, used in phoenetic id'),
        'last_name': fields.String(required=True,
                                description='Last name of the contact, used in phoenetic id'),
        'mother_first_name': fields.String(required=False,
                                description='Mother\'s first name of the contact, used in phoenetic id if present'),
        'fatherr_first_name': fields.String(required=False,
                                description='Father\'s first name of the contact, used in phoenetic id if present'),
        'date_of_birth': fields.Date(required=True,
                                description='date of birth, used in phoenetic id if present')
    })
    new_contact = api.model('new_contact', {
        'first_name': fields.String(required=True,
                                description='First name of the contact, used in phoenetic id'),
        'last_name': fields.String(required=True,
                                description='Last name of the contact, used in phoenetic id'),
        'mother_first_name': fields.String(required=False,
                                description='Mother\'s first name of the contact, used in phoenetic id if present'),
        'fatherr_first_name': fields.String(required=False,
                                description='Father\'s first name of the contact, used in phoenetic id if present'),
        'date_of_birth': fields.Date(required=True,
                                description='date of birth, used in phoenetic id if present')
    })
    contact_to_update = api.model('contact_to_update', {
        'id': fields.String(required=True,
                                description='contact local identifier'),
        'first_name': fields.String(required=True,
                                description='First name of the contact, used in phoenetic id'),
        'last_name': fields.String(required=True,
                                description='Last name of the contact, used in phoenetic id'),
        'mother_first_name': fields.String(required=False,
                                description='Mother\'s first name of the contact, used in phoenetic id if present'),
        'fatherr_first_name': fields.String(required=False,
                                description='Father\'s first name of the contact, used in phoenetic id if present'),
        'date_of_birth': fields.Date(required=True,
                                description='date of birth, used in phoenetic id if present')
    })
    new_contact_list = api.model('contact_list', {
        'records':fields.List(fields.Nested(new_contact)),
    })
    anon_contact = api.model('anon_contact', {
        'uscadi': fields.String(required=True,
                              description='global uscadi identifier'),
        'secret': fields.String(required=True,
                                description='secret bits used as nonce for uscadi'),
    })
    anon_contact_list = api.model('anon_contact_list', {
        'records':fields.List(fields.Nested(anon_contact)),
    })
    anon_check_set = api.model('anon_check_set', {
        'secrets':fields.List(fields.String(required=True,
                              description='secret, 32bytes hex representation')),
        'uscadis':fields.List(fields.String(required=True,
                              description='global uscadi identifier')),
    })
    contact_operation_result = api.model('contact_operation_result', {
        'status': fields.String(required=True,
                                description='Status of the operation: success/fail'),
        'message': fields.String(required=True,
                                description='Description of the operations'),
        'public_id': fields.String(required=False,
                                description='Local public id of the contact'),
    })
    anon_operation_result = api.model('anon_operation_result', {
        'uscadi': fields.String(required=True,
                                description='global uscadi identifier'),
        'known': fields.String(required=True,
                                description='Is the contact known by this node: true/false')
    })

class MethodResultDto:
    api = Namespace('method_result', description='special methods rpc-like')
    method_result = api.model('method_result', {
        'method': fields.String(required=True, description='The called method'),
        'result': fields.String(required=True, description='The result'),
    })
