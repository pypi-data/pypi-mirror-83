from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFATimeConfiguration, GFACCDGeom, \
    GFAExposureStack, GFAClockManagerStatus, GFAClockManagerInfo
from gfaaccesslib.modules.gfamodule import GFAModule
from .logger import log

__author__ = 'otger'


class ClockManager(GFAModule):
    def __init__(self, communication_manager):
        super(ClockManager, self).__init__(communication_manager)

        self._time_conf = GFATimeConfiguration()
        self._time_conf.set_default_values()
        self._geom_conf = GFACCDGeom()
        self._geom_conf.set_default_values()
        self._stack = GFAExposureStack()
        # self._status = GFAClockManagerStatus()
        self._info = GFAClockManagerInfo()

    def _get_time_conf(self):
        return self._time_conf

    def _get_geom_conf(self):
        return self._geom_conf

    def _get_stack(self):
        return self._stack

    def _get_status(self):
        return self._info.status

    def _get_info(self):
        return self._info

    time_conf = property(_get_time_conf)
    geom_conf = property(_get_geom_conf)
    stack = property(_get_stack)
    status = property(_get_status)
    info = property(_get_info)

    def remote_set_clock_timings(self, gfa_time_conf: GFATimeConfiguration = None):
        """
        Access gfa and set a new time configuration. If gfa_time_conf parameter is None, it uses self.time_conf values

        :param gfa_time_conf: New configuration to be set at gfa. If set, updates self.time_conf.
            If not set, self.time_conf is set on GFA device
        """
        if gfa_time_conf:
            self._time_conf.update(gfa_time_conf)

        c = CommandPacket(command='clockman.set_clock_timings', module='clockmanager')
        # if self._time_conf.vert_tdrt is not None:
        #     c.set_arg('vert_tdrt', self._time_conf.vert_tdrt)
        # if self._time_conf.vert_toi is not None:
        #     c.set_arg('vert_toi', self._time_conf.vert_toi)
        # if self._time_conf.vert_tdtr is not None:
        #     c.set_arg('vert_tdtr', self._time_conf.vert_tdtr)
        # if self._time_conf.vert_tdrg is not None:
        #     c.set_arg('vert_tdrg', self._time_conf.vert_tdrg)
        # if self._time_conf.vert_tdgr is not None:
        #     c.set_arg('vert_tdgr', self._time_conf.vert_tdgr)
        # if self._time_conf.hor_del is not None:
        #     c.set_arg('hor_del', self._time_conf.hor_del)
        # if self._time_conf.hor_del_skip is not None:
        #     c.set_arg('hor_del_skip', self._time_conf.hor_del_skip)
        # if self._time_conf.hor_acq is not None:
        #     c.set_arg('hor_acq', self._time_conf.hor_acq)
        # if self._time_conf.hor_acq_skip is not None:
        #     c.set_arg('hor_acq_skip', self._time_conf.hor_acq_skip)
        # if self._time_conf.hor_prerg is not None:
        #     c.set_arg('hor_prerg', self._time_conf.hor_prerg)
        # if self._time_conf.hor_prerg_skip is not None:
        #     c.set_arg('hor_prerg_skip', self._time_conf.hor_prerg_skip)
        # if self._time_conf.hor_rg is not None:
        #     c.set_arg('hor_rg', self._time_conf.hor_rg)
        # if self._time_conf.hor_rg_skip is not None:
        #     c.set_arg('hor_rg_skip', self._time_conf.hor_rg_skip)
        # if self._time_conf.hor_postrg is not None:
        #     c.set_arg('hor_postrg', self._time_conf.hor_postrg)
        # if self._time_conf.hor_postrg_skip is not None:
        #     c.set_arg('hor_postrg_skip', self._time_conf.hor_postrg_skip)
        # if self._time_conf.hor_overlap is not None:
        #     c.set_arg('hor_overlap', self._time_conf.hor_overlap)
        # if self._time_conf.hor_overlap_skip is not None:
        #     c.set_arg('hor_overlap_skip', self._time_conf.hor_overlap_skip)
        #
        # if self._time_conf.reset_wait is not None:
        #     c.set_arg('reset_wait', self._time_conf.reset_wait)
        # if self._time_conf.reset_acq is not None:
        #     c.set_arg('reset_acq', self._time_conf.reset_acq)

        for field_name in self._time_conf.fields:
            field_value = getattr(self._time_conf, field_name, None)
            if field_value is not None:
                c.set_arg(field_name, field_value)

        ans = self._comm.exec_std_command(c)
        log.debug('SetClockTimings values: {0}'.format(ans.json))

        return ans

    def remote_get_clock_timings(self):
        """
        Retrieves clock timing configuration from GFA and updates self.time_conf
        """
        c = CommandPacket(command='clockman.get_clock_timings', module='clockmanager')

        ans = self._comm.exec_std_command(c)
        gfa_time_conf = GFATimeConfiguration()
        for field_name in gfa_time_conf.fields:
            setattr(gfa_time_conf, field_name, ans.get_ans(field_name))
        # gfa_time_conf.vert_tdrt = ans.get_ans('vert_tdrt')
        # gfa_time_conf.vert_toi = ans.get_ans('vert_toi')
        # gfa_time_conf.vert_tdtr = ans.get_ans('vert_tdtr')
        # gfa_time_conf.vert_tdrg = ans.get_ans('vert_tdrg')
        # gfa_time_conf.vert_tdgr = ans.get_ans('vert_tdgr')
        # gfa_time_conf.hor_del = ans.get_ans('hor_del')
        # gfa_time_conf.hor_del_skip = ans.get_ans('hor_del_skip')
        # gfa_time_conf.hor_acq = ans.get_ans('hor_acq')
        # gfa_time_conf.hor_acq_skip = ans.get_ans('hor_acq_skip')
        # gfa_time_conf.hor_prerg = ans.get_ans('hor_prerg')
        # gfa_time_conf.hor_prerg_skip = ans.get_ans('hor_prerg_skip')
        # gfa_time_conf.hor_rg = ans.get_ans('hor_rg')
        # gfa_time_conf.hor_rg_skip = ans.get_ans('hor_rg_skip')
        # gfa_time_conf.hor_postrg = ans.get_ans('hor_postrg')
        # gfa_time_conf.hor_postrg_skip = ans.get_ans('hor_postrg_skip')
        # gfa_time_conf.hor_overlap = ans.get_ans('hor_overlap')
        # gfa_time_conf.hor_overlap_skip = ans.get_ans('hor_overlap_skip')

        self._time_conf.update(gfa_time_conf)
        return ans

    def remote_set_ccd_geom(self, gfa_ccd_geom: GFACCDGeom = None):
        """
        Updates GFA device geometry settings

        :param gfa_ccd_geom: if not set, self.geom_conf values is used. If set, self.geom_conf is updated
        :return:
        """
        if gfa_ccd_geom:
            self._geom_conf.update(gfa_ccd_geom)

        c = CommandPacket(command='clockman.set_ccd_geom', module='clockmanager')
        if gfa_ccd_geom:
            self._geom_conf.update(gfa_ccd_geom)

        # c.set_arg('storage_rows', self._geom_conf.storage_rows)
        # c.set_arg('image_rows', self._geom_conf.image_rows)
        c.set_arg('prescan_cols', self._geom_conf.prescan_cols)
        c.set_arg('overscan_cols', self._geom_conf.overscan_cols)
        c.set_arg('amplifier_active_cols', self._geom_conf.amplifier_active_cols)

        enables = 0
        if self._geom_conf.amplifiers_eh_enable:
            enables |= (1 << 3)
        if self._geom_conf.amplifiers_fg_enable:
            enables |= (1 << 2)
        if self._geom_conf.image_shift_en:
            enables |= (1 << 1)
        if self._geom_conf.storage_shift_en:
            enables |= (1 << 0)
        log.debug('Enables: {0}'.format(enables))
        c.set_arg('clock_status_shift_enables', enables)

        ans = self._comm.exec_std_command(c)
        log.debug('Set geometry values: {0}'.format(ans.json))
        return ans

    def remote_get_ccd_geom(self):
        """
        Retrieves current geometry settings configured on GFA device and updates self.geom_conf

        :return:
        """
        c = CommandPacket(command='clockman.get_ccd_geom', module='clockmanager')

        ans = self._comm.exec_std_command(c)
        log.debug('get_ccd_geometry answer: {0}'.format(ans.json))
        # self._geom_conf.storage_rows = ans.get_ans('storage_rows') or 0
        # self._geom_conf.image_rows = ans.get_ans('image_rows') or 0
        self._geom_conf.prescan_cols = ans.get_ans('prescan_cols') or 0
        self._geom_conf.overscan_cols = ans.get_ans('overscan_cols') or 0

        enables = ans.get_ans('clock_status_shift_enables')
        log.debug('Amplifier enables: {0}'.format(enables))

        self._geom_conf.amplifiers_eh_enable = bool(enables & 0x8)
        self._geom_conf.amplifiers_fg_enable = bool(enables & 0x4)
        self._geom_conf.image_shift_en = bool(enables & 0x2)
        self._geom_conf.storage_shift_en = bool(enables & 0x1)

        # This must be the last one
        self._geom_conf.amplifier_active_cols = ans.get_ans('amplifier_active_cols')

        return ans

    def remote_get_stack_contents(self):

        c = CommandPacket(command='clockman.get_stack_contents', module='clockmanager')

        ans = self._comm.exec_std_command(c)

        self.stack.commands = [('0'*32 + bin(el)[2:])[-32:] for el in ans.get_ans('commands_uint')]

        return ans

    def remote_set_stack_contents(self, exposure_stack: GFAExposureStack = None):
        if exposure_stack:
            if not isinstance(exposure_stack, GFAExposureStack):
                raise Exception('Exposure stack must be an instance of GFAExposureStack')
            self._stack.update(exposure_stack)

        c = CommandPacket(command='clockman.set_stack_contents', module='clockmanager')
        c.set_arg('commands', self._stack.commands)
        ans = self._comm.exec_std_command(c)

        return ans

    def remote_get_info(self):
        return self.remote_get_status()

    def remote_get_status(self):

        c = CommandPacket(command='clockman.get_status', module='clockmanager')
        ans = self._comm.exec_std_command(c)
        # self.status.status = ans.get_ans('status_bits')

        # answer contains:
        # "status_bits", "processed_vertical",
        # "processed_horizontal", "current_row", "current_col", "current_command",
        # "next_command", "exec_pointer", "write_pointer", "read_pointer",
        # "read_pointer_data", "exposure_id", "registers_configured_0",
        #  "registers_configured_1"
        self.info.update_info(ans.answer)

        return ans

    def remote_enable_discharge(self, length: int, pixel_start: bool = False, reset_start: bool = False):
        c = CommandPacket(command="clockman.set_discharge_conf", module="clockmanager")
        c.set_arg("discharge_duration", length)
        c.set_arg("reset_start", reset_start)
        c.set_arg("pixel_start", pixel_start)
        ans = self._comm.exec_std_command(c)

        return ans

    def remote_disable_discharge(self):
        c = CommandPacket(command="clockman.set_discharge_conf", module="clockmanager")
        c.set_arg("discharge_duration", 0)
        c.set_arg("reset_start", False)
        c.set_arg("pixel_start", False)
        ans = self._comm.exec_std_command(c)

        return ans

    def remote_get_discharge_config(self):
        c = CommandPacket(command="clockman.get_discharge_conf", module="clockmanager")
        ans = self._comm.exec_std_command(c)

        return ans

    def _operate(self, clear_stack, clear_execution_pointer, force_start):
        c = CommandPacket(command='clockman.modify_status', module='clockmanager')
        c.set_arg('clear_stack', bool(clear_stack))
        c.set_arg('clear_exec_p', bool(clear_execution_pointer))
        c.set_arg('force_start', bool(force_start))

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_clear_stack(self):
        return self._operate(True, False, False)

    def remote_clear_stack_execution_pointer(self):
        return self._operate(False, True, False)

    def remote_force_execution_start(self):
        return self._operate(False, False, True)

    def remote_get_tr_regs(self):
        c = CommandPacket(command='clockman.get_tr_regs', module='clockmanager')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_tr_reg(self, tr_addr: int):
        c = CommandPacket(command='clockman.get_tr_reg', module='clockmanager')
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_tr_value(self, value: int, tr_addr: int):
        c = CommandPacket(command='clockman.set_tr_value', module='clockmanager')
        c.set_arg('value', value)
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_clear_tr(self, tr_addr: int):
        c = CommandPacket(command='clockman.clear_tr', module='clockmanager')
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_clear_all_tr(self):
        c = CommandPacket(command='clockman.clear_all_tr', module='clockmanager')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_start_tr(self, tr_addr: int, resolution: int):
        c = CommandPacket(command='clockman.start_tr', module='clockmanager')
        c.set_arg('addr', tr_addr)
        c.set_arg('resolution', resolution)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_stop_tr(self, tr_addr: int):
        c = CommandPacket(command='clockman.stop_tr', module='clockmanager')
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_increase_tr(self, tr_addr: int):
        c = CommandPacket(command='clockman.increase_tr', module='clockmanager')
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_decrease_tr(self, tr_addr: int):
        c = CommandPacket(command='clockman.decrease_tr', module='clockmanager')
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_tr_status(self, tr_addr: int):
        c = CommandPacket(command='clockman.get_tr_status', module='clockmanager')
        c.set_arg('addr', tr_addr)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_start_time_thread(self, addr_s: int, addr_ms: int, sleep_s: int):
        c = CommandPacket(command="clockman.start_time_thread", module='clockmanager')
        c.set_arg('addr_s', addr_s)
        c.set_arg('addr_ms', addr_ms)
        c.set_arg('sleep_s', sleep_s)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_join_time_thread(self):
        c = CommandPacket(command='clockman.join_time_thread', module='clockmanager')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_cancel_stack_exec(self):
        c = CommandPacket(command='clockman.cancel_stack_exec')

        ans = self._comm.exec_std_command(c)
        log.debug('Cancel stack exec answer: {}'.format(ans.json))
        return ans
