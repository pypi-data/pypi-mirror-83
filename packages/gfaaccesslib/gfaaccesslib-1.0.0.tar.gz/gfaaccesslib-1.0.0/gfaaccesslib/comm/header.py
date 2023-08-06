__author__ = 'otger'

import struct
import unittest
from abc import ABCMeta, abstractmethod


'''
All transfer packets between GFA and client have same structure: small 32bytes header + data payload

On this header there is some information required to be able to handle the packet


Format characters:
    B : unsigned char :         1 byte
    H : unsigned short :        2 bytes
    I : unsigned int :          4 bytes
    Q : unsigned long long :    8 bytes
byte order:
    ! : network (= big-endian)
    < : little-endian
    > : big-endian

commandPacket: This type of packets should have a json object of type command serialized as data payload
    type(1byte: uint8) = 1
    reserved(3bytes: uint8[3]) -> For future use due to padding in C/C++ structure
    length(4bytes: uint32) --> length of the data payload. It let have payloads of up to 4GB
    zeroes (24bytes)

    fmt: 'BBBBI' +'B'*24

rawRowPacket: Used to send row data of the CCD. It can contain several amplifiers concatenated, all with same row width
    type(1byte: uint8)=2
    reserved(3bytes: uint8[3]) -> For future use due to padding in C/C++ structure
    metadata_bytes(4bytes: uint32) --> length of the json data payload in bytes
    raw_bytes(4bytes: uint32) --> length of the raw data payload in bytes
    image_id(4bytes: uint32) --> id of the image
    rowNumber(2bytes: uint16) --> Actual index of the row
    rowWidth(2bytes: uint16) --> Width of the row in pixels
    pixelBytes(1byte: uint8) --> Size of each pixel data in bytes
    zeroes(18bytes)

    That is equivalent to c struct like:
    struct rowpacketheader
    {
        uint8  type;
        uint8  reserved[3];
        uint32 metadata_bytes;
        uint32 raw_bytes;
        uint32 image_id;
        uint16 row_number;
        uint16 row_width;
        uint8  pixel_bytes;
        uint8  zeroes[11];

    }

    fmt: 'BBBBIIIHHB' + 'B'*11


'''

STRUCT_BYTE_ORDER = '!'  # On C/C++ server it will make a network to host conversion ntohl
STRUCT_COMMON_PACKET_FMT = 'BBBBI' + 'B'*24
STRUCT_COMMAND_PACKET_FMT = STRUCT_COMMON_PACKET_FMT
STRUCT_RAWROW_PACKET_FMT = 'BBBBIIIHHB' + 'B'*11

STRUCT_ERROR_PACKET_FMT = STRUCT_COMMON_PACKET_FMT

# enum class HEADER_PACKTYPE : uint8_t {
#     COMMAND = 1,
#     RAWROW,
#     ASYNC_IMG_START,
#     ASYNC_IMG_DONE,
#     ASYNC_TELEMETRY,
#     ERROR = 10,
# };


HEADER_PACKTYPE_COMMAND = 1
HEADER_PACKTYPE_RAWROW = 2
HEADER_PACKTYPE_ASYNC_IMG_START = 3
HEADER_PACKTYPE_ASYNC_IMG_DONE = 4
HEADER_PACKTYPE_ASYNC_TELEMETRY_VOLTAGES = 5
HEADER_PACKTYPE_ASYNC_TELEMETRY_SENSORS = 6
HEADER_PACKTYPE_ASYNC_TELEMETRY_ALARMS = 7
HEADER_PACKTYPE_ASYNC_PID = 8

HEADER_PACKTYPE_ERROR = 10
HEADER_PACKTYPE_ASYNC_RESOURCES = 11


