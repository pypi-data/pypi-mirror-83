from gfaaccesslib.comm.command import CommandPacket
from .gfamodule import GFAModule
from .logger import log
from gfaaccesslib.api_helpers import GFATelemetryVoltages

__author__ = 'david roman'


class Telemetry(GFAModule):
    def __init__(self, communication_manager, auto_update=True):
        super(Telemetry, self).__init__(communication_manager)
        # FIXME: ccd_voltages currently will have both, sensors and voltages
        self.ccd_voltages = GFATelemetryVoltages()

        if auto_update:
            self.remote_init_alarms()

    def remote_get_status(self):
        c = CommandPacket(command='telemetry.get_status')

        ans = self._comm.exec_std_command(c)
        #self.ccd_voltages.powerdown = True if int(ans.answer['status']) & 1 == '1' else False
        return ans

    def remote_get_voltage_values(self):
        c = CommandPacket(command='telemetry.get_voltage_values')

        ans = self._comm.exec_std_command(c)
        self.ccd_voltages.update(ans.answer)
        return ans

    def remote_get_xadc_voltages(self):
        c = CommandPacket(command='telemetry.get_xadc_voltages')

        ans = self._comm.exec_std_command(c)
        #self.ccd_voltages.update(ans.answer)
        return ans

    def remote_get_sensor_values(self):
        c = CommandPacket(command='telemetry.get_sensor_values')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_xadc_meta(self):
        c = CommandPacket(command='telemetry.get_xadc_meta')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_xadc_temp(self):
        c = CommandPacket(command='telemetry.get_xadc_temp')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_configure_sensors_autoupdate(self, period: int):
        """
        Set period to 0 to disable autoupdate

        :param period: seconds
        :return:
        """
        c = CommandPacket(command='telemetry.configure_sensors_autoupdate')
        c.set_arg('period', period)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_configured_autoupdate(self):
        c = CommandPacket(command='telemetry.get_configured_autoupdate')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_force_sensors_read(self):
        c = CommandPacket(command='telemetry.force_sensors_read')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_i2ccontrol_write(self, cmd: int, address: int, bus: int):
        c = CommandPacket(command='telemetry.i2ccontrol_write')
        c.set_arg('cmd', cmd)
        c.set_arg('address', address)
        c.set_arg('bus_selector', bus)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_i2ccontrol_read(self, bytes: int, address: int, bus: int):
        c = CommandPacket(command='telemetry.i2ccontrol_read')
        c.set_arg('bytes_to_read', bytes)
        c.set_arg('address', address)
        c.set_arg('bus_selector', bus)

        ans = self._comm.exec_std_command(c)
        self.ccd_voltages.update(ans.answer)
        return ans

    def remote_get_voltage_telem_settings(self):
        c = CommandPacket(command='telemetry.get_voltage_telem_settings')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_voltage_telem_settings(self, udelay: int, reference_enabled: int):
        c = CommandPacket(command='telemetry.set_voltage_telem_settings')
        c.set_arg('delay_us', udelay)
        c.set_arg('reference_enabled', reference_enabled)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_voltage_telem_spi_settings(self):
        c = CommandPacket(command='telemetry.get_voltage_telem_spi_settings')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_voltage_telem_spi_settings(self, sclk_period: int, spi_access: int):
        c = CommandPacket(command='telemetry.set_voltage_telem_spi_settings')
        c.set_arg('half_sclk_period', sclk_period)
        c.set_arg('before_spi_access', spi_access)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_init_alarms(self):
        """
        Initialize alarms with a predefined configuration (defined on gfaserver).

        :return: answer
        """
        c = CommandPacket(command='telemetry.init_alarms')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_alarm_thresholds(self, fpga: int , hotpeltier: int, coldpeltier: int, ambient: int, filter_alarm: int,
                                hold_ms: int = 2000, interlock_delay_ms: int = 10000):

        """
        configure alarms

        :param fpga: temperature threshold
        :param hotpeltier: temperature threshold
        :param coldpeltier: temperature threshold
        :param ambient: temperature threshold
        :param filter_alarm: temperature threshold
        :param hold_ms: for how many milliseconds the temperature have to be above the threshold raise an alarm
        :param interlock_delay_ms: how many milliseconds we have to wait before the interlock
        :return:
        """
        c = CommandPacket(command='telemetry.configure_alarms')
        c.set_arg('fpga', fpga)
        c.set_arg('hotpeltier', hotpeltier)
        c.set_arg('coldpeltier', coldpeltier)
        c.set_arg('ambient', ambient)
        c.set_arg('filter', filter_alarm)
        c.set_arg('hold_ms', hold_ms)
        c.set_arg('interlock_delay_ms', interlock_delay_ms)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_alarm_thresholds(self):
        """
        Retrieve alarms threshold

        :return: answer
        """
        c = CommandPacket(command='telemetry.get_configured_alarms')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_enable_alarms(self, fpga: bool = False, hotpeltier: bool = False,
                             coldpeltier: bool = False, ambient: bool = False, filter_alarm: bool = False):
        """
        Configure given alarms

        :param fpga: alarm
        :param hotpeltier: alarm
        :param coldpeltier: alarm
        :param ambient: alarm
        :param filter_alarm: alarm
        :return: answer
        """

        c = CommandPacket(command='telemetry.enable_alarms')
        c.set_arg('fpga', fpga)
        c.set_arg('hotpeltier', hotpeltier)
        c.set_arg('coldpeltier', coldpeltier)
        c.set_arg('ambient', ambient)
        c.set_arg('filter', filter_alarm)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_enabled_alarms(self):
        """
        Retrieve configured alarms

        :return: answer
        """
        c = CommandPacket(command='telemetry.get_enabled_alarms')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_triggered_alarms(self):
        """
        Retrieve alarms status (ie: if have been raised or not).

        :return: answer
        """
        c = CommandPacket(command='telemetry.get_triggered_alarms')

        ans = self._comm.exec_std_command(c)
        return ans

    # Force pwm value, for debugging
    def remote_set_pwm(self, percentage: int):
        """
        Change pwm setting

        :param percentage: Percentage
        :return: answer
        """
        c = CommandPacket(command='telemetry.set_pwm')
        c.set_arg('percentage', percentage)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_pwm(self):
        """
        Retrieve current pwm configuration

        :return: answer
        """
        c = CommandPacket(command='telemetry.get_pwm')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_force_pwm_raw(self, high_clocks: int, low_clocks: int):
        """
        Command to manually configure the pwm system.

        :param high_clocks: Value to be written to the high_clocks register
        :param low_clocks: Value to be written to the low_clocks register
        :return: answer
        """

        c = CommandPacket(command='telemetry.force_pwm_values')
        c.set_arg('high_clocks', high_clocks)
        c.set_arg('low_clocks', low_clocks)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_force_pwm(self, duty_100: int, freq_hz: int):
        """
        Command to manually configure the pwm system.

        :param duty_100: duty cycle
        :param freq_hz: frequency
        :return: answer
        """

        if freq_hz == 0:
            high = 0
            low = 0
        else:
            high = int((duty_100 / freq_hz) * 10000000)
            low = int(((100 - duty_100) / freq_hz) * 10000000)

        return self.remote_force_pwm_raw(high_clocks=high, low_clocks=low)

    def remote_get_pwm_registers(self):
        """
        Retrieve raw pwm registers

        :return: answer
        """

        c = CommandPacket(command='telemetry.get_pwm_registers')
        ans = self._comm.exec_std_command(c)
        return ans

    # To acquire new values of ccd voltage, use exposecontroller.get_telemetry()
