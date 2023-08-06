#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import re
import datetime
import pytz

__author__ = 'otger'


class GFATimeConfiguration(object):
    """
    Values in ns

    GFA have a step in time of 10ns
    """
    fields = ['vert_tdrt', 'vert_toi', 'vert_tdtr', 'vert_tdrg',
              'vert_tdgr',
              'hor_del',  # Delay time before starting to acquire data with ADC
              'hor_del_skip',
              'hor_acq',  # Acquisition time for each one of the edges (high and low)
              'hor_acq_skip',
              'hor_prerg',
              'hor_prerg_skip',
              'hor_rg',
              'hor_rg_skip',
              'hor_postrg',
              'hor_postrg_skip',
              'hor_overlap',
              'hor_overlap_skip',
              'debug_phase',
              ]

    def __init__(self):
        self.vert_tdrt = None
        self.vert_toi = None
        self.vert_tdtr = None
        self.vert_tdrg = None
        self.vert_tdgr = None
        self.hor_del = None  # Delay time before starting to acquire data with ADC
        self.hor_del_skip = None
        self.hor_acq = None  # Acquisition time for each one of the edges (high and low)
        self.hor_acq_skip = None
        self.hor_prerg = None
        self.hor_prerg_skip = None
        self.hor_rg = None
        self.hor_rg_skip = None
        self.hor_postrg = None
        self.hor_postrg_skip = None
        self.hor_overlap = None
        self.hor_overlap_skip = None
        self.debug_phase = None

    def set_default_values(self):
        self.vert_tdrt = 16000  #
        self.vert_toi = 16000  #
        self.vert_tdtr = 16000  #
        self.vert_tdrg = 20000  #
        self.vert_tdgr = 20000  #
        self.hor_del = 750  # Delay time before starting to acquire data with ADC
        self.hor_del_skip = 20
        self.hor_acq = 1000  # Acquisition time for each one of the edges (high and low)
        self.hor_acq_skip = 750
        self.hor_prerg = 60
        self.hor_prerg_skip = 50
        self.hor_rg = 160
        self.hor_rg_skip = 100
        self.hor_postrg = 60
        self.hor_postrg_skip = 50
        self.hor_overlap = 60  #
        self.hor_overlap_skip = 20
        self.debug_phase = 50000

    def check_values_ranges(self):
        """Check values make sense

        Returns:
            True or False
        """
        return True

    def __str__(self):
        ret = ""
        for k in sorted(self.fields):
            ret += "- {0}: {1}\n".format(k, getattr(self, k, None))

        return ret

    def update(self, other):
        if not isinstance(other, GFATimeConfiguration):
            raise Exception("Can't from an unknown type")

        self.vert_tdrt = other.vert_tdrt
        self.vert_toi = other.vert_toi
        self.vert_tdtr = other.vert_tdtr
        self.vert_tdrg = other.vert_tdrg
        self.vert_tdgr = other.vert_tdgr
        self.hor_del = other.hor_del
        self.hor_del_skip = other.hor_del_skip
        self.hor_acq = other.hor_acq
        self.hor_acq_skip = other.hor_acq_skip
        self.hor_prerg = other.hor_prerg
        self.hor_prerg_skip = other.hor_prerg_skip
        self.hor_rg = other.hor_rg
        self.hor_rg_skip = other.hor_rg_skip
        self.hor_postrg = other.hor_postrg
        self.hor_postrg_skip = other.hor_postrg_skip
        self.hor_overlap = other.hor_overlap
        self.hor_overlap_skip = other.hor_overlap_skip
        self.debug_phase = other.debug_phase

    def _get_pixel_time(self):
        return self.hor_del + self.hor_acq + self.hor_prerg + self.hor_rg + self.hor_postrg \
                + self.hor_del + self.hor_acq + 2*self.hor_overlap
    pixel_time = property(_get_pixel_time)



class GFAExposeMode(object):
    roi = 'roi'
    store_and_read = 'storeandread'
    full_frame = 'fullframe'
    store_only = 'store only'
    read_storage = 'read_store'


class GFARoi(object):
    def __init__(self):
        self.row_init = None
        self.row_end = None
        self.col_init = None
        self.col_end = None

    @classmethod
    def new(cls, row_init, row_end, col_init, col_end):
        roi = cls()
        roi.row_init = row_init
        roi.row_end = row_end
        roi.col_init = col_init
        roi.col_end = col_end
        return roi

    @classmethod
    def new_width(cls, row_init, col_init, width, height):
        roi = cls()
        roi.row_init = row_init
        roi.row_end = row_init + height
        roi.col_init = col_init
        roi.col_end = col_init + width
        return roi

    def __lt__(self, other):
        return self.row_init < other.row_init

    def row_clash(self, other):
        return (self.row_init < other.row_init) and (self.row_end > other.row_init)

    def _get_width(self):
        return self.col_end - self.col_init

    width = property(_get_width)

    def _get_height(self):
        return self.row_end - self.row_init

    height = property(_get_height)

    def __str__(self):
        return "GFARoi: row_init: {0} - height : {1} - col_init: {2} - width: {3}".format(self.row_init, self.height,
                                                                                          self.col_init, self.width)

    def __repr__(self):
        return "[GFARoi: {0}(+{1}), {2}(+{3})]".format(self.row_init, self.height,
                                                       self.col_init, self.width)


class GFARoisSet(object):
    def __init__(self):
        self._rois = []
        self._merged = []
        self.clash = False
        self._cached_merge = False

    def _get_rois(self):
        return self._rois[:]

    rois = property(_get_rois)

    def _get_merged(self):
        if self._cached_merge is False:
            self.merge()
        return self._merged[:]

    merged_rois = property(_get_merged)

    def merge(self):
        self.clash = False
        self.sort()
        self._merge(True)
        self._cached_merge = True

    def _merge(self, first=False):
        clash = False
        if first:
            for _ in range(len(self._merged)):
                self._merged.pop()
            self._merged.extend(self._rois)
        for i in range(len(self._merged) - 1):
            c = self._merged[i]
            n = self._merged[i + 1]
            clash = c.row_clash(n)
            if clash:
                self.clash = True
                self._merged[i].row_init = min(c.row_init, n.row_init)
                self._merged[i].row_end = max(c.row_end, n.row_end)
                self._merged[i].col_init = min(c.col_init, n.col_init)
                self._merged[i].col_end = max(c.col_end, n.col_end)
                self._merged.pop(i + 1)
                break
        if clash:
            self._merge(first=False)

    def set_rois(self, *list_of_rois):
        """
        Sets configured ROIS to values provided.

        :param list_of_rois: Should be a list of coordinates like:
            [[init_row, end_row, init_column, end_column], [init_row2, end_row2,...],...]
            or a list of GFARoi instances
        """
        # check list of rois is valid
        rois_2_set = []
        if isinstance(list_of_rois, GFARoisSet):
            list_of_rois = list_of_rois.rois
        elif not isinstance(list_of_rois, (list, tuple)):
            raise Exception("Invalid argument, it must be a list of GFARoi instances or a list of coordinates")
        for el in list_of_rois:
            if not isinstance(el, GFARoi):
                if not isinstance(el, (list, tuple)):
                    raise Exception("Invalid argument, it must be a list of GFARoi instances or a list of coordinates")
                else:
                    if len(el) != 4:
                        raise Exception(
                            "Invalid argument, it must be a list of GFARoi instances or a list of coordinates")
                    rois_2_set.append(GFARoi.new(el[0], el[1], el[2], el[3]))
            else:
                rois_2_set.append(el)

        self.clear_rois()
        self._rois.extend(rois_2_set)
        self.merge()

    def clear_rois(self):
        """Clears ROIS to an empty list
        """
        self.clash = False
        for i in range(len(self._rois)):
            self._rois.pop()
        self._cached_merge = False

    def add_roi(self, gfaroi):
        """Add a new ROI

        :param gfaroi: instance of GFARoi
        """
        if not isinstance(gfaroi, GFARoi):
            if not isinstance(gfaroi, (list, tuple)) or len(gfaroi) != 4:
                raise Exception("Invalid argument, it must be a GFARoi instance or a list of 4 coordinates")
            else:
                gfaroi = GFARoi.new(gfaroi[0], gfaroi[1], gfaroi[2], gfaroi[3])
        self._rois.append(gfaroi)
        self._cached_merge = False

    def add_roi_geom(self, row_init, col_init, width, height):
        """
        Add a new ROI

        :param row_init: initial row of roi
        :param col_init: initial column of roi
        :param width: roi width in number of columns
        :param height: roi height in number of rows
        """
        gfaroi = GFARoi.new_width(row_init=row_init, col_init=col_init, width=width, height=height)
        self.add_roi(gfaroi=gfaroi)
        self._cached_merge = False

    def sort(self):
        self._rois = sorted(self._rois)


