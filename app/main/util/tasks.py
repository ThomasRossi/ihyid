from flask import current_app
from app.main.celery import celery
from celery.utils.log import get_task_logger
from app.main.services import db
import requests, json
from app.main.model.organisation import Organisation
from app.main.util.keymanagementutils import KeyManagementClient

logger = get_task_logger(__name__)

def make_gossip_call(*args):
    """ 
    Exectue the desired HTTP method on the url 

    the headers are optional, the response is returned
    although it may be ignored if when calling the task
    the ignore_result is set

    Parameters
    ----------
    args[0]: str
        the method, can be 'get','post','put'

    args[1]: str
        base_url, must have the complete url from http... 

    args[2]: dict
        the JSON to be sent as payload for put and post requests

    args[3]: dict
        the headers to be added 

    Response
    --------

    Raises
    ------

    """
    method = args[0]
    url = args[1]
    payload = {} if (len(args)<=2) else args[2]
    headers = {} if (len(args)<=3) else args[3]

    try:
        if(method=='get'):
            return requests.get(url,headers=headers)
        elif(method=='post'):
            r = requests.post(url,data=payload,headers=headers)
            return r
        elif(method=='put'):
            return requests.put(url,data=payload,headers=headers)
        else:
            return
    except Exception as general_exception:
        return {
            'error': "An Exception occured: " + str(general_exception)}

@celery.task()
def validate_new_org(base_url, public_id):
    """ 
    GET the owner data and compare it against the local copy, if all checks out ACK, else destroy local company

    the method calls the remote system for its owner data, then compares it against the
    local public_id of the company that has been created with the initial POST.
    Empty data is filled, but if an incongruence is found the company is destroyed

    Parameters
    ----------
    base_url: str
        the endpoint to query must have the complete url from http... to /owner
    public_id: str
        the local id of the company 

    Response
    --------

    Raises
    ------

    """
    res = make_gossip_call("get", base_url)
    remote_company = res.json()

    local_org = Organisation.query.filter_by(public_id=public_id).first()

    fields = ['name','vat_number','public_key']
    error_flag = False
    for field in fields:
        if(getattr(local_org, field) == None):
            setattr(local_org, field, remote_company[field])
        if(getattr(local_org, field) != remote_company[field]):
            db.session.delete(local_org)
            db.session.commit()
            error_flag = True
            break
    if not error_flag:
        db.session.add(local_org)
        db.session.commit()
    return
