from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFAExposeControllerStatus
from .gfamodule import GFAModule
from .logger import log

__author__ = 'otger'


class ExposeController(GFAModule):
    def __init__(self, communication_manager, auto_update):
        super(ExposeController, self).__init__(communication_manager)

        self._status = GFAExposeControllerStatus()

        if auto_update:
            self.remote_get_status()

    def _get_status(self):
        return self._status

    status = property(_get_status)

    def _operate(self, expose=None, get_telem=None,
                 power_up=None, power_down=None, clear_error=None):
        c = CommandPacket(command='expctrl.operation')
        if expose:
            c.set_arg("expose", True)
        elif get_telem:
            c.set_arg("get_telem", True)
        elif power_up:
            c.set_arg("power_up", True)
        elif power_down:
            c.set_arg("power_down", True)
        elif clear_error:
            c.set_arg("clear_error", True)

        ans = self._comm.exec_std_command(c)
        log.debug('exposure controller operation answer: {0}'.format(ans.json))
        return ans

    def remote_start_stack_exec(self):
        return self._operate(expose=True)

    def remote_get_telemetry(self):
        return self._operate(get_telem=True)

    def remote_power_up(self):
        return self._operate(power_up=True)

    def remote_power_down(self):
        return self._operate(power_down=True)

    def remote_clear_error_state(self):
        return self._operate(clear_error=True)

    def remote_get_status(self):
        c = CommandPacket(command='expctrl.get_status')
        ans = self._comm.exec_std_command(c)
        self.status.status_word = ans.get_ans('status')
        log.debug('exposure controller operation answer: {0}'.format(ans.json))
        return ans

    def remote_cancel_stack_powerdown_ccd(self):
        """
        Ask the power controller to cancel any execution of the stack and powerdown the bias of the CCD
        This is a software routine executed at the gfa server not at VHDL level. The gfaserver asks to cancel the stack
        execution to the clock manager, waits a couple of seconds and then asks the expose controller to shutdown the
        bias
        """
        c = CommandPacket(command='expctrl.cancel_and_shutdown_bias')

        ans = self._comm.exec_std_command(c)
        log.debug('expctrl.cancel_and_shutdown_bias values: {0}'.format(ans.json))
        return ans