class GFAStandardExposureBuilder(object):
    """
    This is a helper class which can generate specific exposures. It is an upper layer to GFAExposureStack

    In order to build a custom exposure setting each one of the commands that defines itself use GFAExposureStack.
    """

    def __init__(self, gfageomconf, image_id=0):
        """Sets configuration to default values"""
        self.geom_conf = gfageomconf
        self.image_id = image_id
        self.clear_before_integrate = True  # Clear CCD before integration time
        self.clear_after_read = False  # Clear CCD after reading it
        self.integration_time = 1000  # milisecs
        self.mode = GFAExposeMode.store_and_read
        self.rois = GFARoisSet()
        self.stack = GFAExposureStack()
        self._eh_en = gfageomconf.amplifiers_eh_enable
        self._fg_en = gfageomconf.amplifiers_fg_enable

    def set_roi_set(self, gfa_rois_set):
        self.rois.set_rois(gfa_rois_set.rois)

    def check_values(self):
        """Returns True if values make sense (e.g. do not have more ROIs than MAX_ROIS)"""
        return True

    def __str__(self):
        ret = 'CCD Geometry\n'
        ret += '{0}'.format(self.geom_conf)
        ret += 'Exposure conf\n'
        ret += ' - clear before integrate: {0}\n'.format(self.clear_before_integrate)
        ret += ' - clear after read: {0}\n'.format(self.clear_after_read)
        ret += ' - integration time (ms): {0}\n'.format(self.integration_time)

        ret += ' - expose mode configured: {0}\n'.format(self.mode)

        ret += ' - Rois configured: {0}\n'.format(len(self.rois.rois))
        ret += ' - Rois after merge: {0}\n'.format(len(self.rois.merged_rois))

        return ret

    def build(self):
        """Build the exposure configuration and sets each one of the commands that will be written to stack
        Returns a GFAExposureStack instance
        """
        self.stack.clear()

        self.stack.add_new_image_cmd(self.image_id)
        # Clear CCD ?
        if self.clear_before_integrate and self.mode != GFAExposeMode.read_storage:
            # How much rows? storage+image
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, True, True)
            self.stack.add_dump_rows_cmd(self.geom_conf.total_rows)

        # Integration time
        if self.integration_time > 0 and self.mode != GFAExposeMode.read_storage:
            self.stack.add_wait_cmd(self.integration_time)

        # Check which mode are we on:
        if self.mode == GFAExposeMode.full_frame:
            # Reads both storage and image section
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, True, True)
            self.stack.add_read_rows_cmd(self.geom_conf.total_rows)
        elif self.mode == GFAExposeMode.store_only:
            # This mode only stores image section into storage section
            # It does not read any data
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, True, True)
            self.stack.add_dump_rows_cmd(self.geom_conf.storage_rows)
        elif self.mode == GFAExposeMode.store_and_read:
            # This mode shifts image section into storage and then it reads
            # the storage area completely
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, True, True)
            self.stack.add_dump_rows_cmd(self.geom_conf.storage_rows)
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, False, True)
            self.stack.add_read_rows_cmd(self.geom_conf.image_rows)
        elif self.mode == GFAExposeMode.read_storage:
            # This mode read storage contents without shifting charge at image section
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, False, True)
            self.stack.add_read_rows_cmd(self.geom_conf.storage_rows)

        elif self.mode == GFAExposeMode.roi:
            # This mode shifts image section into storage and then it reads
            # each one of the ROI defined

            self.rois.merge()
            self.stack.add_set_modes_cmd(self._eh_en, self._fg_en, True, True)
            self.stack.add_dump_rows_cmd(self.geom_conf.storage_rows)
            last_row = 0
            for el in self.rois.merged_rois:
                if last_row < el.row_init:
                    self.stack.add_dump_rows_cmd(el.row_init - last_row)
                    last_row = el.row_init
                if last_row < el.row_end:
                    # Set columns config
                    self.stack.add_set_roi_conf_cmd(el)
                    # process rows
                    self.stack.add_read_rows_cmd(el.row_end - last_row)
                    last_row = el.row_end

        return self.stack


class GFAStackCodops(object):
    stop = "00000"
    set_mode = "00001"
    wait = "00010"
    proc_rows = "00011"
    set_roi = "00100"
    new_im = "00101"
    shutter = "00110"
    timeregs = "00111"
    looping = "01000"
    end_im = "01001"


