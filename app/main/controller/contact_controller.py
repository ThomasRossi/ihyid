from flask import request
from flask_restplus import Resource

from app.main.service.contact_service import (get_a_contact, get_all_contacts, save_new_contact, update_contact)
from app.main.util.dto import ContactDto
from app.main.util.decorator import admin_token_required, token_required
from app.main.util.eonerror import EonError

api = ContactDto.api
_contact = ContactDto.contact
_new_contact = ContactDto.new_contact
_contact_to_update = ContactDto.contact_to_update
_new_contact_list = ContactDto.new_contact_list
_anon_contact_list = ContactDto.anon_contact_list
_contact_operation_result = ContactDto.contact_operation_result
_anon_operation_result = ContactDto.anon_operation_result
_anon_check_set = ContactDto.anon_check_set

parser = api.parser()
parser.add_argument('Authorization', location='headers', help="Auth token from login")

@api.route('/')
class ContactList(Resource):
    @api.doc('List of contacts registered on this node - admin only')
    @api.marshal_with(_contact, as_list=True)
    @api.response(400, 'Malformed URL.')
    @api.response(500, 'Internal Server Error.')
    @api.expect(parser)
    @admin_token_required
    def get(self):
        """Returns contacts, known by this node, in a list, admins only"""
        try:
            return get_all_contacts()
        except Exception as e:
                api.abort(500)

    @api.doc('Register a new contact - admin only')
    @api.expect(parser, _new_contact, validate=True)
    @api.response(201, 'Contact successfully created.')
    @api.response(400, 'Contact input data is invalid.')
    @api.response(409, 'Contact already exists.')
    @api.response(500, 'Internal Server Error.')
    @admin_token_required
    def post(self):
        """Register a new contact, admins only"""
        data = request.json
        try:
            return save_new_contact(data=data)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)

@api.route('/import')
class ContactList(Resource):
    @api.doc('Register a list of new contacts - admin only')
    @api.marshal_with(_contact_operation_result, as_list=True)
    @api.expect(parser, _new_contact_list, validate=True)
    @api.response(200, 'Contact list successfully digested.')
    @api.response(500, 'Internal Server Error.')
    @admin_token_required
    def post(self):
        """Register a list of new contacts, admins only"""
        data = request.json
        try:
            return save_new_contacts(data=data)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)

@api.route('/checkanons')
class AnonList(Resource):
    @api.doc('Checks which anons are known - admin only')
    @api.marshal_with(_anon_operation_result, as_list=True)
    @api.expect(parser, _anon_check_set, validate=True)
    @api.response(200, 'Contacts successfully checked.')
    @api.response(500, 'Internal Server Error.')
    @token_required
    def post(self):
        """Check an anon list and find which contacts are known"""
        data = request.json
        try:
            return save_new_contacts(data=data)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)

@api.route('/<id>')
@api.param('id', 'The contact identifier on this node')
class Contact(Resource):
    @api.doc('get a contact - admin only')
    @api.marshal_with(_contact)
    @api.response(404, 'Organisation not found.')
    @api.response(500, 'Internal Server Error.')
    @api.expect(parser)
    @admin_token_required
    def get(self, public_id):
        """Get details for a single contact, admins only""" 
        try:
            return get_an_organisation(public_id)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)

    @api.doc('Update an existing contact - admin only')
    @api.expect(parser, _contact_to_update, validate=True)
    @api.response(200, 'Contact successfully updated.')
    @api.response(404, 'Contact not found.')
    @api.response(409, 'Conflicts with the request, detailed message included')
    @api.response(500, 'Internal Server Error.')
    @admin_token_required
    def put(self, public_id):
        """Update an existing contact, admins only"""
        try:
            data = request.json
            return update_contact(data=data)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)

