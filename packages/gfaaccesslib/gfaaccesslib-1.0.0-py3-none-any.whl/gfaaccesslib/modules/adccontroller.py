from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFAAdcControllerStatus, GFAAdcInterfaceValues
from .gfamodule import GFAModule
from .logger import log

__author__ = 'otger'


class ADCController(GFAModule):
    def __init__(self, communication_manager):
        super(ADCController, self).__init__(communication_manager)
        self.status = GFAAdcControllerStatus()
        self.hw_if = GFAAdcInterfaceValues()

    def spi_write(self, address: int, value: int):
        c = CommandPacket(command='adcctrl.write_spi')
        c.set_arg("address", address)
        c.set_arg("value", value)
        ans = self._comm.exec_std_command(c)
        log.debug('adc controller spi written value: {0}'.format(ans.get_ans('written_value')))
        return ans

    def write_conf_register(self, value: int):
        c = CommandPacket(command='adcctrl.set_conf')
        c.set_arg("conf_value", value)
        ans = self._comm.exec_std_command(c)
        log.debug('adc controller spi written value: {0}'.format(ans.get_ans('written_value')))
        return ans

    def _send_status_bits_command(self, argument: str, value: bool):
        c = CommandPacket(command='adcctrl.set_status_bits')
        c.set_arg(argument, value)
        ans = self._comm.exec_std_command(c)
        self.status.status_word = ans.get_ans('status')
        log.debug('adc controller get status: {0}'.format(ans.json))
        return ans

    def adc_start_acq(self):
        """Long ago it was needed to power up the adc to start reading but it was generating problems so, now the ADC
        is perpetually reading values. This command does nothing"""
        return self._send_status_bits_command("read_start", True)

    def adc_stop_acq(self):
        """"Long ago it was needed to power up the adc to start reading but it was generating problems so, now the ADC
        is perpetually reading values. This command does nothing
        """
        return self._send_status_bits_command("read_stop", True)

    def adc_init_calib(self):
        return self._send_status_bits_command("set_init_calib", True)

    def adc_calib_align_frame(self):
        return self._send_status_bits_command("start_align_frame", True)

    def adc_calib_align_data(self):
        return self._send_status_bits_command("start_align_data", True)

    def adc_calib_bitslip(self):
        return self._send_status_bits_command("start_bitslip", True)

    def adc_stop_calib(self):
        return self._send_status_bits_command("stop_calib", True)

    def set_adc_reset_pin(self, value: int):
        return self._send_status_bits_command("reset_adc", bool(value))

    def set_adc_powerdown_pin(self, value: int):
        return self._send_status_bits_command("powerdown_adc", bool(value))

    def reset_adc_controller(self):
        return self._send_status_bits_command("reset_adc_controller", True)

    def cos_generator_output(self, enable: int):
        return self._send_status_bits_command("select_cos_gen", bool(enable))

    def remote_get_status(self):
        c = CommandPacket(command='adcctrl.get_status')
        ans = self._comm.exec_std_command(c)
        self.status.status_word = ans.get_ans('status')
        # print "status word: {0}".format(hex(self.status.status_word))
        self.status.init_status.init_state_value = ans.get_ans('init_state')
        # print "calib state: {0}".format(self.status.init_status.init_state_value)
        # print "status word: {0}".format(hex(self.status.status_word))
        self.status.init_status.init_status_line_word = ans.get_ans('init_status_bits')
        # print "status word: {0}".format(hex(self.status.status_word))
        # print "calib status word: {0}".format(hex(self.status.init_status.init_status_line_word))
        log.debug('adc controller get status: {0}'.format(ans.json))
        return ans

    def remote_get_init_rx_data(self):
        c = CommandPacket(command='adcctrl.get_rx_data')
        ans = self._comm.exec_std_command(c)
        for ix, k in enumerate(["rx_chan_0", "rx_chan_1", "rx_chan_2", "rx_chan_3"]):
            self.status.init_status.rx_data[ix] = ans.get_ans(k)
        log.debug('adc controller get init rx data: {0}'.format(ans.json))
        return ans

    def remote_get_init_rx_expected_pattern(self):
        c = CommandPacket(command='adcctrl.get_expected_pattern')
        ans = self._comm.exec_std_command(c)
        self.status.init_status.rx_expected_pattern = ans.get_ans("expected_rx_data_pattern")
        log.debug('adc controller get init rx expected pattern: {0}'.format(ans.json))
        return ans

    def remote_set_init_rx_expected_pattern(self, pattern: int):
        c = CommandPacket(command='adcctrl.set_expected_pattern')
        c.set_arg("rx_datapattern", pattern)
        ans = self._comm.exec_std_command(c)
        self.status.init_status.rx_expected_pattern = ans.get_ans("written_value")
        log.debug('adc controller set init rx data: {0}'.format(ans.json))
        return ans

    def remote_enable_drivers(self):
        c = CommandPacket(command="adcctrl.enable_drivers")
        ans = self._comm.exec_std_command(c)
        log.debug("Drivers enabled: {}".format(ans.json))

        return ans

    def remote_disable_drivers(self):
        c = CommandPacket(command="adcctrl.disable_drivers")
        ans = self._comm.exec_std_command(c)
        log.debug("Drivers disabled: {}".format(ans.json))

        return ans

    def remote_get_if_delays(self):
        c = CommandPacket(command="adcctrl.get_delays")
        ans = self._comm.exec_std_command(c)
        self.hw_if.delays_0 = ans.get_ans('delays_0') or 0
        self.hw_if.delays_1 = ans.get_ans('delays_1') or 0
        self.hw_if.delays_2 = ans.get_ans('delays_2') or 0
        log.debug("ADC Interface delays: {}".format(ans.json))

        return ans

    def remote_get_if_bitslips(self):
        c = CommandPacket(command="adcctrl.get_bitslips")
        ans = self._comm.exec_std_command(c)
        self.hw_if.bitslip_0 = ans.get_ans('bitslips_0') or 0
        self.hw_if.bitslip_1 = ans.get_ans('bitslips_1') or 0
        self.hw_if.bitslip_2 = ans.get_ans('bitslips_2') or 0
        log.debug("ADC Interface bitslips: {}".format(ans.json))
        return ans