class GFAExposureStack(object):
    # TODO: think about how do we pass unsigned 32 bits
    """
    How do we convert back from string to number in server?
    """
    STACK_DEPTH = 1024

    def __init__(self):
        self._commands = []
        self._empty = True

    def _get_commands(self):
        return self._commands[:]

    def _set_commands(self, commands):
        if not isinstance(commands, (list, tuple)):
            raise Exception('commands must be a list of strings')
        for el in commands:
            if not isinstance(el, str):
                raise Exception('commands must be a list of strings')
            if len(el) != 32:
                raise Exception('commands elements length must be 32')
                # if set(el) != set(u"01"):
                #     raise Exception('commands elements must be a string of 0 and 1')
        self._commands = commands

    commands = property(_get_commands, _set_commands)

    def update(self, other):
        if not isinstance(other, GFAExposureStack):
            raise Exception("Can't update from type: {0}".format(type(other)))
        self.commands = other.commands

    def clear(self):
        for _ in range(len(self._commands)):
            self._commands.pop()

    def _add(self, command):
        if len(command) != 32:
            raise Exception("Bad format of command, must be 32 bits long: '{}'".format(command))
        self._commands.append(command)

    def add_wait_cmd(self, millisecs):
        if millisecs > 2 ** 22 - 1:
            raise Exception('millisecs must be at much a 22 bit unsigned integer')
        # bits 26->0 millisecs
        codop = '00000'
        binmillisecs = ('0' * 32 + bin(millisecs)[2:])[-22:]
        self._add(GFAStackCodops.wait + codop + binmillisecs)

    def add_wait_until_tra_goet_trb_cmd(self, address_tra, address_trb):
        if address_tra > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        if address_trb > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        # bits 26->0 millisecs
        bin_op = '0001'
        binaddr_tra = ('0' * 32 + bin(address_tra)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(address_trb)[2:])[-5:]
        empty = ('0' * 32)[-13:]
        composed_cmd = GFAStackCodops.wait + bin_op + binaddr_tra + binaddr_trb + empty
        self._add(composed_cmd)

    def add_wait_until_tra_plus_trb_goet_trc_cmd(self, address_tra, address_trb, address_trc):
        if address_tra > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        if address_trb > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        if address_trc > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        # bits 26->0 millisecs
        bin_op = '0010'
        binaddr_tra = ('0' * 32 + bin(address_tra)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(address_trb)[2:])[-5:]
        binaddr_trc = ('0' * 32 + bin(address_trc)[2:])[-5:]
        empty = ('0' * 32)[-8:]
        composed_cmd = GFAStackCodops.wait + bin_op + binaddr_tra + binaddr_trb + binaddr_trc + empty
        self._add(composed_cmd)

    def add_wait_until_tra_goet_trb_plus_trc_cmd(self, address_tra, address_trb, address_trc):
        if address_tra > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        if address_trb > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        if address_trc > 31:
            raise Exception('Time registers addresses are limited. Valid values range from 0 to 31')
        # bits 26->0 millisecs
        bin_op = '0011'
        binaddr_tra = ('0' * 32 + bin(address_tra)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(address_trb)[2:])[-5:]
        binaddr_trc = ('0' * 32 + bin(address_trc)[2:])[-5:]
        empty = ('0' * 32)[-8:]
        composed_cmd = GFAStackCodops.wait + bin_op + binaddr_tra + binaddr_trb + binaddr_trc + empty
        self._add(composed_cmd)

    def add_none_cmd(self):
        self._add(GFAStackCodops.stop + '0' * 27)

    def _procrows_composer(self, num_rows, skip=False, dump=False, roi=False,
                           roi_overscan=False, debug_reset=False, debug_reference=False,
                           debug_signal=False):
        if num_rows > 2 ** 16:
            raise Exception('num_rows must be a 16 bit unsigned integer')

        nr = '{:016b}'.format(num_rows)
        s = '0'
        if skip:
            s = '1'
        d = '0'
        if dump:
            d = '1'
        r = '0'
        if roi:
            r = '1'
        ro = '0'
        if roi_overscan:
            ro = '1'
        dres = '0'
        if debug_reset:
            dres = '1'
        dref = '0'
        if debug_reference:
            dref = '1'
        ds = '0'
        if debug_signal:
            ds = '1'
        fill = '0' * 4
        return GFAStackCodops.proc_rows + d + s + r + ro + dres + dref + ds + fill + nr

    def add_accumulate_rows_cmd(self, num_rows):
        """
        Add a command to accumulate num_rows rows. Make num_rows vertical transfers
        without dumping charge

        :param num_rows: integer
        :return:
        """
        # skip = '1'
        # dump = '0'
        # fill = '0' * 9
        # num_rows = '{:016b}'.format(num_rows)
        # self._add(GFAStackCodops.proc_rows + dump + skip + fill + num_rows)
        self._add(self._procrows_composer(num_rows=num_rows, skip=True))

    def add_dump_rows_cmd(self, num_rows):
        # if num_rows > 2 ** 16:
        #     raise Exception('num_rows must be a 16 bit unsigned integer')
        # skip = '0'
        # dump = '1'
        # fill = '0' * 9
        # num_rows = '{:016b}'.format(num_rows)
        # self._add(GFAStackCodops.proc_rows + dump + skip + fill + num_rows)
        self._add(self._procrows_composer(num_rows=num_rows, dump=True))

    def add_read_rows_cmd(self, num_rows):
        # if num_rows > 2 ** 16:
        #     raise Exception('num_rows must be a 16 bit unsigned integer')
        # skip = '0'
        # dump = '0'
        # fill = '0' * 9
        # num_rows = '{:016b}'.format(num_rows)
        # self._add(GFAStackCodops.proc_rows + dump + skip + fill + num_rows)
        self._add(self._procrows_composer(num_rows=num_rows))

    def add_read_rows_roi_cmd(self, num_rows):
        # if num_rows > 2 ** 16:
        #     raise Exception('num_rows must be a 16 bit unsigned integer')
        # skip = '0'
        # dump = '0'
        # roi = '1'
        # fill = '0' * 8
        # num_rows = '{:016b}'.format(num_rows)
        # self._add(GFAStackCodops.proc_rows + dump + skip + roi + fill + num_rows)
        self._add(self._procrows_composer(num_rows=num_rows, roi=True))

    def add_read_rows_roi_and_overscan_cmd(self, num_rows):
        # if num_rows > 2 ** 16:
        #     raise Exception('num_rows must be a 16 bit unsigned integer')
        # skip = '0'
        # dump = '0'
        # roi = '1'
        # roi_ovscan = '1'
        # fill = '0' * 7
        # num_rows = '{:016b}'.format(num_rows)
        # self._add(GFAStackCodops.proc_rows + dump + skip + roi + roi_ovscan + fill + num_rows)
        self._add(self._procrows_composer(num_rows=num_rows, roi_overscan=True))

    def add_read_rows_debug_mode_cmd(self, num_rows, debug_reset=False, debug_reference=False, debug_signal=False):
        """
        This command will skip all columns except last one. Last one will use tdebug_phase for reset, acq_reference
        and/or acq_signal depending on values of the arguments
        It is intended for use with raw mode in datmanager and be able to find noise in each one of the phases

        :param num_rows:
        :param debug_reset:
        :param debug_reference:
        :param debug_signal:
        :return:
        """
        self._add(self._procrows_composer(num_rows=num_rows, debug_reset=debug_reset, debug_reference=debug_reference,
                                          debug_signal=debug_signal))

    # def add_set_roi_conf_cmd(self, gfaroi):
    #     skip_columns = ('0' * 32 + bin(gfaroi.col_init)[2:])[-14:]
    #     roi_width = ('0' * 32 + bin(gfaroi.width)[2:])[-13:]
    #     self._add(GFAStackCodops.set_roi + skip_columns + roi_width)
    def add_set_roi_conf_cmd(self, skip_columns, roi_width):
        skip_columns = '{:014b}'.format(skip_columns)
        roi_width = '{:013b}'.format(roi_width)
        self._add(GFAStackCodops.set_roi + skip_columns + roi_width)

    def add_set_modes_cmd(self, eh_en, fg_en, image_en, storage_en):
        eh_en = '1' if eh_en is True else '0'
        fg_en = '1' if fg_en is True else '0'
        i_en = '1' if image_en is True else '0'
        s_en = '1' if storage_en is True else '0'
        modes = ('0' * 32 + eh_en + fg_en + i_en + s_en)[-27:]
        self._add(GFAStackCodops.set_mode + modes)

    def add_new_image_cmd(self, image_id=0):
        """
        add a new exposure commands

        :param image_id: exposure id of the exposure. If left at 0, gfa increases its last value
        """

        if image_id > 2 ** 27:
            raise Exception('image_id must an unsigned integer < {0}'.format(2 ** 27))
        _id = ('0' * 32 + bin(image_id)[2:])[-27:]
        self._add(GFAStackCodops.new_im + _id)

    def add_end_image_cmd(self):
        """
        add an end exposure command
        """
        empty = ('0' * 32)[-27:]
        self._add(GFAStackCodops.end_im + empty)

    def add_open_shutter_command(self):
        self._add(GFAStackCodops.shutter + "0"*26 + "1")

    def add_close_shutter_command(self):
        self._add(GFAStackCodops.shutter + "0"*27)

    def _add_tr_load_value(self, tr_address, value, msb=True):
        if value > 2**16-1:
            raise Exception("value to load must be a 16 bit integer")
        bin_op = '00000'
        binaddr_tra = ('0' * 32 + bin(tr_address)[2:])[-5:]
        # binaddr_trb = ('0' * 32 + bin(address_TRB)[2:])[-5:]
        # binaddr_trc = ('0' * 32 + bin(address_TRC)[2:])[-5:]
        bin_value = ('0' * 32 + bin(value)[2:])[-16:]
        msb_lsb_n = '1' if msb else '0'
        # empty = ('0' * 32)[-8:]
        composed_cmd = GFAStackCodops.timeregs + bin_op + binaddr_tra + msb_lsb_n + bin_value
        if len(composed_cmd) != 32:
            raise Exception("Command must be 32 bits wide")
        self._add(composed_cmd)

    def add_tr_load_value(self, tr_address, value):
        self._add_tr_load_value(tr_address, value >> 16, msb=True)
        self._add_tr_load_value(tr_address, value & 0x0000ffff, msb=False)

    def add_tr_start_timer(self, tr_address, resolution='10ns'):
        valid_resolutions = ['10ns', '1us', '1ms']
        if resolution not in valid_resolutions:
            raise Exception('Valid resolutions are: {}'.format(', '.join(valid_resolutions)))
        if resolution == '10ns':
            res = '00'
        elif resolution == '1us':
            res = '01'
        else:
            res = '10'
        binaddr_tra = ('0' * 32 + bin(tr_address)[2:])[-5:]
        empty = ('0' * 32)[-15:]
        compose_cmd = GFAStackCodops.timeregs + "00001" + binaddr_tra + res + empty
        self._add(compose_cmd)

    def add_tr_stop_timer(self, tr_address):
        binaddr_tra = ('0' * 32 + bin(tr_address)[2:])[-5:]
        empty = ('0' * 32)[-15:]
        res = '11'
        compose_cmd = GFAStackCodops.timeregs + "00001" + binaddr_tra + res + empty
        self._add(compose_cmd)

    def add_tr_clear(self, tr_address, all=False):
        """If all is False, only register set by address is cleared, otherwise all registers are cleared
        and address value is not taken into account. When TR is cleared, its timer functionality is stopped
        and its value set to 0"""

        if all:
            codop = "00010"
            empty = ('0' * 32)[-22:]
            compose_cmd = GFAStackCodops.timeregs + codop + empty
            self._add(compose_cmd)
        else:
            codop = "00011"
            binaddr_tra = ('0' * 32 + bin(tr_address)[2:])[-5:]
            empty = ('0' * 32)[-17:]
            compose_cmd = GFAStackCodops.timeregs + codop + binaddr_tra + empty
            self._add(compose_cmd)

    def add_tr_increase(self, tr_address):
        """Increase value of TR by 1"""
        codop = "00100"
        binaddr_tra = ('0' * 32 + bin(tr_address)[2:])[-5:]
        op = '0'
        empty = ('0' * 32)[-16:]
        compose_cmd = GFAStackCodops.timeregs + codop + binaddr_tra + op + empty
        self._add(compose_cmd)

    def add_tr_decrease(self, tr_address):
        """Decrease value of TR by 1"""
        codop = "00100"
        binaddr_tra = ('0' * 32 + bin(tr_address)[2:])[-5:]
        op = '1'
        empty = ('0' * 32)[-16:]
        compose_cmd = GFAStackCodops.timeregs + codop + binaddr_tra + op + empty
        self._add(compose_cmd)

    def add_tr_copy_trb_2_tra(self, tra_address, trb_address):
        """Copy value of TRB to TRA"""
        codop = "00101"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        empty = ('0' * 32)[-12:]
        compose_cmd = GFAStackCodops.timeregs + codop + binaddr_tra + binaddr_trb + empty
        self._add(compose_cmd)

    def add_tr_load_trb_plus_trc_2_tra(self, tra_address, trb_address, trc_address):
        """Copy value of TRB + TRC to TRA. TRA = TRB + TRC"""
        codop = "00110"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        binaddr_trc = ('0' * 32 + bin(trc_address)[2:])[-5:]
        op = '0'
        empty = ('0' * 32)[-7:]
        compose_cmd = GFAStackCodops.timeregs + codop + binaddr_tra + binaddr_trb + binaddr_trc + op + empty
        self._add(compose_cmd)

    def add_tr_load_trb_minus_trc_2_tra(self, tra_address, trb_address, trc_address):
        """Copy value of TRB - TRC to TRA. TRA = TRB - TRC"""
        codop = "00110"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        binaddr_trc = ('0' * 32 + bin(trc_address)[2:])[-5:]
        op = '1'
        empty = ('0' * 32)[-7:]
        compose_cmd = GFAStackCodops.timeregs + codop + binaddr_tra + binaddr_trb + binaddr_trc + op + empty
        self._add(compose_cmd)

    def add_loop_start(self):
        codop = "00000"
        empty = ('0' * 32)[-22:]

        compose_cmd = GFAStackCodops.looping + codop + empty
        self._add(compose_cmd)

    def add_loop_end_loop_if_tra_neq_0(self, tra_address):
        codop = "00001"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        op = '0'
        empty = ('0' * 32)[-16:]
        compose_cmd = GFAStackCodops.looping + codop + binaddr_tra + op + empty
        self._add(compose_cmd)

    def add_loop_end_loop_if_tra_eq_0(self, tra_address):
        codop = "00001"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        op = '1'
        empty = ('0' * 32)[-16:]
        compose_cmd = GFAStackCodops.looping + codop + binaddr_tra + op + empty
        self._add(compose_cmd)

    def add_loop_end_loop_if_tra_neq_trb(self, tra_address, trb_address):
        codop = "00010"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        op = '0'
        empty = ('0' * 32)[-11:]
        compose_cmd = GFAStackCodops.looping + codop + binaddr_tra + binaddr_trb + op + empty
        self._add(compose_cmd)

    def add_loop_end_loop_if_tra_eq_trb(self, tra_address, trb_address):
        codop = "00010"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        op = '1'
        empty = ('0' * 32)[-11:]
        compose_cmd = GFAStackCodops.looping + codop + binaddr_tra + binaddr_trb + op + empty
        self._add(compose_cmd)

    def add_loop_end_loop_if_tra_lt_trb(self, tra_address, trb_address):
        """
        End loop command. Loop if tra < trb, else stop loop

        :param tra_address: Time Register address of tra
        :param trb_address: Time Register address of trb
        :return: None
        """
        codop = "00011"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        op = '0'
        empty = ('0' * 32)[-11:]
        compose_cmd = GFAStackCodops.looping + codop + binaddr_tra + binaddr_trb + op + empty
        self._add(compose_cmd)

    def add_loop_end_loop_if_tra_loet_trb(self, tra_address, trb_address):
        """
        End loop command. Loop if tra <= trb, else stop loop

        :param tra_address: Time Register address of tra
        :param trb_address: Time Register address of trb
        :return: None
        """
        codop = "00011"
        binaddr_tra = ('0' * 32 + bin(tra_address)[2:])[-5:]
        binaddr_trb = ('0' * 32 + bin(trb_address)[2:])[-5:]
        op = '1'
        empty = ('0' * 32)[-11:]
        compose_cmd = GFAStackCodops.looping + codop + binaddr_tra + binaddr_trb + op + empty
        self._add(compose_cmd)

    def translate_2_human(self):
        """
        return list of string explaining contents of stack

        :return:
        """
        return [stack_code_2_human(el) for el in self._commands]

    def set_commands(self, commands):
        self._commands = commands

    def __str__(self):
        if len(self._commands) == 0:
            return "Exposure stack is empty"
        ret = "Commands contents\n"
        for ix, el in enumerate(self._commands):
            ret += '\t{0:03} - {1} - {2}\n'.format(ix, el, stack_code_2_human(el))
        return ret


