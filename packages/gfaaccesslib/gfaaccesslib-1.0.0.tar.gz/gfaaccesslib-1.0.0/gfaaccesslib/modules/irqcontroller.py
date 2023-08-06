from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFAIRQControllerStatus
from .gfamodule import GFAModule
from .logger import log

__author__ = 'otger'


class IRQController(GFAModule):
    def __init__(self, communication_manager, auto_update):
        super(IRQController, self).__init__(communication_manager)

        self._status = GFAIRQControllerStatus()

        if auto_update:
            self.remote_get_status()

    def _get_status(self):
        return self._status
    status = property(_get_status)

    def remote_get_status(self):
        c = CommandPacket(command='irqctrl.get_status')
        ans = self._comm.exec_std_command(c)
        self._status.status_bits = ans.get_ans('status_bits')
        self._status.received_img_start = ans.get_ans('received_img_start')
        self._status.received_line = ans.get_ans('received_line')
        self._status.received_ccd_done = ans.get_ans('received_ccd_done')
        self._status.received_telemetry = ans.get_ans('received_telemetry')

        self._status.processed_img_start = ans.get_ans('processed_img_start')
        self._status.processed_line = ans.get_ans('processed_line')
        self._status.processed_ccd_done = ans.get_ans('processed_ccd_done')
        self._status.processed_telemetry = ans.get_ans('processed_telemetry')

        self._status.clear_us_img_start = ans.get_ans('clear_us_img_start')
        self._status.clear_us_line = ans.get_ans('clear_us_line')
        self._status.clear_us_ccd_done = ans.get_ans('clear_us_ccd_done')
        self._status.clear_us_telemetry = ans.get_ans('clear_us_telemetry')

        # log.debug('exposure controller operation answer: {0}'.format(ans.json))
        return ans

