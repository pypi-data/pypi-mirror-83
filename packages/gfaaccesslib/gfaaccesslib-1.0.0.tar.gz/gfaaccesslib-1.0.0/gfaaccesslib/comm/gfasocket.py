from gfaaccesslib.comm.header import HeaderBase
import socket
from .logger import log

__author__ = 'otger'


class GFASocket(object):
    """
           Creates a socket for commands.

           :param header_size: int number of bytes that compose the header
           :param header_deserializer: function that recovers a header from a struct string
    """

    def __init__(self, ip, port, header_deserializer, header_size=32):

        self._header_size = header_size
        self._header_deserializer = header_deserializer
        self._ip = ip
        self._port = port
        self._connected = False
        self._s = None

    def connect(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._s.connect((self._ip, self._port))
            self._connected = True
        except:
            self._connected = False
            raise

    def settimeout(self, timeout):
        if self._s:
            self._s.settimeout(timeout)

    def close(self):
        self._s.close()

    def send(self, header, dataload):
        """
        send header and dataload

        :param header: string or HeaderBase instance
        :param dataload: string
        :return: number of bytes sent
        :raises RuntimeError:
        """

        if isinstance(header, HeaderBase):
            header = header.pack()
        if isinstance(header, str):
            header = header.encode(encoding='UTF-8')
        if isinstance(dataload, str):
            dataload = dataload.encode(encoding='UTF-8')
        if not self._connected:
            self.connect()
        msglen = len(header) + len(dataload)
        totalsent = 0
        msg = header + dataload
        while totalsent < msglen:
            sent = self._s.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken sending")
            totalsent += sent

        return totalsent

    def receive_packet(self):

        # data = ''
        # bytes_recvd = 0
        # Receive header
        # while bytes_recvd < self._header_size:
        #     chunk = self._s.recv(min(self._header_size - bytes_recvd, 4096))
        #     if chunk == '':
        #         raise RuntimeError("socket connection broken receiving header")
        #     # print "Received chunk of header: {0}\n".format(len(chunk))
        #     data += chunk
        #     bytes_recvd += len(chunk)

        data, bytes_recvd = self.receive(self._header_size)
        # log.debug('received header: {0} bytes'.format(bytes_recvd))
        if bytes_recvd != self._header_size:
            log.error('Receiving packet payload received{0}/{1} bytes'.format(bytes_recvd, self._header_size))
        header = self._header_deserializer(data)
        # log.debug('header type:{0} - payload: {1}'.format(header.type, header.length))

        data, bytes_recvd = self.receive(header.length)
        # log.debug('received packet payload {0} bytes'.format(bytes_recvd))
        if bytes_recvd != header.length:
            log.error('Receiving packet payload received{0}/{1} bytes'.format(bytes_recvd, header.length))
        return header, data, bytes_recvd

    def receive(self, bytelength):
        data = bytes()
        bytes_recvd = 0
        # Receive data payload
        while bytes_recvd < bytelength:
            # chunk = self._s.recv(min(bytelength - bytes_recvd, 4096))
            try:
                chunk = self._s.recv(bytelength - bytes_recvd)
            except socket.timeout:
                if bytes_recvd > 0:
                    raise Exception('Timeout on middle of reception')
                raise
            # print chunk
            # print bytes_recvd
            # print datapayloadlength
            if chunk == b'' and bytes_recvd < bytelength:
                raise RuntimeError("socket connection broken receiving payload. Received {0} of {1} bytes".format(len(data), bytelength))
            # print("Received chunk of data: {0}\n".format(len(chunk)))
            data += chunk
            bytes_recvd += len(chunk)

        return data, bytes_recvd