def stack_code_2_human(code):
    if code.startswith(GFAStackCodops.wait):
        wait_op = code[-27:-23]
        if wait_op == "0000":
            ms = int(code[-23:], 2)
            if ms < 2000:
                ret = "Wait for {0} milliseconds".format(ms)
            elif ms < 120000:
                ret = "Wait for {0} seconds".format(ms / 1000.0)
            elif ms < 120000 * 60:
                ret = "Wait for {0} minutes".format(ms / 60000.0)
            else:
                ret = "Wait for {0} hours".format(ms / 3600000.0)
        elif wait_op == "0001":
            tra = int(code[-23:-18], 2)
            trb = int(code[-18:-13], 2)
            ret = "Wait until TimeRegister @{} >= TimeRegister @{}".format(tra, trb)
        elif wait_op == "0010":
            tra = int(code[-23:-18], 2)
            trb = int(code[-18:-13], 2)
            trc = int(code[-13:-8], 2)
            ret = "Wait until TimeRegister @{} + TimeRegister @{} >= TimeRegister @{}".format(tra, trb, trc)
        elif wait_op == "0011":
            tra = int(code[-23:-18], 2)
            trb = int(code[-18:-13], 2)
            trc = int(code[-13:-8], 2)
            ret = "Wait until TimeRegister @{} >= TimeRegister @{} + TimeRegister @{}".format(tra, trb, trc)
    elif code.startswith(GFAStackCodops.stop):
        ret = "Stop command"
    elif code.startswith(GFAStackCodops.proc_rows):
        if code.startswith("00011100"):
            ret = "Dump {0} rows".format(int(code[-16:], 2))
        elif code.startswith("00011010"):
            ret = "Accumulate {0} rows".format(int(code[-16:], 2))
        elif code.startswith("00011000"):
            ret = "Read {0} rows".format(int(code[-16:], 2))
        elif code.startswith("00011001"):
            ret = "Read {0} rows as ROI".format(int(code[-16:], 2))
        else:
            ret = "Erroneous read, skip or dump command. {0} rows.".format(int(code[-16:], 2))
    elif code.startswith(GFAStackCodops.set_roi):
        ret = "Set roi init col to {0} and roi width to {1} cols". \
            format(int(code[-27:-13], 2), int(code[-13:], 2))
    elif code.startswith(GFAStackCodops.set_mode):
        eh_en = (code[-4] == '1')
        fg_en = (code[-3] == '1')
        i_en = (code[-2] == '1')
        s_en = (code[-1] == '1')
        ret = "Set modes, EH: {0} - FG: {1} - Shift Image: {2} - Shift Storage: {3}". \
            format(eh_en, fg_en, i_en, s_en)
    elif code.startswith(GFAStackCodops.new_im):
        _id = int(code[-27:], 2)
        ret = "New image with id {0}".format(_id)
    elif code.startswith(GFAStackCodops.end_im):
        ret = "Mark end of image"
    elif code.startswith(GFAStackCodops.timeregs):
        codop = code[-27:-22]
        tra = int(code[-22:-17], 2)
        if codop == "00000":
            value = int(code[-16:], 2)
            msb = 'MSB' if code[-16] == '1' else 'LSB'
            ret = "Load {} to 16 {} of TimeReg @{}".format(value, msb, tra)
        elif codop == "00001":
            if code[-17:-15] == "11":
                ret = "Stop timer at TimeReg @{}".format(tra)
            elif code[-17:-15] == "00":
                ret = "Start timer at TimeReg @{} with resolution 10 ns".format(tra)
            elif code[-17:-15] == "01":
                ret = "Start timer at TimeReg @{} with resolution 1 us".format(tra)
            elif code[-17:-15] == "10":
                ret = "Start timer at TimeReg @{} with resolution 1 ms".format(tra)
        elif codop == "00010":
            ret = "Clear all timeregs"
        elif codop == "00011":
            ret = "Clear Timereg @{}".format(tra)
        elif codop == "00100":
            if code[-16] == '1':
                ret = "Decrease Timereg @{} value by 1".format(tra)
            else:
                ret = "Increase Timereg @{} value by 1".format(tra)
        elif codop == "00101":
            trb = int(code[-17:-12], 2)
            ret = "Copy value of Timereg @{} to Timereg @{}".format(trb, tra)
        elif codop == "00110":
            trb = int(code[-17:-12], 2)
            trc = int(code[-12:-7], 2)
            if code[-6] == '1':
                ret = "TimeReg @{} = TimeReg @{} - TimeReg @{}".format(tra, trb, trc)
            else:
                ret = "TimeReg @{} = TimeReg @{} + TimeReg @{}".format(tra, trb, trc)
    elif code.startswith(GFAStackCodops.looping):
        codop = code[-27:-22]
        if codop == "00000":
            ret = "Start loop"
        elif codop == "00001":
            tra = int(code[-22:-17], 2)
            op = code[-16]
            if op == '0':
                ret = "Loop if TR {} /= 0".format(tra)
            else:
                ret = "Loop if TR {} = 0".format(tra)
        elif codop == "00010":
            tra = int(code[-22:-17], 2)
            trb = int(code[-17:-12], 2)
            op = code[-11]
            if op == '0':
                ret = "Loop if TR {} /= TR {}".format(tra, trb)
            else:
                ret = "Loop if TR {} =  TR {}".format(tra, trb)
        elif codop == "00011":
            tra = int(code[-22:-17], 2)
            trb = int(code[-17:-12], 2)
            op = code[-11]
            if op == '0':
                ret = "Loop if TR {} < TR {}".format(tra, trb)
            else:
                ret = "Loop if TR {} <=  TR {}".format(tra, trb)

    else:
        ret = "Unknown command"

    return ret


class GFAExposureLock(object):

    def __init__(self):
        self._lock = threading.Lock()

    def acquire(self, msg=None):
        self._lock.acquire()
        if msg:
            print('acquired - {0}'.format(msg))

    def _get_is_locked(self):
        return self._lock.locked()
    is_locked = property(_get_is_locked)

    def release(self, msg=None):
        self._lock.release()
        if msg:
            print('released - {0}'.format(msg))

    def async_callback_release(self, *args, **kwargs):
        try:
            # print('async release')
            self.release(msg='async')
        except threading.ThreadError as ex:
            print('Release error: {0}'.format(ex))


class GFAClockManagerInfo(object):
    def __init__(self):
        self._info = {
            u'next_command': 0,
            u'read_pointer': 0,
            u'read_pointer_data': 0,
            u'status_bits': 0,
            u'processed_horizontal': 0,
            u'current_row': 0,
            u'exec_pointer': 0,
            u'write_pointer': 0,
            u'exposure_id': 0,
            u'processed_vertical': 0,
            u'current_command': 0,
            u'current_col': 0
        }
        self._status = GFAClockManagerStatus()

    def update_info(self, info):
        self._info.update(info)
        self._status.status = self._info['status_bits']

    def _get_proc_hor(self):
        return self._info['processed_horizontal']

    processed_horizontal = property(_get_proc_hor)

    def _get_proc_vert(self):
        return self._info['processed_vertical']

    processed_vertical = property(_get_proc_vert)

    def _get_exp_id(self):
        return self._info['exposure_id']

    exposure_id = property(_get_exp_id)

    def _get_next_command(self):
        return self._info['next_command']

    next_command = property(_get_next_command)

    def _get_next_command_human(self):
        return stack_code_2_human(self.next_command)

    next_command_human = property(_get_next_command_human)

    def _get_read_pointer(self):
        return self._info[u'read_pointer']

    read_pointer = property(_get_read_pointer)

    def _get_read_pointer_data(self):
        return self._info[u'read_pointer_data']

    read_pointer_data = property(_get_read_pointer_data)

    def _get_status(self):
        return self._status

    def _set_status(self, status):
        self._status = status
    status = property(_get_status, _set_status)

    def __str__(self):
        tmp = ""
        for k,v in self._info.items():
            tmp += " - {0}: {1}\n".format(k, v)
        return tmp


class GFAClockManagerStatus(object):
    def __init__(self):
        # self._full = False
        # self._empty = False
        # self._executing_last_command = False
        # self._executing_stack = False
        # self._force_execute = False
        # self._cancel_exp = False
        # self._clear_stack = False
        # self._reset_exec_pointer = False
        # self._storage_shift_en = False
        # self._image_shift_en = False
        # self._amplifier_fg_en = False
        # self._amplifier_eh_en = False
        # self._cm_configured = False
        self._bin_status = 0

    def _get_full(self):
        return bool(self._bin_status & (1 << 0))

    stack_full = property(_get_full)

    def _get_empty(self):
        return bool(self._bin_status & (1 << 1))

    stack_empty = property(_get_empty)

    def _get_exec_last_cmd(self):
        return bool(self._bin_status & (1 << 2))

    executing_last_cmd = property(_get_exec_last_cmd)

    def _get_running(self):
        return bool(self._bin_status & (1 << 3))

    running = property(_get_running)

    def _get_force_execute(self):
        return bool(self._bin_status & (1 << 4))

    def _set_force_execute(self, execute):
        if execute:
            self._bin_status |= (1 << 4)

    force_execute = property(_get_force_execute, _set_force_execute)

    def _get_clear_stack(self):
        return bool(self._bin_status & (1 << 6))

    def _set_clear_stack(self, start):
        if start:
            self._bin_status |= (1 << 6)

    clear_stack = property(_get_clear_stack, _set_clear_stack)

    def _get_reset_exec_pointer(self):
        return bool(self._bin_status & (1 << 7))

    def _set_reset_exec_pointer(self, start):
        if start:
            self._bin_status |= (1 << 7)

    reset_exec_pointer = property(_get_reset_exec_pointer, _set_reset_exec_pointer)

    def _get_storage_shift_en(self):
        return bool(self._bin_status & (1 << 8))

    def _set_storage_shift_en(self, shift):
        if shift:
            self._bin_status |= (1 << 8)

    shift_storage = property(_get_storage_shift_en, _set_storage_shift_en)

    def _get_image_shift_en(self):
        return bool(self._bin_status & (1 << 9))

    def _set_image_shift_en(self, shift):
        if shift:
            self._bin_status |= (1 << 9)

    shift_image = property(_get_image_shift_en, _set_image_shift_en)

    def _get_amplifier_fg_en(self):
        return bool(self._bin_status & (1 << 10))

    def _set_amplifier_fg_en(self, shift):
        if shift:
            self._bin_status |= (1 << 10)

    amplifier_fg = property(_get_amplifier_fg_en, _set_amplifier_fg_en)

    def _get_amplifier_eh_en(self):
        return bool(self._bin_status & (1 << 11))

    def _set_amplifier_eh_en(self, shift):
        if shift:
            self._bin_status |= (1 << 11)

    amplifier_eh = property(_get_amplifier_eh_en, _set_amplifier_eh_en)

    # ToDo: gfa sends information about which registers are set and which aren't. Create access to this info
    def _get_configured(self):
        return bool(self._bin_status & (1 << 12))

    is_configured = property(_get_configured)

    def _get_status(self):
        return self._bin_status

    def _set_status(self, status):
        self._bin_status = status

    status = property(_get_status, _set_status)

    def _get_str_status(self):
        return ('0' * 32 + bin(self._bin_status)[2:])[-32:]

    def _set_str_status(self, str_status):
        if not isinstance(str_status, str):
            raise Exception("str_status must be a string of 01")
        str_status = '0' * 32 + str_status
        self._bin_status = int(str_status[-32:], 2)

    str_status = property(_get_str_status, _set_str_status)

    def __str__(self):
        ret = ""
        ret += "GFA Clock Manager Status\n"
        ret += " - status: {0}\n".format(self.status)
        ret += " - bin status: {0}\n".format(self.str_status)
        ret += " - stack full: {0}\n".format(self.stack_full)
        ret += " - stack empty: {0}\n".format(self.stack_empty)
        ret += " - executing_last_command: {0}\n".format(self.executing_last_cmd)
        ret += " - running: {0}\n".format(self.running)
        ret += " - force execute: {0}\n".format(self.force_execute)
        ret += " - clear stack: {0}\n".format(self.clear_stack)
        ret += " - reset execution pointer: {0}\n".format(self.reset_exec_pointer)
        ret += " - shift storage lines: {0}\n".format(self.shift_storage)
        ret += " - shift image lines: {0}\n".format(self.shift_image)
        ret += " - amplifiers fg enabled: {0}\n".format(self.amplifier_fg)
        ret += " - amplifiers eh enabled: {0}\n".format(self.amplifier_eh)
        ret += " - all settings configured: {0}\n".format(self.is_configured)

        return ret


