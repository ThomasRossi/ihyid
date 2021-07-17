from flask import request
from flask_restplus import Resource

from app.main.service.organisation_service import (get_an_organisation, get_all_organisations, save_new_org, get_node_owner)
from app.main.util.dto import OrganisationDto
from app.main.util.decorator import admin_token_required, token_required
from app.main.util.eonerror import EonError

api = OrganisationDto.api
_organisation = OrganisationDto.organisation
_new_organisation = OrganisationDto.new_organisation
_node_owner_organisation = OrganisationDto.node_owner_organisation

parser = api.parser()
parser.add_argument('Authorization', location='headers', help="Auth token from login")

@api.route('/')
class OrganisationList(Resource):
    @api.doc('List of organisations registere on this node')
    @api.marshal_with(_organisation, as_list=True)
    @api.response(400, 'Malformed URL.')
    @api.response(500, 'Internal Server Error.')
    def get(self):
        """Returns organisations, known by this node, in a list"""
        try:
            return get_all_organisations()
        except Exception as e:
                api.abort(500)

    @api.doc('Register a new organisation')
    @api.expect(parser, _new_organisation, validate=True)
    @api.response(201, 'Org successfully created.')
    @api.response(400, 'Org input data is invalid.')
    @api.response(409, 'Org already exists.')
    @api.response(500, 'Internal Server Error.')
    @api.expect(parser)
    def post(self):
        """Register a new Organisation"""
        data = request.json
        try:
            return save_new_org(data=data)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)


@api.route('/<public_id>')
@api.param('public_id', 'The organisation identifier on this node')
class Organisation(Resource):
    @api.doc('get an organisation')
    @api.marshal_with(_organisation)
    @api.response(404, 'Organisation not found.')
    @api.response(500, 'Internal Server Error.')
    def get(self, public_id):
        """Get details for a single org""" 
        try:
            return get_an_organisation(public_id)
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)


@api.route('/node-owner')
class NodeOwnerCompany(Resource):
    @api.doc('get the details of the org owning this node')
    @api.marshal_with(_node_owner_organisation)
    @api.response(500, 'Internal Server Error.')
    def get(self):
        """Get details of the company running this node""" 
        try:
            return get_node_owner()
        except EonError as e:
            if(e.code and e.message):
                api.abort(e.code, e.message)
            else:
                api.abort(500)

