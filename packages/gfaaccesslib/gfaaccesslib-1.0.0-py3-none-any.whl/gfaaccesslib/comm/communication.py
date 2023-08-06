import datetime
from gfaaccesslib.comm.gfasocket import GFASocket
from gfaaccesslib.comm.header import *
from gfaaccesslib.comm.errorpackage import ErrorPackage
from gfaaccesslib.comm.command import CommandPacket
from .logger import log
import json
import threading
import queue
import socket

__author__ = 'otger'

# ToDo: Make a module inside communication manager called statistics
# ToDo: at statistics: how many commands have been executed and of which type
# ToDo: at statistics: how many bytes sent
# ToDo: at statistics: how many bytes received (separated by header types)


class CommStats(object):
    def __init__(self):
        self._sent_bytes = {'total':0}
        self._rcvd_bytes = {'total':0}

    def sent_bytes(self, num_bytes, xfer_type=''):
        if type:
            if xfer_type not in self._sent_bytes:
                self._sent_bytes[xfer_type] = 0
            self._sent_bytes[xfer_type] += num_bytes
        self._sent_bytes['total'] += num_bytes

    def _get_sent_bytes_stats(self):
        return self._sent_bytes.copy()
    sent_bytes_stats = property(_get_sent_bytes_stats)

    def rcvd_bytes(self, num_bytes, xfer_type=''):
        if type:
            if xfer_type not in self._rcvd_bytes:
                self._rcvd_bytes[xfer_type] = 0
            self._rcvd_bytes[xfer_type] += num_bytes
        self._rcvd_bytes['total'] += num_bytes

    def _get_rcvd_bytes_stats(self):
        return self._rcvd_bytes.copy()
    rcvd_bytes_stats = property(_get_rcvd_bytes_stats)


class CommunicationManager(object):

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self.stats = CommStats()

    def set_parameters(self, ip, port):
        self._ip = ip
        self._port = port

    def get_socket(self, ip=None, port=None):
        return GFASocket(ip or self._ip, port or self._port, build_header)

    def exec_std_command(self, command_packet):
        """
        Sends a command and receives an answer. No asynchronous answers

        :param command_packet:
        :return: CommandPacket
        """
        gfasocket = self.get_socket()
        start = datetime.datetime.utcnow()
        sent = gfasocket.send(command_packet.header, command_packet.payload)
        self.stats.sent_bytes(num_bytes=sent, xfer_type='{0}.{1}'.format(command_packet.module,
                                                                         command_packet.command))
        log.debug('Sent {0} bytes to gfa. Module: {1} - Command: {2}'.format(sent,
                                                                             command_packet.module,
                                                                             command_packet.command))
        rcvd_header, rcvd_dataload, bytes_rcvdd = gfasocket.receive_packet()
        self.stats.rcvd_bytes(num_bytes=bytes_rcvdd, xfer_type='{0}.{1}'.format(command_packet.module,
                                                                                command_packet.command))
        if rcvd_header.is_error():
            err = ErrorPackage.from_string(rcvd_dataload)
            log.error("Error received! type: {0} - message: {1}".format(err.error_type, err.message))
            raise Exception(err.message)
        c = CommandPacket.from_payload(header=rcvd_header, payload=rcvd_dataload)
        c.set_received_on()
        end = datetime.datetime.utcnow()
        c.set_elapsed(start, end)
        return c