class GFAExposeControllerStatus(object):
    def __init__(self):
        self._status = 0

    def _get_status_word(self):
        return self._status

    def _set_status_word(self, word):
        self._status = word
    status_word = property(_get_status_word, _set_status_word)

    def _get_is_idle(self):
        return bool(self._status & (1 << 6))

    def _get_is_configured(self):
        return bool(self._status & (1 << 7))

    def _get_is_power_up(self):
        return bool(self._status & (1 << 8))

    def _get_is_power_down(self):
        return bool(self._status & (1 << 9))

    def _get_is_ready(self):
        return bool(self._status & (1 << 10))

    def _get_is_exposing(self):
        return bool(self._status & (1 << 11))

    def _get_is_telemetry(self):
        return bool(self._status & (1 << 12))

    def _get_is_error(self):
        return bool(self._status & (1 << 13))

    def _get_is_powered(self):
        return bool(self._status & (1 << 14))

    is_powered = property(_get_is_powered)
    error_state = property(_get_is_error)
    telemetry_state = property(_get_is_telemetry)
    exposing_state = property(_get_is_exposing)
    ready_state = property(_get_is_ready)
    power_down_state = property(_get_is_power_down)
    power_up_state = property(_get_is_power_up)
    configured_state = property(_get_is_configured)
    idle_state = property(_get_is_idle)

    def _get_current_state(self):
        if self.error_state:
            return 'error_state'
        if self.telemetry_state:
            return 'telemetry'
        if self.exposing_state:
            return 'exposing'
        if self.ready_state:
            return 'ready'
        if self.power_down_state:
            return 'power down'
        if self.power_up_state:
            return 'power up'
        if self.configured_state:
            return 'configured'
        if self.idle_state:
            return 'idle'
        return 'Unknown state. Status word: {0}'.format(self._status)
    current_state = property(_get_current_state)

    def __str__(self):
        tmp = "Current state: {0}\n".format(self._get_current_state())
        tmp += "Voltage powered: {0}\n".format(self.is_powered)
        return tmp


class GFAVoltageEnables(object):
    enables = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4', 'D1', 'D2', 'D3', 'D4',
               'E1', 'E2', 'E3', 'F1', 'F2', 'F3', 'G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'DD', 'OG', 'VSS', 'RD',
               'TGA', 'TGD', 'SWE', 'SWF', 'SWG', 'SWH', 'ODE', 'ODF', 'ODG', 'ODH', 'DGA', 'DGD',
               'RGE', 'RGF', 'RGG', 'RGH']

    def __init__(self):
        self.enables_0 = 0
        self.enables_1 = 0

    def print_status(self):
        print(self.__str__())

    def __str__(self):
        ix = 0
        tmp = ''
        while ix < len(self.enables):
            tmp += " - {0:3}: {1:5}   {2:3}: {3:5}   {4:3}: {5:5}   {6:3}: {7:5}\n".format(self.enables[ix],
                                                                                 str(getattr(self, self.enables[ix])),
                                                                                 self.enables[ix + 1],
                                                                                 str(getattr(self, self.enables[ix + 1])),
                                                                                 self.enables[ix + 2],
                                                                                 str(getattr(self, self.enables[ix + 2])),
                                                                                 self.enables[ix + 3],
                                                                                 str(getattr(self, self.enables[ix + 3])),
                                                                                 )
            ix += 4
        return tmp

    def __getattr__(self, item):

        if item not in self.enables:
            return None
        ix = self.enables.index(item)
        mod = ix % 32
        if ix < 32:
            return bool(self.enables_0 & (1 << mod))
        return bool(self.enables_1 & (1 << mod))


class GFACCDGeom(object):
    """Defines geometry of the CCD

        - active_cols: number of columns to be read by each amplifier if all amplifiers are enabled
        - cols_2_be_read: of the enabled amplifiers, how many columns will be read by each amplifier.
            This value changes when enabling/disabling amplifiers. This is the real setting sent to the GFA.
            It contains prescan and overscan.
    """

    def __init__(self):
        self._amplifiers_en = {'EH': True, 'FG': True}
        self._image_shift_en = True
        self._store_shift_en = True
        self._store_rows = 0
        self._image_rows = 0
        self._amplifier_prescan = 0
        self._amplifier_overscan = 0
        self._ccd_active_cols = 0  # columns to be read by each amplifier in normal mode

    def set_default_values(self):
        self._amplifiers_en = {'EH': True, 'FG': True}
        self._image_shift_en = True
        self._store_shift_en = True
        self._store_rows = 512
        self._image_rows = 512
        self._amplifier_prescan = 50
        self._amplifier_overscan = 50
        self._ccd_active_cols = 2048  # columns of active pixels of the whole ccd

    def update(self, other):
        if not isinstance(other, GFACCDGeom):
            raise Exception("Can't from this type: {0}".format(type(other)))

        self._amplifiers_en = other._amplifiers_en
        self._image_shift_en = other._image_shift_en
        self._store_shift_en = other._store_shift_en
        self._store_rows = other._store_rows
        self._image_rows = other._image_rows
        self._amplifier_prescan = other._amplifier_prescan
        self._amplifier_overscan = other._amplifier_overscan
        self._ccd_active_cols = other._ccd_active_cols

    @property
    def amplifier_active_cols(self):
        if self.amplifiers_eh_enable and self.amplifiers_fg_enable:
            return int(self._ccd_active_cols / 2)
        if self.amplifiers_eh_enable or self.amplifiers_fg_enable:
            return self._ccd_active_cols
        return 0

    @amplifier_active_cols.setter
    def amplifier_active_cols(self, value):
        if self.amplifiers_eh_enable and self.amplifiers_fg_enable:
            self.ccd_active_cols = value * 2
        elif self.amplifiers_eh_enable or self.amplifiers_fg_enable:
            self.ccd_active_cols = value
        else:
            self.ccd_active_cols = 0


    @property
    def ccd_active_cols(self):
        return self._ccd_active_cols

    @ccd_active_cols.setter
    def ccd_active_cols(self, value):
        # Active pixels of the CCD
        if value % 2 != 0:
            raise Exception("ccd number of active columns should be an even number")
        self._ccd_active_cols = value

    # geometry values
    def _get_store_rows(self):
        return self._store_rows

    def _set_store_rows(self, rows):
        self._store_rows = rows

    storage_rows = property(_get_store_rows, _set_store_rows)

    def _get_image_rows(self):
        return self._image_rows

    def _set_image_rows(self, rows):
        self._image_rows = rows

    image_rows = property(_get_image_rows, _set_image_rows)

    def _get_total_rows(self):
        return self.storage_rows + self.image_rows

    total_rows = property(_get_total_rows)

    # Exposure values
    def _get_prescan_cols(self):
        return self._amplifier_prescan

    def _set_prescan_cols(self, rows):
        self._amplifier_prescan = rows

    prescan_cols = property(_get_prescan_cols, _set_prescan_cols)

    def _get_overscan_cols(self):
        return self._amplifier_overscan

    def _set_overscan_cols(self, rows):
        self._amplifier_overscan = rows

    overscan_cols = property(_get_overscan_cols, _set_overscan_cols)

    # Amplifiers enable or disable
    def _get_eh(self):
        return self._amplifiers_en['EH']

    def _set_eh(self, enable):
        self._set_amplifier_enable(name='EH', enable=enable)

    amplifiers_eh_enable = property(_get_eh, _set_eh)

    def _get_fg(self):
        return self._amplifiers_en['FG']

    def _set_fg(self, enable):
        self._set_amplifier_enable(name='FG', enable=enable)

    amplifiers_fg_enable = property(_get_fg, _set_fg)

    def _set_amplifier_enable(self, name, enable):
        self._amplifiers_en[name] = enable

    def _get_im_en(self):
        return self._image_shift_en

    def _set_im_en(self, value):
        self._image_shift_en = value

    image_shift_en = property(_get_im_en, _set_im_en)

    def _get_st_en(self):
        return self._store_shift_en

    def _set_st_en(self, value):
        self._store_shift_en = value

    storage_shift_en = property(_get_st_en, _set_st_en)

    def __str__(self):
        ret = ""
        for k in sorted(vars(self).keys()):
            ret += "- {0}: {1}\n".format(k, getattr(self, k, None))

        return ret


