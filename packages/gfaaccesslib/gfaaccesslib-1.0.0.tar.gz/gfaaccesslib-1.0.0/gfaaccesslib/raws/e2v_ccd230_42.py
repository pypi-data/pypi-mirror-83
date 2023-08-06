#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'otger'
import json
import struct
from .logger import log

class e2vccd23042(object):
    def __init__(self, rawdatamanager):
        self.raws = rawdatamanager

    def process_row(self, header, jsondata, payload):
        # print 'header: ', str(header)
        im = self.raws.get_image(header.image_id)
        if isinstance(jsondata, bytes):
            jsondata = jsondata.decode('UTF-8')
        j = json.loads(jsondata)
        # log.debug('process row json: {0}'.format(j))
        # print("process_row json: {0}".format(j))
    # rowasyncpack.pixel_bytes = 4;
    # rowasyncpack.row_number = GFA_DATAMANAGER_Metadata->MetaInfo.current_line;
    # rowasyncpack.image_id = GFA_DATAMANAGER_Metadata->MetaInfo.LineImageId;
    # rowasyncpack.raw_bytes = raw_bytes;
    # rowasyncpack.row_width = amp_pixels;
    # rowasyncpack.rjsondoc.AddMember("pixel_bytes", rowasyncpack.pixel_bytes, allocator);
    # rowasyncpack.rjsondoc.AddMember("amplifiers_num", GFA_DATAMANAGER_Metadata->MetaInfo.AmplificatorConfig, allocator);
    # rowasyncpack.rjsondoc.AddMember("pages_per_amp", GFA_DATAMANAGER_Metadata->MetaInfo.NumberOfPagesPerThisLine, allocator);
    # rowasyncpack.rjsondoc.AddMember("image_id", GFA_DATAMANAGER_Metadata->MetaInfo.LineImageId, allocator);
    # rowasyncpack.rjsondoc.AddMember("ccd_row_num", GFA_DATAMANAGER_Metadata->MetaInfo.current_line, allocator);
    # rowasyncpack.rjsondoc.AddMember("amplifiers", amplifiers, allocator);
    # rowasyncpack.rjsondoc.AddMember("amplifier_pixels", amp_pixels, allocator);
    # rowasyncpack.rjsondoc.AddMember("amplifier_bytes", amp_bytes, allocator);
        numamps = j['amplifiers_num']
        pixel_bytes = j['pixel_bytes']
        width_pixels = j['amplifier_pixels']
        amplifiers = j['amplifiers']
        if pixel_bytes == 4:
            STRUCT_EL = 'I'
        STRUCT_BYTE_ORDER = '<'
        ## Check if I have to truncate:
        # print('Json received: {0}'.format(j))
        total_bytes = len(payload)
        # print("Received {0}bytes".format(total_bytes))
        if total_bytes < numamps*pixel_bytes*width_pixels:
            # print("There are less bytes than expected")
            width_pixels = total_bytes/(numamps*pixel_bytes)
            # print("New width_pixels: {0}".format(width_pixels))
            #TODO: this must be fixed on HW
            payload = payload[:numamps*width_pixels*pixel_bytes]

        ### end truncate
        str_fmt = STRUCT_EL*numamps*width_pixels
        # print("Length of str_fmt: {0}".format(len(str_fmt)))
        # print("Length of payload: {0}".format(len(payload)))
        # print()
        values = struct.unpack(STRUCT_BYTE_ORDER + str_fmt, payload)
        for ix, el in enumerate(amplifiers):
            im.amplifiers[el].add_row(values[0+ix*width_pixels:(ix+1)*width_pixels], j)

    def process_start_exp(self, header, jsondata):
        if isinstance(jsondata, bytes):
            jsondata = jsondata.decode('UTF-8')
        j = json.loads(jsondata)
        im = self.raws.get_image(j['image_id'])
        im.update_meta(j)
