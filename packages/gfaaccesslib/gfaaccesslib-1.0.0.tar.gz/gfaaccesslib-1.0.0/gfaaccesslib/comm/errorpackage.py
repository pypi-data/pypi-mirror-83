import time
import datetime
import json

from .logger import log
__author__ = 'otger'


class ErrorPackage(object):

    def __init__(self, error_type, message):
        self.error_type = error_type
        self.message = message
        self.received_on = time.mktime(datetime.datetime.utcnow().timetuple())

    @classmethod
    def from_string(cls, json_str):
        '''
        :param json_str:
        :return:
        :raises ValueError: when incorrect json_str
        :raises CommandError: when json does not contain 'command' field
        '''
        if isinstance(json_str, bytes):
            json_str = json_str.decode('UTF-8')
        d = json.loads(json_str)
        log.error("Received error with json: {0} \n\tdict: {1}".format(json_str, d))
        err = d.get('error_type', '')
        msg = d.get('message', '')

        return ErrorPackage(err, msg)
