from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFADataManagerStatus
from .gfamodule import GFAModule
from gfaaccesslib.modules.memorydump import MemoryDumpManager
from .logger import log

__author__ = 'otger'


class DataManager(GFAModule):
    def __init__(self, communication_manager):
        super(DataManager, self).__init__(communication_manager)

        self.status = GFADataManagerStatus()
        self.mem_dump_manager = MemoryDumpManager()
        self._last_answer = None

    def _get_last_answer(self):
        return self._last_answer

    last_answer = property(_get_last_answer)

    def _set_adc_delay(self, clock_steps: int):
        c = CommandPacket(command='dataman.set_adc_delay')

        c.set_arg('clock_steps', clock_steps)

        self._last_answer = self._comm.exec_std_command(c)

    def _get_adc_delay(self):
        c = CommandPacket(command='dataman.get_adc_delay')

        ans = self._comm.exec_std_command(c)
        self._last_answer = ans
        return ans.get_ans('clock_steps')

    adc_delay = property(_get_adc_delay, _set_adc_delay)

    def remote_set_data_provider(self, provider: int, mode: int):
        # provider: 0 = real, 1 = fake
        # real modes:
        # 0: pixel value = average reference - average signal
        # 1: pixel value = average reference (16 MSB) & average signal (16 LSB)
        # 2: pixel value = number of signal phase samples (8MSB) & signal sum (24 LSB)
        # 3: pixel value = number of reference phase samples (8MSB) & reference sum (24 LSB)
        # 4: each value: bits 18,17,16 -> acq lines (debug, reference, signal) & 16LSB adc sample
        # fake_mode
        # 0: output zeros
        # 1: output ones
        # 2: e: 0, f: 1000, g: 2000, h: 3000
        # 3: e: row + col, f: row + col +1000, g: row + col +2000, h: row + col +3000
        # 4: pixel value = row
        # 5: pixel value = column
        # 6: pixel value = row x col

        c = CommandPacket(command='dataman.set_data_provider')

        c.set_arg('provider', provider)
        c.set_arg('mode', mode)

        ans = self._comm.exec_std_command(c)
        self.status.mode = ans.get_ans('mode')
        self.status.provider = ans.get_ans('provider')
        return ans

    def remote_get_data_mode(self):
        c = CommandPacket(command='dataman.get_data_provider')

        ans = self._comm.exec_std_command(c)
        self.status.mode = ans.get_ans('mode')
        self.status.provider = ans.get_ans('provider')
        return ans

    def remote_get_buffers_status(self):
        c = CommandPacket(command='dataman.get_buffers_status')

        ans = self._comm.exec_std_command(c)
        self.status.stream_status_word = ans.get_ans('stream_status')
        for b in self.status.buffers:
            b.status_word = ans.get_ans('pixbufstatus')
            b.contents = ans.get_ans('pix_buf_length_{0}'.format(b.buffer_names[b.buffer_index]))
            b.enabled_word = ans.get_ans('line_amplifiers_enabled')
        self.status.pending_lines = ans.get_ans('pending_lines')
        return ans

    def remote_get_memory_dump(self, buffer_number: int, pages: int):
        if pages < 1:
            log.warn("Minimum value that makes sense for \"pages\" is 1")

        c = CommandPacket(command='dataman.get_memory_dump')
        c.set_arg('buffer_number', buffer_number)
        c.set_arg('pages', pages)
        ans = self._comm.exec_std_command(c)
        dump = self.mem_dump_manager.new_dump()

        page_array = ans.get_ans('page_array')
        if page_array:
            for i in page_array:
                dump.add_page(i)

        return ans

    def remote_clear_buffers(self):
        c = CommandPacket(command='dataman.clear_buffers')

        ans = self._comm.exec_std_command(c)
        self.status.stream_status_word = ans.get_ans('stream_status')
        for b in self.status.buffers:
            b.status_word = ans.get_ans('pixbufstatus')
            b.contents = ans.get_ans('pix_buf_length_{0}'.format(b.buffer_names[b.buffer_index]))
            b.enabled_word = ans.get_ans('line_amplifiers_enabled')
        self.status.pending_lines = ans.get_ans('pending_lines')
        return ans