class GFADataManagerBuffer(object):
    buffer_names = ['e', 'f', 'g', 'h']

    def __init__(self, buffer_index):
        self.buffer_index = buffer_index
        self.status_word = 0
        self.contents = 0
        self.enabled_word = 0

    def _get_has_overflow(self):
        return bool(self.status_word & (1 << self.buffer_index))

    def _get_has_underflow(self):
        return bool(self.status_word & (1 << self.buffer_index+4))

    def _get_is_empty(self):
        return bool(self.status_word & (1 << self.buffer_index+8))

    def _get_is_full(self):
        return bool(self.status_word & (1 << self.buffer_index+12))

    def _get_is_enabled(self):
        """
        is enabled is referred at this current image. enabling amplifiers can change from exposure to exposure
        Returns:

        """
        return bool(self.enabled_word & (1 << self.buffer_index))

    has_overflow = property(_get_has_overflow)
    has_underflow = property(_get_has_underflow)
    is_empty = property(_get_is_empty)
    is_full = property(_get_is_full)
    is_enabled = property(_get_is_enabled)

    def __str__(self):
        tmp = ' - Buffer {0}\n'.format(self.buffer_index)
        tmp += '   - Contents: {0}\n'.format(self.contents)
        tmp += '   - Overflow: {0}\n'.format(self.has_overflow)
        tmp += '   - Underflow: {0}\n'.format(self.has_underflow)
        tmp += '   - Empty: {0}\n'.format(self.is_empty)
        tmp += '   - Full: {0}\n'.format(self.is_full)
        tmp += '   - Enabled: {0}\n'.format(self.is_enabled)
        tmp += '   - Status: {0}\n'.format(self.status_word)
        tmp += '   - enabled word: {0}\n'.format(self.enabled_word)
        return tmp


class GFADataManagerStatus(object):
    # fake_mode
    # 0: output zeros
    # 1: output ones
    # 2: e: 0, f: 1000, g: 2000, h: 3000
    # 3: e: row + col, f: row + col +1000, g: row + col +2000, h: row + col +3000
    # 4: pixel value = row
    # 5: pixel value = column
    # 6: pixel value = row x col

    def __init__(self):
        self.stream_status_word = 0
        self.buffers = [GFADataManagerBuffer(ix) for ix in range(4)]
        self.pending_lines = 0
        self.provider = 0
        self.mode = 0

    def _get_is_xferring(self):
        return bool(self.stream_status_word & (1 << 31))

    def _get_xferred_words(self):
        return self.stream_status_word | 0x3fff

    is_xferring = property(_get_is_xferring)
    xferred_words = property(_get_xferred_words)

    def __str__(self):
        tmp = ' - stream status word: {0}\n'.format(self.stream_status_word)
        tmp += ' - pending lines: {0}\n'.format(self.pending_lines)
        tmp += ' - provider : {0}\n'.format(self.provider)
        tmp += ' - mode : {0}\n'.format(self.mode)
        for el in self.buffers:
            tmp += el.__str__()
        return tmp


class GFAAdcControllerInitStatus(object):

    init_states = ['NA', 's_idle', 's_init', 's_align_frame', 's_align_data',
                   's_bitslip_frame', 's_bitslip_data']

    init_status_lines = ['done', 'ready', 'bs_finished_frame', 'i_init_busy',
                         'i_init_done', 'align_frame', 'set_init',
                         'flag1', 'flag2', 'frame_aligned', 'good_pattern',
                         'good_pattern_full', 'bs_finished_data']

    def __init__(self):
        self.init_state_value = 0
        self.init_status_line_word = 0
        self.rx_data = [0, 0, 0, 0]
        self.rx_expected_pattern = 0

    def _get_state(self):
        return self.init_states[self.init_state_value]
    state = property(_get_state)

    def is_idle(self):
        return self.state == 's_idle'

    def is_init(self):
        return self.state == 's_init'

    def __getattr__(self, item):
        if item == 'good_pattern_full':
            return ((0xff << 11) & self.init_status_line_word) >> 11
        if item == 'bs_finished_data':
            return ((0xff << 19) & self.init_status_line_word) >> 19

        try:
            ix = self.init_status_lines.index(item)
            return (self.init_status_line_word & (1 << ix)) >> ix
        except ValueError:
            raise AttributeError('{0} is not a GFAAdcControllerInitStatus attribute'.format(item))

    def __str__(self):

        tmp = ' - state: {0}\n'.format(self.state)
        for el in self.init_status_lines:
            val = getattr(self, el, None)
            if val and val > 1:
                tmp += ' - {0}: 0x{1}\n'.format(el, hex(val))
            else:
                tmp += ' - {0}: {1}\n'.format(el, val)
        tmp += ' - {0}: {1}\n'.format('rx_chan_0', hex(self.rx_data[0]))
        tmp += ' - {0}: {1}\n'.format('rx_chan_1', hex(self.rx_data[1]))
        tmp += ' - {0}: {1}\n'.format('rx_chan_2', hex(self.rx_data[2]))
        tmp += ' - {0}: {1}\n'.format('rx_chan_3', hex(self.rx_data[3]))
        tmp += ' - {0}: {1}\n'.format('rx_expected_pattern', hex(self.rx_expected_pattern))

        return tmp


class GFAAdcControllerStatus(object):

    fields = ['read_start', 'read_stop', 'NA', 'reading', 'set_calib', 'start_align_frame',
              'start_align_data', 'start_bitslip', 'stop_calib', 'calib_busy', 'spi_ready',
              'reset_adc', 'power_down', 'reset_adc_controller', 'select_cos_gen']

    def __init__(self):
        self.status_word = 0
        self.init_status = GFAAdcControllerInitStatus()

    def __getattr__(self, item):
        try:
            ix = self.fields.index(item)
            return bool(self.status_word & (1 << ix))
        except ValueError:
            raise AttributeError('{0} is not a GFAAdcControllerStatus attribute'.format(item))

    def __str__(self):

        tmp = ''
        for el in self.fields:
            tmp += ' - {0}: {1}\n'.format(el, getattr(self, el, None))
        tmp += 'Init:\n'
        tmp += str(self.init_status)
        return tmp


class GFAAdcInterfaceValues(object):
    def __init__(self):
        self.bitslip_0 = 0
        self.bitslip_1 = 0
        self.bitslip_2 = 0
        self.delays_0 = 0
        self.delays_1 = 0
        self.delays_2 = 0

    def get_bitslips(self):
        return {
            'frame': 0xff & self.bitslip_0,
            'out1': (0xff00 & self.bitslip_0) >> 8,
            'out2': (0xff0000 & self.bitslip_0) >> 16,
            'out3': (0xff000000 & self.bitslip_0) >> 24,
            'out4': 0xff & self.bitslip_1,
            'out5': (0xff00 & self.bitslip_1) >> 8,
            'out6': (0xff0000 & self.bitslip_1) >> 16,
            'out7': (0xff000000 & self.bitslip_1) >> 24,
            'out8': 0xff & self.bitslip_2
        }

    def get_delays(self):
        return {
            'frame': 0x1f & self.delays_0,
            'out1m': ((0x1f << 5) & self.delays_0) >> 5,
            'out1s': ((0x1f << 10) & self.delays_0) >> 10,
            'out2m': ((0x1f << 15) & self.delays_0) >> 15,
            'out2s': ((0x1f << 20) & self.delays_0) >> 20,
            'out3m': ((0x1f << 25) & self.delays_0) >> 25,
            'out3s': 0x1f & self.delays_1,
            'out4m': ((0x1f << 5) & self.delays_1) >> 5,
            'out4s': ((0x1f << 10) & self.delays_1) >> 10,
            'out5m': ((0x1f << 15) & self.delays_1) >> 15,
            'out5s': ((0x1f << 20) & self.delays_1) >> 20,
            'out6m': ((0x1f << 25) & self.delays_1) >> 25,
            'out6s': 0x1f & self.delays_2,
            'out7m': ((0x1f << 5) & self.delays_2) >> 5,
            'out7s': ((0x1f << 10) & self.delays_2) >> 10,
            'out8m': ((0x1f << 15) & self.delays_2) >> 15,
            'out8s': ((0x1f << 20) & self.delays_2) >> 20,
        }

    def __str__(self):
        dl = self.get_delays()
        bs = self.get_bitslips()
        l = "\n"
        tmp = 'Delays\n'
        for i, k in enumerate(dl):
            tmp += f' - {k}: {dl[k]}{l if (i+1) % 5 == 0 else ""}'
        tmp += '\nBitslips\n'
        for i, k in enumerate(bs):
            tmp += f' - {k}: {bs[k]}{l if (i+1) % 5 == 0 else ""}'
        return tmp



class DACVoltage(object):
    def __init__(self, volts, channel, name):
        self.volts = volts
        self.dac_chan = channel
        self.name = name
        self.maxV = None
        self.minV = None
        self.ext_gain = 1
        self.int_gain = 0
        self.int_offset = 0

    def _get_chantag(self):
        return 'chan_{0}'.format(self.dac_chan)

    def _counts_2_volts(self, counts):
        # Due to errors on DAC PCB
        return self.ext_gain * ((7.5 / 12000) * counts)
        # return self.ext_gain * ((10.0 / 16383) * counts - 2.5)

    def _volts_2_counts(self, volts):
        # Due to errors on DAC on PCB
        return int(round((12000 / 7.5) * ((1.0 * volts) / self.ext_gain)))
        # return int(round((16383 / 10.0) * (((1.0 * volts) / self.ext_gain) + 2.5)))

    def _get_dac_counts(self):
        return self._volts_2_counts(self.volts)

    def _set_dac_counts(self, counts):
        self.volts = self._counts_2_volts(counts)

    def _get_max_counts(self):
        return self._volts_2_counts(self.maxV)

    def _set_max_counts(self, counts):
        self.maxV = self._counts_2_volts(counts)

    def _get_min_counts(self):
        return self._volts_2_counts(self.minV)

    def _set_min_counts(self, counts):
        self.minV = self._counts_2_volts(counts)

    def _get_volt_delta(self):
        # Due to errors on DAC in PCB
        return 7.5/12000
        # return (10.0 / 16383)

    chantag = property(_get_chantag)
    dac_counts = property(_get_dac_counts, _set_dac_counts)
    max_counts = property(_get_max_counts, _set_max_counts)
    min_counts = property(_get_min_counts, _set_min_counts)
    volts_delta = property(_get_volt_delta)

    def __str__(self):
        tmp = ""
        for attr in ['volts', 'dac_chan', 'name', 'maxV', 'minV', 'chantag', 'dac_counts',
                     'min_counts', 'max_counts', 'ext_gain', 'int_gain', 'int_offset',
                     'volts_delta']:
            tmp += " - {0}: {1}\n".format(attr, getattr(self, attr))
        return tmp