class AsyncManager(object):
    def __init__(self, ip, async_port, auto_connect=False):
        self._ip = ip
        self._aport = async_port
        self.stats = CommStats()
        self._exit = False
        self._row_callbacks = []
        self._res_callbacks = []
        self._async_callbacks = {'new_img': [async_img_start_callback_log, ],
                                 'img_done': [async_img_done_callback_log, ],
                                 'telemetry': [async_telemetry_callback_log],
                                 'error': [async_error_callback_log],
                                 'sensors_reading': [async_sensors_reading_callback_log],
                                 'alarms': [async_alarms_callback_log],
                                 'pid': [async_pid_callback_log],
                                 }

        self._socket = None

        if auto_connect:
            self.connect()

    def set_parameters(self, ip, async_port):
        self._ip = ip
        self._aport = async_port

    def connect(self):
        if self._socket:
            log.warning("Already connected")
            return

        self._exit = False
        self._socket = GFASocket(self._ip, self._aport, build_header)
        self._socket.connect()
        self._socket.settimeout(1.0)

        self._asyncs_q = queue.Queue()

        self._receive_asyncs_th = threading.Thread(target=self.receive_asyncs)
        self._receive_asyncs_th.start()

        self._process_async_th = threading.Thread(target=self.process_asyncs)
        self._process_async_th.start()

    def receive_asyncs(self):
        while not self._exit:
            try:
                raw_payload = None
                raw_length = None
                header, data, bytes_recvd = self._socket.receive_packet()
                if isinstance(header, RawRowHeader):
                    raw_payload, raw_length = self._socket.receive(header.raw_bytes)
                    if header.raw_bytes != raw_length:
                        log.error('Asked raw payload of {0} bytes, received {1}'.format(header.raw_bytes, raw_length))
                    # log.debug('Received raw payload: {0}/{1} bytes'.format(raw_length, header.raw_bytes))
            except socket.timeout:
                pass
            except Exception:
                log.exception("Exception waiting for asyncs closing thread")
                return
            else:
                # log.info("Received async with header:\n {0}".format(str(header)))
                # log.info("Received async with json payload of {0}bytes".format(bytes_recvd))
                self._asyncs_q.put((header, data, bytes_recvd, (raw_payload, raw_length)))
                # log.debug('Put async on queue')

    def process_asyncs(self):
        while True:
            try:
                # raw = (raw_payload, raw_length)
                (header, data, bytes_recvd, raw) = self._asyncs_q.get(block=True, timeout=1.0)
            except queue.Empty:
                if self._exit:
                    return
            except Exception:
                log.exception("Unknown exception waiting for asyncs closing thread")
                # return
            else:
                # log.debug('Got async on queue')
                # log.info("Received async with header:\n {0}".format(str(header)))
                # log.info("Received async with json payload of {0}bytes".format(bytes_recvd))
                self.process_async(header, data, bytes_recvd, raw)

    @staticmethod
    def _exec_registered_callbacks(callbacks, header, jsondata, raw=None):
        for cb in callbacks:
            try:
                if raw:
                    cb(header, jsondata, raw)
                else:
                    cb(header, jsondata)
            except Exception:
                log.exception("Exception when executing callback")

    def process_async(self, header, jsondata, bytes_recvd, raw):
        # raw = (raw_payload, raw_length)
        # log.info("Received async of type: {0}".format(type(header)))
        if isinstance(header, RawRowHeader):
            # payload, data_recv = self._socket.receive(header.raw_bytes)
            # log.info("Received rawrow payload: {0}/{1} bytes".format(data_recv, header.raw_bytes))
            # for cb in self._row_callbacks:
            #     cb(header, jsondata, raw[0])
            self._exec_registered_callbacks(self._row_callbacks, header, jsondata, raw[0])

        elif isinstance(header, ResourcesHeader):
            log.debug('Received resources: {0}'.format(jsondata))
            # for cb in self._res_callbacks:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._res_callbacks, header, jsondata)

        elif isinstance(header, AsyncImageStartHeader):
            # for cb in self._async_callbacks['new_img']:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._async_callbacks['new_img'], header, jsondata)

        elif isinstance(header, AsyncImageDoneHeader):
            # for cb in self._async_callbacks['img_done']:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._async_callbacks['img_done'], header, jsondata)

        elif isinstance(header, AsyncTelemetryVoltages):
            # for cb in self._async_callbacks["telemetry"]:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._async_callbacks['telemetry'], header, jsondata)

        elif isinstance(header, AsyncTelemetrySensors):
            # for cb in self._async_callbacks['sensors_reading']:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._async_callbacks['sensors_reading'], header, jsondata)

        elif isinstance(header, AsyncTelemetryAlarms):
            self._exec_registered_callbacks(self._async_callbacks['alarms'], header, jsondata)

        elif isinstance(header, AsyncPID):
            # for cb in self._async_callbacks['pid']:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._async_callbacks['pid'], header, jsondata)

        elif isinstance(header, ErrorPacket):
            # for cb in self._async_callbacks['error']:
            #     cb(header, jsondata)
            self._exec_registered_callbacks(self._async_callbacks['error'], header, jsondata)

    def add_row_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata, raw_data
        """
        self._row_callbacks.append(callback)

    def add_resources_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """
        self._res_callbacks.append(callback)

    def add_new_image_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks['new_img'].append(callback)

    def add_end_image_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks['img_done'].append(callback)

    def add_sensors_reading_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks['sensors_reading'].append(callback)

    def add_alarms_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks["alarms"].append(callback)

    def add_telemetry_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks["telemetry"].append(callback)

    def add_pid_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks['pid'].append(callback)

    def add_error_callback(self, callback):
        """
        Callback calling arguments will be header, jsondata
        """

        self._async_callbacks['error'].append(callback)

    def close(self):
        if not self._socket:
            log.warning("Not connected")
            return

        self._exit = True

        if self._receive_asyncs_th:
            log.info('Joining receive async thread')
            self._receive_asyncs_th.join()
            log.info('Received async thread joined')

        self._socket.close()
        self._socket = None

        if self._process_async_th:
            log.info('Joining process async thread')
            self._process_async_th.join()
            log.info('Process async thread joined')


def resources_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA Resources - vm: {0}KB - rss: {1}KB'.format(j['vm'], j['rss']))


def async_img_start_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - exposure started with image_id: {0}'.format(j['image_id']))


def async_img_done_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - exposure done with image_id: {0}'.format(j['image_id']))


def async_sensors_reading_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - sensors reading received')


def async_alarms_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - alarms received')


def async_telemetry_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - telemetry received')


def async_pid_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - pidreceived')


def async_error_callback_log(header, jsondata):
    if isinstance(jsondata, bytes):
        jsondata = jsondata.decode('UTF-8')
    j = json.loads(jsondata)
    log.info('GFA - error with msg: {0}'.format(j['msg']))