def build_header(str_struct):

    values = struct.unpack(STRUCT_BYTE_ORDER+STRUCT_COMMON_PACKET_FMT, str_struct)

    if values[0] == HEADER_PACKTYPE_COMMAND:
        return CommandHeader(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_IMG_START:
        return AsyncImageStartHeader(str_struct)

    if values[0] == HEADER_PACKTYPE_RAWROW:
        return RawRowHeader(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_IMG_DONE:
        return AsyncImageDoneHeader(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_TELEMETRY_VOLTAGES:
        return AsyncTelemetryVoltages(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_TELEMETRY_SENSORS:
        return AsyncTelemetrySensors(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_TELEMETRY_ALARMS:
        return AsyncTelemetryAlarms(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_PID:
        return AsyncPID(str_struct)

    if values[0] == HEADER_PACKTYPE_ERROR:
        return ErrorPacket(str_struct)

    if values[0] == HEADER_PACKTYPE_ASYNC_RESOURCES:
        return ResourcesHeader(str_struct)

    raise Exception('Unkown type of header: {0}'.format(values[0]))


class HeaderBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, str_struct=None):
        self.length = 0
        self.str_struct = str_struct
        self.values = []

        if str_struct is not None:
            self.load_values_from_struct(str_struct)

    def pack(self):
        self.str_struct = struct.pack(self.fmt, *self.values)
        # print "Bytes: {0}".format(struct.unpack("!"+"B"*32, self.str_struct))
        return self.str_struct

    def unpack(self):
        self.values = struct.unpack(self.fmt, self.str_struct)
        return self.values

    def is_command(self):
        return self.type == HEADER_PACKTYPE_COMMAND

    def is_error(self):
        return self.__class__.__name__.find('Error') > -1

    @abstractmethod
    def set_values(self, *args, **kwargs):
        pass

    @abstractmethod
    def load_values_from_struct(self, str):
        pass


class JsonBaseHeader(HeaderBase):

    def __init__(self, str_struct=None):
        self.fmt = STRUCT_BYTE_ORDER + STRUCT_COMMON_PACKET_FMT
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        HeaderBase.__init__(self, str_struct)

    def set_values(self, length):
        self.length = length
        self.values = [self.type, 0, 0, 0, self.length] + list(range(24))

    def load_values_from_struct(self, str_struct):
        self.values = struct.unpack(self.fmt, str_struct)
        if self.values[0] != self.type:
            raise Exception("This string does not define a JsonBaseHeader")
        self.length = self.values[4]


class CommandHeader(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_COMMAND
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class ResourcesHeader(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_RESOURCES
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class AsyncImageStartHeader(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_IMG_START
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class AsyncImageDoneHeader(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_IMG_DONE
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class AsyncTelemetryVoltages(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_TELEMETRY_VOLTAGES
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class AsyncTelemetrySensors(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_TELEMETRY_SENSORS
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class AsyncTelemetryAlarms(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_TELEMETRY_ALARMS
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class AsyncPID(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ASYNC_PID
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class ErrorPacket(JsonBaseHeader):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_ERROR
        self.fmt = STRUCT_BYTE_ORDER + STRUCT_ERROR_PACKET_FMT
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        JsonBaseHeader.__init__(self, str_struct)


class RawRowHeader(HeaderBase):

    def __init__(self, str_struct=None):
        self.type = HEADER_PACKTYPE_RAWROW
        self.fmt = STRUCT_BYTE_ORDER + STRUCT_RAWROW_PACKET_FMT
        self.metadata_bytes = None
        self.raw_bytes = None
        self.image_id = None
        self.row_number = None
        self.row_width = None
        self.pixel_bytes = None
        # HeaderBase init must be called after otherwise if str_struct is provided it will fail
        HeaderBase.__init__(self, str_struct)

    def set_values(self, metadata_bytes, raw_bytes, image_id, row_number, row_width, pixel_bytes):
        self.length = metadata_bytes
        self.metadata_bytes = metadata_bytes
        self.raw_bytes = raw_bytes
        self.image_id = image_id
        self.row_number = row_number
        self.row_width = row_width
        self.pixel_bytes = pixel_bytes
        self.values = [self.type, 0, 0, 0, self.metadata_bytes, self.raw_bytes, self.image_id,
                       self.row_number, self.row_width, self.pixel_bytes] + range(11)

    def load_values_from_struct(self, str_struct):
        self.values = struct.unpack(self.fmt, str_struct)
        if self.values[0] != self.type:
            raise Exception("This string does not define a RawRowHeader")
        self.length = self.values[4]
        self.metadata_bytes = self.values[4]
        self.raw_bytes = self.values[5]
        self.image_id = self.values[6]
        self.row_number = self.values[7]
        self.row_width = self.values[8]
        self.pixel_bytes = self.values[9]

    def __str__(self):
        tmp = ''
        tmp += "\t-metadata_bytes: {0}\n".format(self.metadata_bytes)
        tmp += "\t-raw_bytes: {0}\n".format(self.raw_bytes)
        tmp += "\t-image_id: {0}\n".format(self.image_id)
        tmp += "\t-row_num: {0}\n".format(self.row_number)
        tmp += "\t-row_width: {0}\n".format(self.row_width)
        tmp += "\t-pixel_bytes: {0}\n".format(self.pixel_bytes)

        return tmp


class TestCommandHeaders(unittest.TestCase):

    def setUp(self):
        self.pack = CommandHeader()
        self.pack.set_values(350)
        self.pack_struct = self.pack.pack()
#        print "Length of str_struct: {0}".format(len(self.cmdpack_struct))

    def testPacketRegenerate(self):
        cmdpack = build_header(self.pack_struct)
        self.assertEqual(self.pack.type, cmdpack.type, 'Type are not equal')
        self.assertEqual(self.pack.length, cmdpack.length, 'Lengths are not equal')
        self.assertEqual(self.pack_struct, cmdpack.pack(), 'Struct string generated error')

    def testIsError(self):
        self.assertFalse(self.pack.is_error())


# class TestRawRowHeaders(unittest.TestCase):
#
#     def setUp(self):
#         self.pack = RawRowHeader()
#         self.pack.set_values(length=5000, rowNumber=65, rowwidth=600, amplifier=1)
#         self.pack.pack()
#
#     def testRawRowHeaderRegeneration(self):
#         # print "Lenght: {0}".format(len(self.rawpack.str_struct))
#         rawpack = build_header(self.pack.str_struct)
#         self.assertEqual(self.pack.type, rawpack.type, 'Types are not equal')
#         self.assertEqual(self.pack.length, rawpack.length, 'Lengths are not equal')
#         self.assertEqual(self.pack.rowNumber, rawpack.rowNumber, 'Row Numbers are not equal')
#         self.assertEqual(self.pack.rowWidth, rawpack.rowWidth, 'Row widths are not equal')
#         self.assertEqual(self.pack.amplifier, rawpack.amplifier, 'Amplifiers are not equal')
#
#     def testIsError(self):
#         self.assertFalse(self.pack.is_error())


class TestErrorHeaders(unittest.TestCase):

    def setUp(self):
        self.pack = ErrorPacket()
        self.pack.set_values(350)
        self.pack.pack()

    def testPacketRegenerate(self):
        errpack = build_header(self.pack.str_struct)
        self.assertEqual(self.pack.type, errpack.type, 'Type are not equal')
        self.assertEqual(self.pack.length, errpack.length, 'Lengths are not equal')
        self.assertEqual(self.pack.str_struct, errpack.pack(), 'Struct string generated error')

    def testIsError(self):
        self.assertTrue(self.pack.is_error())

if __name__ == "__main__":
    unittest.main()