class DACVoltageSet(object):
    def __init__(self):
        self._by_chan = {}
        self._by_chantag = {}
        self._by_name = {}

    def add(self, dacvoltage):
        self._by_chan[dacvoltage.dac_chan] = dacvoltage
        self._by_chantag[dacvoltage.chantag] = dacvoltage
        self._by_name[dacvoltage.name] = dacvoltage

    def get_by_chan(self, chan):
        return self._by_chan[chan]

    def get_by_chantag(self, chantag):
        return self._by_chantag[chantag]

    def get_by_name(self, name):
        return self._by_name[name]


class GFADacChannels(object):
    def __init__(self):
        self.binary = 0

    def is_configured(self, chan):
        return bool(self.binary & (1 << chan))

    def __str__(self):
        ix = 0
        tmp = 'Configured dac channels:\n'
        while ix < 32:
            tmp += "{0:2}: {1}   {2:2}: {3}   {4:2}: {5}   {6:2}: {7}\n".format(ix,
                                                                                bool(self.is_configured(ix)),
                                                                                ix + 1,
                                                                                bool(self.is_configured(ix + 1)),
                                                                                ix + 2,
                                                                                bool(self.is_configured(ix + 2)),
                                                                                ix + 3,
                                                                                bool(self.is_configured(ix + 3)),
                                                                                )
            ix += 4

        return tmp


class GFAVoltagesConfiguration(object):
    """
    Check https://docs.google.com/spreadsheets/d/19A1WYV7GNeFB4azF0UVjV-AvPpEc_VadSdhTTeCGuDI/edit#gid=0
    To know correlations with ccd pins
    """

    def __init__(self):
        self.RD = DACVoltage(18.0, 0, 'RD')
        self.I02_IM_hi = DACVoltage(11.0, 1, 'I02_IM_hi')
        self.I03_IM_low = DACVoltage(0.0, 2, 'I03_IM_low')
        self.I04_ST_hi = DACVoltage(11.0, 3, 'I04_ST_hi')
        self.I03_ST_low = DACVoltage(0.0, 4, 'I03_ST_low')
        self.I04_IM_hi = DACVoltage(11.0, 5, 'I04_IM_hi')
        self.I03_ST_hi = DACVoltage(11.0, 6, 'I03_ST_hi')
        self.I02_IM_low = DACVoltage(0.0, 7, 'I02_IM_low')
        self.DG_hi = DACVoltage(11.3, 8, 'DG_hi')
        self.I01_ST_hi = DACVoltage(11.0, 9, 'I01_ST_hi')
        self.R02_hi = DACVoltage(11.0, 10, 'R02_hi')
        self.I02_ST_hi = DACVoltage(11.0, 11, 'I02_ST_hi')
        self.I03_IM_hi = DACVoltage(11.0, 12, 'I03_IM_hi')
        self.I02_ST_low = DACVoltage(0.0, 13, 'I02_ST_low')
        self.I01_IM_hi = DACVoltage(11.0, 14, 'I01_IM_hi')
        self.I04_ST_low = DACVoltage(0.0, 15, 'I04_ST_low')
        self.I01_IM_low = DACVoltage(0.0, 16, 'I01_IM_low')
        self.RG_low = DACVoltage(0.0, 17, 'RG_low')
        self.I01_ST_low = DACVoltage(0.0, 18, 'I01_ST_low')
        self.R01_low = DACVoltage(0.0, 19, 'R01_low')
        self.DG_low = DACVoltage(0.0, 20, 'DG_low')
        self.R01_hi = DACVoltage(11.0, 21, 'R01_hi')
        self.R03_hi = DACVoltage(11.0, 22, 'R03_hi')
        self.RG_hi = DACVoltage(11.0, 23, 'RG_hi')
        self.R03_low = DACVoltage(0.0, 24, 'R03_low')
        self.R02_low = DACVoltage(0.0, 25, 'R02_low')
        self.I04_IM_low = DACVoltage(0.0, 26, 'I04_IM_low')
        self.OD_EH = DACVoltage(30.8, 27, 'OD_EH')
        self.VSS = DACVoltage(9.0, 28, 'VSS')
        self.DD = DACVoltage(30.0, 29, 'DD')
        self.OG = DACVoltage(3.0, 30, 'OG')
        self.OD_FG = DACVoltage(30.0, 31, 'OD_FG')

        self.powerup_ms = 0
        self.powerdown_ms = 0

        self._set = DACVoltageSet()
        self._build_set()

    def _build_set(self):
        self._set.add(self.RD)
        self._set.add(self.OD_EH)
        self._set.add(self.OD_FG)
        self._set.add(self.OG)
        self._set.add(self.DD)
        self._set.add(self.VSS)
        self._set.add(self.I01_ST_low)
        self._set.add(self.I01_ST_hi)
        self._set.add(self.I02_ST_low)
        self._set.add(self.I02_ST_hi)
        self._set.add(self.I03_ST_low)
        self._set.add(self.I03_ST_hi)
        self._set.add(self.I04_ST_low)
        self._set.add(self.I04_ST_hi)
        self._set.add(self.I01_IM_low)
        self._set.add(self.I01_IM_hi)
        self._set.add(self.I02_IM_low)
        self._set.add(self.I02_IM_hi)
        self._set.add(self.I03_IM_low)
        self._set.add(self.I03_IM_hi)
        self._set.add(self.I04_IM_low)
        self._set.add(self.I04_IM_hi)
        self._set.add(self.DG_low)
        self._set.add(self.DG_hi)
        self._set.add(self.R01_low)
        self._set.add(self.R01_hi)
        self._set.add(self.R02_low)
        self._set.add(self.R02_hi)
        self._set.add(self.R03_low)
        self._set.add(self.R03_hi)
        self._set.add(self.RG_low)
        self._set.add(self.RG_hi)

    def set_default_values(self):
        """Sets configuration to default values
        """

        self.RD.volts = 18.5
        self.OD_EH.volts = 30.7
        self.OD_FG.volts = 30.7
        self.OG.volts = 3.3
        self.DD.volts = 30.8
        self.VSS.volts = 9.4
        self.I01_ST_low.volts = 0.0
        self.I01_ST_hi.volts = 11.35
        self.I02_ST_low.volts = 0.0
        self.I02_ST_hi.volts = 11.35
        self.I03_ST_low.volts = 0.0
        self.I03_ST_hi.volts = 11.35
        self.I04_ST_low.volts = 0.0
        self.I04_ST_hi.volts = 11.35
        self.I01_IM_low.volts = 0.0
        self.I01_IM_hi.volts = 11.35
        self.I02_IM_low.volts = 0.0
        self.I02_IM_hi.volts = 11.35
        self.I03_IM_low.volts = 0.0
        self.I03_IM_hi.volts = 11.35
        self.I04_IM_low.volts = 0.0
        self.I04_IM_hi.volts = 11.35
        self.DG_low.volts = 0.0
        self.DG_hi.volts = 11.3
        self.R01_low.volts = 0.0
        self.R01_hi.volts = 11.0
        self.R02_low.volts = 0.0
        self.R02_hi.volts = 11.0
        self.R03_low.volts = 0.0
        self.R03_hi.volts = 11.0
        self.RG_low.volts = 0.0
        self.RG_hi.volts = 11.35
        self.powerdown_ms = 250
        self.powerup_ms = 250

    def set_test_values(self):
        """Sets configuration to default values
        """

        self.RD.volts = 4.0
        self.OD_EH.volts = 4.0
        self.OD_FG.volts = 4.0
        self.OG.volts = 4.0
        self.DD.volts = 4.0
        self.VSS.volts = 4.0
        self.I01_ST_low.volts = 0.0
        self.I01_ST_hi.volts = 4.0
        self.I02_ST_low.volts = 0.0
        self.I02_ST_hi.volts = 4.0
        self.I03_ST_low.volts = 0.0
        self.I03_ST_hi.volts = 4.0
        self.I04_ST_low.volts = 0.0
        self.I04_ST_hi.volts = 4.0
        self.I01_IM_low.volts = 0.0
        self.I01_IM_hi.volts = 4.0
        self.I02_IM_low.volts = 0.0
        self.I02_IM_hi.volts = 4.0
        self.I03_IM_low.volts = 0.0
        self.I03_IM_hi.volts = 4.0
        self.I04_IM_low.volts = 0.0
        self.I04_IM_hi.volts = 4.0
        self.DG_low.volts = 0.0
        self.DG_hi.volts = 4.0
        self.R01_low.volts = 0.0
        self.R01_hi.volts = 4.0
        self.R02_low.volts = 0.0
        self.R02_hi.volts = 4.0
        self.R03_low.volts = 0.0
        self.R03_hi.volts = 4.0
        self.RG_low.volts = 0.0
        self.RG_hi.volts = 4.0

    def set_zeroes(self):
        """Sets configuration to default values
        """

        self.RD.volts = 0.0
        self.OD_EH.volts = 0.0
        self.OD_FG.volts = 0.0
        self.OG.volts = 0.0
        self.DD.volts = 0.0
        self.VSS.volts = 0.0
        self.I01_ST_low.volts = 0.0
        self.I01_ST_hi.volts = 0.0
        self.I02_ST_low.volts = 0.0
        self.I02_ST_hi.volts = 0.0
        self.I03_ST_low.volts = 0.0
        self.I03_ST_hi.volts = 0.0
        self.I04_ST_low.volts = 0.0
        self.I04_ST_hi.volts = 0.0
        self.I01_IM_low.volts = 0.0
        self.I01_IM_hi.volts = 0.0
        self.I02_IM_low.volts = 0.0
        self.I02_IM_hi.volts = 0.0
        self.I03_IM_low.volts = 0.0
        self.I03_IM_hi.volts = 0.0
        self.I04_IM_low.volts = 0.0
        self.I04_IM_hi.volts = 0.0
        self.DG_low.volts = 0.0
        self.DG_hi.volts = 0.0
        self.R01_low.volts = 0.0
        self.R01_hi.volts = 0.0
        self.R02_low.volts = 0.0
        self.R02_hi.volts = 0.0
        self.R03_low.volts = 0.0
        self.R03_hi.volts = 0.0
        self.RG_low.volts = 0.0
        self.RG_hi.volts = 0.0

    def __str__(self):
        tmp = ''
        for i in range(32):
            chan = self.get_by_chan(i)
            tmp += " - {0:11}:  {1:5.2f}\t([{2:5.2f}, {3:5.2f}]) - G: {4:5.2f}\n".format(chan.name,
                                                                                      chan.volts,
                                                                                      chan.minV,
                                                                                      chan.maxV,
                                                                                      chan.ext_gain
                                                                                      )
        return tmp

    def get_by_chan(self, chan):
        return self._set.get_by_chan(chan)

    def get_by_chantag(self, chantag):
        return self._set.get_by_chantag(chantag)

    def get_by_name(self, name):
        return self._set.get_by_name(name)

    def update(self, other):
        if not isinstance(other, GFAVoltagesConfiguration):
            raise Exception('other must be a GFAVoltagesConfiguration instance')
        for i in range(32):
            this = self.get_by_chan(i)
            that = other.get_by_chan(i)
            this.volts = that.volts

        self.powerdown_ms = other.powerdown_ms
        self.powerup_ms = other.powerup_ms


