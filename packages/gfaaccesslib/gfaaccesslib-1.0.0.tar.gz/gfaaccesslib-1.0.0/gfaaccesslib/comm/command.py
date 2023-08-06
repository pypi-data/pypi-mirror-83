import json
import time
import datetime
from gfaaccesslib.comm.header import CommandHeader
from .logger import log
import uuid

__author__ = 'otger'


class CommandStatus:
    REQUEST = 'REQ'
    ACKNOWLEDGE = 'ACK'
    ANSWER = 'ANS'
    DONE = 'DONE'
    ERROR = 'ERR'


class CommandError(Exception):
    pass


class CommandPacket(object):
    args = ['arguments', 'answer', 'created_on', 'received_on', 'elapsed_ms', 'status', 'command']

    def __init__(self, command=None, module=None):

        self._json_dict = {
            'uuid': uuid.uuid4().hex,
            'arguments': {},
            'answer': {},
            'status': CommandStatus.REQUEST,
            'module': module,
            'command': command,
            'created_on': time.mktime(datetime.datetime.utcnow().timetuple()),
            'received_on': None,
            'elapsed_ms': None
        }
        self._cached_payload = None

    def set_arg(self, key, value):
        self._cached_payload = None
        self._json_dict['arguments'][key] = value

    def clear_arguments(self):
        self._cached_payload = None
        self._json_dict['arguments'] = {}

    def get_ans(self, key):
        return self._json_dict['answer'].get(key, None)

    def _get_command(self):
        return self._json_dict['command']
    command = property(_get_command)

    def _get_module(self):
        return self._json_dict['module']
    module = property(_get_module)

    def _get_uuid(self):
        return uuid.UUID(hex=self._json_dict.get('uuid'))
    uuid = property(_get_uuid)

    def _get_json(self):
        return self._json_dict.copy()

    def _set_json(self, json_str):
        if isinstance(json_str, bytes):
            json_str = json_str.decode('UTF-8')
        self._cached_payload = None
        self._json_dict = json.loads(json_str)
    json = property(_get_json, _set_json)

    def _get_answer(self):
        return self._json_dict.get('answer', {})
    answer = property(_get_answer)

    def serialize(self):
        return json.dumps(self._json_dict)

    def set_received_on(self):
        self._cached_payload = None
        self._json_dict['received_on'] = time.mktime(datetime.datetime.utcnow().timetuple())

    def set_elapsed(self, start, end):
        self._cached_payload = None
        self._json_dict['elapsed_ms'] = (end-start).total_seconds()*1000

    def __getattr__(self, item):
        if item not in self.args:
            raise AttributeError('{0} object has no atttribute {1}'.format(self.__class__.__name__, item))

        return self._json_dict.get(item, None)

    @classmethod
    def from_payload(cls, header, payload):
        if not header.is_command():
            msg = "CommandPacket can not be created from another type of header and payload! type: {0}".format(header.type)
            log.error(msg)
            raise Exception(msg)

        c = cls()
        c.json = payload
        return c

    def _get_header(self):
        hdr = CommandHeader()
        hdr.set_values(len(self.payload))
        return hdr
    header = property(_get_header)

    def _get_payload(self):
        self._cached_payload = self._cached_payload or self.serialize()
        return self._cached_payload
    payload = property(_get_payload)




