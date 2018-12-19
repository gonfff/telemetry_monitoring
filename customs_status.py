# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from settings import EXCH_API_URL, EXCH_API_AUTH
import json

# import logging
# container = 'TKRU4084405'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def exch_status(container):
    try:
        exch_request = requests.get(EXCH_API_URL + container,
                                    auth=EXCH_API_AUTH)
        exch_answer = json.loads(exch_request.content.decode('utf-8'))
        if exch_answer[0]['tracking'] == []:
            return {'msg': 'Wrong container number'}
        last_status = (exch_answer[0]['tracking'][-1])
        result = last_status['number'] + ' - ' + str(datetime.strptime(
            last_status['create_date'],
            DATETIME_FORMAT)) + ' - ' + last_status['status_desc']
        return {'msg': result, 'status': last_status['status_desc']}
    except Exception as e:
        #logger
        return {'msg': 'Error'}
