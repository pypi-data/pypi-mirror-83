from gfaaccesslib.comm.command import CommandPacket
from .gfamodule import GFAModule
from .logger import log

__author__ = 'david roman'


class PID(GFAModule):
    def __init__(self, communication_manager):
        super(PID, self).__init__(communication_manager)

    def remote_enable(self):
        c = CommandPacket(command="pid.enable")
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_disable(self):
        c = CommandPacket(command="pid.disable")
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_is_enabled(self):
        c = CommandPacket(command='pid.is_enabled')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_components(self, kp: int, ki: int, kd: int):
        c = CommandPacket(command='pid.set_components')
        c.set_arg('kp', kp)
        c.set_arg('ki', ki)
        c.set_arg('kd', kd)
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_components(self):
        c = CommandPacket(command='pid.get_components')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_setpoint(self, setpoint: int):
        c = CommandPacket(command='pid.set_setpoint')
        c.set_arg("setpoint", setpoint)
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_setpoint(self):
        c = CommandPacket(command='pid.get_setpoint')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_fix_duty_cycle(self, duty: int):
        c = CommandPacket(command="pid.fix_duty_cycle")
        c.set_arg("duty", duty)
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_fixed_duty_cycle(self):
        c = CommandPacket(command="pid.get_fixed_duty_cycle")

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_disable_fixed_duty_cycle(self):
        c = CommandPacket(command="pid.disable_fixed_duty_cycle")
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_enable_fixed_duty_cycle(self):
        c = CommandPacket(command="pid.enable_fixed_duty_cycle")
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_is_duty_cycle_fixed(self):
        c = CommandPacket(command='pid.is_duty_cycle_fixed')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_max_duty_cycle(self, duty_cycle: int):
        c = CommandPacket(command='pid.set_max_duty_cycle')
        c.set_arg("max_duty", duty_cycle)
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_max_duty_cycle(self):
        c = CommandPacket(command='pid.get_max_duty_cycle')
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_set_integral_error_limits(self, max: int, min: int):
        c = CommandPacket(command="pid.set_integral_error_limits")
        c.set_arg("max_error", max)
        c.set_arg("min_error", min)
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_get_integral_error_limits(self):
        c = CommandPacket(command="pid.get_integral_error_limits")
        ans = self._comm.exec_std_command(c)
        return ans

    def remote_update(self, val: int):
        c = CommandPacket(command="pid.update")
        c.set_arg("val", val)

        ans = self._comm.exec_std_command(c)
        return ans