class GFAStatusType(object):
    idle = 0
    configured = 1
    power_up = 2
    power_down = 3
    ready = 4
    error = 5
    exposing = 6
    telemetry =7


class GFAStatus(object):
    def __init__(self):
        self.state = GFAStatusType.idle
        # self.integration_progress = 0.0  # % of integration time (meaningful only on integration)
        # self.integrated_ms = 0.0  # current exposure how many ms have been integrating
        # self.acq_progress = 0.0  # when status is acquiring, % of total rows to be read
        self.horizontal_transfers = 0  # how many horizontal charge transfers have been processed in current exposure
        self.vertical_transfers = 0  # how many vertical charge transfers have been processed in current exposure
        self.exposure_id = None  # exposure id of last exposure started
        self.bias_enabled = False


class GFAIRQControllerStatus(object):
    """
    Class to hold status of the IRQ Controller on the GFA
        - received fields refers to how many rise pulses has the irq received
        - processed fields refers to how many times the irq cleared that type of interrupt
        - clear_us fields refer to how much microseconds elapsed between the last interrupt
            rose and the controller cleared it
    """
    def __init__(self):
        self.status_bits = 0
        self.received_img_start = 0
        self.received_line = 0
        self.received_ccd_done = 0
        self.received_telemetry = 0

        self.processed_img_start = 0
        self.processed_line = 0
        self.processed_ccd_done = 0
        self.processed_telemetry = 0

        self.clear_us_img_start = 0
        self.clear_us_line = 0
        self.clear_us_ccd_done = 0
        self.clear_us_telemetry = 0

    def _get_active_new_exposure(self):
        return bool(self.status_bits & (1<<2))

    def _get_active_line(self):
        return bool(self.status_bits & (1 << 3))

    def _get_active_ccd_done(self):
        return bool(self.status_bits & (1 << 4))

    def _get_active_telemetry(self):
        return bool(self.status_bits & (1 << 5))

    image_start = property(_get_active_new_exposure)
    line = property(_get_active_line)
    ccd_done = property(_get_active_ccd_done)
    telemetry = property(_get_active_telemetry)

    def __str__(self):
        tmp = ""
        fields = ["status_bits"
                   , "received_img_start" , "received_line", "received_ccd_done", "received_telemetry"
                   , "processed_img_start" , "processed_line", "processed_ccd_done", "processed_telemetry"
                   , "clear_us_img_start" , "clear_us_line", "clear_us_ccd_done", "clear_us_telemetry"]
        for el in fields:
            tmp += " - {0}: {1}\n".format(el, getattr(self, el))
        return tmp


class GFATelemetryVoltageValue(object):
    """Class to hold sensors data
        name: sensor name
        value: current value
        dt: datetime of last value update
    """

    def __init__(self, name, adc_lsb: float=0, gain: float=1, offset: float=0):
        self.name = name
        self.counts = 0
        self._lsb = adc_lsb
        self._gain = gain
        self._offset = offset
        self.dt = 0

    @property
    def value(self):
        return self.counts*self._lsb*self._gain + self._offset
        # return (self.counts*self._lsb + self._offset)*self._gain

AD7490_VOLTAGE_FULL_SCALE = 2.5
AD7490_BITS = 12
AD7490_LSB = AD7490_VOLTAGE_FULL_SCALE/(2**AD7490_BITS)

'''
Pepe mail
Bias: 1M, 200k referenciat a GND   =>   V = Vm * 6

CLK: 1M, 180k referenciat a 0.4V    =>   V= (Vm * 6.55) - 2.22

Vm = counts * 2.5/2^12

20180921:
BIAS: 1M, 68K => gain: 15.7
Clocks: 1M, 180K => gain = 6.55, offset -13.8

V = Vm(1 + R1/R2) - Vref(R1/R2)
'''
CLOCKS_R1 = 1000000
CLOCKS_R2 = 180000
CLOCKS_Vref = 0.4
CLOCKS_OFFSET = -1.0*CLOCKS_Vref*CLOCKS_R1/CLOCKS_R2
CLOCKS_GAIN = (1.0 + 1.0*CLOCKS_R1/CLOCKS_R2)
BIAS_R1 = 1000000
BIAS_R2 = 68000
BIAS_Vref = 0
BIAS_OFFSET = -1.0*BIAS_Vref*BIAS_R1/BIAS_R2
BIAS_GAIN = (1.0 + 1.0*BIAS_R1/BIAS_R2)


class GFATelemetryVoltages(object):
    def __init__(self):

        self.updated_on = None
        self.acq_time_ns = None
        self.powerdown = False

        self._values = {}

        self._add_value(GFATelemetryVoltageValue("a1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a3_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a3_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a4_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("a4_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("b1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b3_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b3_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b4_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("b4_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("c1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c3_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c3_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c4_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("c4_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("d1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d3_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d3_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d4_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("d4_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("dd", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("dga_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("dga_low", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("dgd_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("dgd_low", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("e1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("e1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("e2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("e2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("e3f3_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("e3f3_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("f1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("f1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("f2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("f2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("g1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("g1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("g2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("g2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("g3h3_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("g3h3_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("h1_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("h1_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("h2_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("h2_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("ode", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("odf", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("odg", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("odh", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("og", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rd", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("rge_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rge_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rgf_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rgf_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rgg_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rgg_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rgh_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("rgh_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("sweswf_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("sweswf_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("swgswh_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("swgswh_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("tga_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("tga_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("tgd_high", adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))
        self._add_value(GFATelemetryVoltageValue("tgd_low",  adc_lsb=AD7490_LSB, gain=CLOCKS_GAIN, offset=CLOCKS_OFFSET))

        self._add_value(GFATelemetryVoltageValue("vss", adc_lsb=AD7490_LSB, gain=BIAS_GAIN, offset=BIAS_OFFSET))

    def __getattr__(self, item):
        return self._values.get(item)

    def get(self, name, default_value=None):
        return self._values.get(name, default_value)

    def _add_value(self, value):
        self._values[value.name] = value
        
    def update(self, values, ignore_invalid=False):
        for k, v in values.items():
            if k == "time_to_capture":
                self._values[k] = v
            elif k == "live_time":
                self._values[k] = v
            else:
                m = re.match(r'(.*)?_(ms|value|raw_register)', k)
                if m:
                    m = m.groups()
                    item = self._values.get(m[0], None)
                    if item:
                        if m[1] == 'value':
                            item.counts = int(v)
                        elif m[1] == 'ms':
                            item.dt = datetime.datetime.utcnow() - datetime.timedelta(milliseconds=v)
                        elif m[1] == 'raw_register':
                            # raw value is unused
                            pass
                else:
                    if not ignore_invalid:
                        print("Error updating key: {}:{}".format(k, v))
                self.updated_on = datetime.datetime.utcnow()

    def update_dt(self, delta):
        self.updated_on = datetime.datetime.utcnow() - datetime.timedelta(milliseconds=delta)

    def __repr__(self):
        t  = "Telemetry values\n"
        t += "------------------\n"
        t += " - powerdown: {}\n".format(self.powerdown)
        t += " - acq time ns: {}\n".format(self.acq_time_ns)
        t += " - updated on: {}\n".format(self.updated_on)
        if self.updated_on:
            td = datetime.datetime.utcnow() - self.updated_on
            t += " - updated {} seconds ago\n".format(td.seconds)
            t += "------------------\n"
            for el in sorted(self._values.keys()):
                if el != "time_to_capture" and el != "live_time":
                    # t += " - {}: {}V (counts: {} - dt: {})\n".format(el, self._values[el].value, self._values[el].counts,
                    #                                                   self._values[el].dt)
                    t += " - {}:  {:.3f}V\n".format(el, self._values[el].value, self._values[el].counts,
                                                                  self._values[el].dt)
        return t


class GFATelemetry(object):
    
    def __init__(self):
        self.ccd_voltages = GFATelemetryVoltages()
    

class GFATelemetryConfig(object):
    def __init__(self):
        self.read_sensors_on_ccd_read = None
        self.sensors_update_time = None  # Time in milliseconds. how often, DACs on GFA are accessed
        self.set_default_values()

    def set_default_values(self):
        self.read_sensors_on_ccd_read = False
        self.sensors_update_time = 1000  # Time in milliseconds. how often, Sensors on GFA are accessed
        # to update sensors values


class GFAInterlocksConfig(object):
    def __init__(self):
        self.powerdown_by_ccd_temp = 2  # How many of the available temperature sensors (there are 4) must be above
        # max_ccd_temp to power down the system. If set to 0 or > 4, the GFA won't
        # be automatically powered down
        self.max_ccd_temp = 50  # Temperature in degrees

        self.powerdown_on_pcb_temp = True
        self.max_pcb_temp = 60


class HeartBeatStatus(object):
    def __init__(self):
        self.address = None
        self.enabled = False
        self.interval = None
        self.retries = None
        self.errors = 0
        self.last_ping_ts = 0
        self.last_ping_error_ts = 0

    def __str__(self):
        return f"""HeartBeat Status
    - address: {self.address}
    - enabled: {'true' if self.enabled else 'false'}
    - interval: {self.interval} s
    - retries: {self.retries}
    - current_errors: {self.errors}
    - last ping: {pytz.utc.localize(datetime.datetime.fromtimestamp(self.last_ping_ts)) if self.last_ping_ts else 'NA'}
    - last error ping: {pytz.utc.localize(datetime.datetime.fromtimestamp(self.last_ping_error_ts)) if self.last_ping_error_ts else 'NA'} 
    """



