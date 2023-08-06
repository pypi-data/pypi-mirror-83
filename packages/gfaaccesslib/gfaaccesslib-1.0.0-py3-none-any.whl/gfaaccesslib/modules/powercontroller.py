from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFAVoltagesConfiguration, GFAVoltageEnables, GFADacChannels
from .gfamodule import GFAModule
from .logger import log

__author__ = 'otger'


class PowerController(GFAModule):
    """

        When system power ups (or down), it enables (disables) the switch enables by groups. Between groups it waits for
            a configured amount of time.

        :param powerup_timing_ms: time between switching on enables of different groups in milliseconds
        :param powerdown_timing_ms: time between switching off enables of different groups in milliseconds
    """

    def __init__(self, communication_manager, auto_update=True):
        super(PowerController, self).__init__(communication_manager)

        self.powerup_timing_ms = 0
        self.powerdown_timing_ms = 0

        self._enables = GFAVoltageEnables()
        self._volt_conf = GFAVoltagesConfiguration()
        self._channels = GFADacChannels()

        if auto_update:
            self.remote_update_hw_conf()

    def _get_enables(self):
        return self._enables

    def _get_volt_conf(self):
        return self._volt_conf

    def _get_dac_channels(self):
        return self._channels

    enables = property(_get_enables)
    voltages = property(_get_volt_conf)
    dac_channels = property(_get_dac_channels)

    def remote_spi_write(self, value: int):
        c = CommandPacket(command='pwr.spi_write')
        c.set_arg("value", value)
        ans = self._comm.exec_std_command(c)
        log.debug("Spi writed: {}".format(ans.json))

        return ans

    def remote_get_configured_channels(self):
        c = CommandPacket(command='pwr.get_configured_channels')
        ans = self._comm.exec_std_command(c)
        log.debug('get_configured_channels values: {0}'.format(ans.json))

        self._channels.binary = ans.get_ans('binary')

        return ans

    def remote_get_dac_counts_valid_ranges(self):
        c = CommandPacket(command='pwr.get_dac_counts_valid_ranges')
        ans = self._comm.exec_std_command(c)
        log.debug('get_dac_counts_valid_ranges values: {0}'.format(ans.json))

        for i in range(32):
            values = ans.get_ans('chan_{0}'.format(i))
            if values:
                chan = self.voltages.get_by_chan(i)
                chan.max_counts = values['max']
                chan.min_counts = values['min']
        return ans

    def remote_get_external_gains(self):
        c = CommandPacket(command='pwr.get_external_gain')
        ans = self._comm.exec_std_command(c)
        log.debug('get_external_gain values: {0}'.format(ans.json))

        for i in range(32):
            values = ans.get_ans('chan_{0}'.format(i))
            if values:
                self.voltages.get_by_chan(i).ext_gain = values/1000.0

        return ans

    def remote_update_hw_conf(self):
        """
        Asks for maximum and minimum allowed values for each channel

        Asks for external amplifier gain
        Configures voltages
        :return:
        """

        self.remote_get_external_gains()
        self.remote_get_dac_counts_valid_ranges()
        self.remote_get_phase_timing()
        self.remote_get_configured_channels()

    def remote_set_voltages(self):
        """
        Applies configured voltages on self.voltages to GFA

        :return:
        """

        c = CommandPacket(command='pwr.set_dac_counts')

        for i in range(32):
            chan = self._volt_conf.get_by_chan(i)
            c.set_arg(chan.chantag, chan.dac_counts)

        ans = self._comm.exec_std_command(c)
        log.debug('set_dac_countss values: {0}'.format(ans.json))

        # Update voltage values on self.volts as some values may have not been written because out of limits or
        # because values can't be changed on this state
        self.remote_get_configured_voltages()

        return ans

    def remote_set_dac_conf(self):
        """
        Applies configured voltages on self.voltages to GFA

        :return:
        """

        c = CommandPacket(command='pwr.set_dac_conf')

        for i in range(32):
            chan = self._volt_conf.get_by_chan(i)
            # value_to_write = ((chan.int_offset & 0xffff) << 16) | (chan.int_gain & 0xffff)
            c.set_arg(chan.chantag, {'offset': chan.int_offset, 'gain': chan.int_gain})
        # print(c.json)
        ans = self._comm.exec_std_command(c)
        log.debug('set_dac_conf values: {0}'.format(ans.json))

        # Update voltage values on self.volts as some values may have not been written because out of limits or
        # because values can't be changed on this state
        self.remote_get_configured_voltages()

        return ans

    def remote_get_configured_voltages(self):
        """
        Recover configured voltages from GFA and update self.voltages

        :return:
        """

        c = CommandPacket(command='pwr.get_dac_counts')
        ans = self._comm.exec_std_command(c)

        for i in range(32):
            chan = self._volt_conf.get_by_chan(i)
            val = ans.get_ans(chan.chantag)
            chan.dac_counts = val

        log.debug('get_configured_voltages values: {0}'.format(ans.json))
        return ans

    def remote_get_ccd_pins_mask(self):
        """
        Recover od_mask registry

        :return:
        """
        c = CommandPacket(command='pwr.get_ccd_pins_mask')
        ans = self._comm.exec_std_command(c)

        log.debug('get_ccd_pins_mask values: {0}'.format(ans.json))
        return ans

    def remote_set_ccd_pins_mask(self, od_e: bool = True, od_f: bool = True, od_g: bool = True, od_h: bool = True,
                                 dd: bool = True, rd: bool = True, vss: bool = True, of: bool = True,
                                 clocks: bool = True):
        """
        Set od_mask values.

        :param od_e: When set to True, OD pin is enabled
        :param od_f: When set to True, OD pin is enabled
        :param od_g: When set to True, OD pin is enabled
        :param od_h: When set to True, OD pin is enabled

        :return: answer
        """
        c = CommandPacket(command='pwr.set_ccd_pins_mask')
        c.set_arg('od_e', od_e)
        c.set_arg('od_f', od_f)
        c.set_arg('od_g', od_g)
        c.set_arg('od_h', od_h)
        c.set_arg('dd', dd)
        c.set_arg('rd', rd)
        c.set_arg('vss', vss)
        c.set_arg('og', of)
        c.set_arg('clocks', clocks)

        ans = self._comm.exec_std_command(c)

        log.debug('set_ccd_pins_mask values: {0}'.format(ans.json))
        return ans

    def remote_get_enables(self):
        """
        Recover enables status from GFA and update self.enables

        :return: answer
        """

        c = CommandPacket(command='pwr.get_enables_status')
        ans = self._comm.exec_std_command(c)

        self.enables.enables_0 = ans.get_ans('enables_0')
        self.enables.enables_1 = ans.get_ans('enables_1')

        log.debug('get_enables: {0}'.format(ans.json))
        return ans

    def remote_set_phase_timing(self):
        """
        Set phase timings

        :return: answer
        """

        c = CommandPacket(command='pwr.set_power_ud_timing')
        c.set_arg('powerup_ms', self.powerup_timing_ms)
        c.set_arg('powerdown_ms', self.powerdown_timing_ms)

        ans = self._comm.exec_std_command(c)

        log.debug('pwr.set_power_ud_timing values: {0}'.format(ans.json))
        return ans

    def remote_get_phase_timing(self):
        """
        Retrieve current phase timing

        :return: answer
        """

        c = CommandPacket(command='pwr.get_power_ud_timing')

        ans = self._comm.exec_std_command(c)

        self.powerup_timing_ms = ans.get_ans('powerup_ms')
        self.powerdown_timing_ms = ans.get_ans('powerdown_ms')
        log.debug('pwr.get_power_ud_timing values: {0}'.format(ans.json))
        return ans
