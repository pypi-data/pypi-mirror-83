from gfaaccesslib.comm.command import CommandPacket
from .gfamodule import GFAModule
import numpy as np
import base64

__author__ = 'otger'


class MetaInfo(GFAModule):

    def __init__(self, page):
        self.data_page_number = page['data_page_number']
        self.data_buffer_number = page['data_buffer_number']
        self.pixel_length = page['pixel_length']
        self.byte_length = page['byte_length']
        self.data_length = page['data_length']
        self.number_of_pages_per_this_line = page['number_of_pages_per_this_line']
        self.amplificator_config = page['amplificator_config']
        self.amplificator_number = page['amplificator_number']
        self.current_line = page['current_line']
        self.current_image = page['current_image']
        self.line_image_id = page['line_image_id']


class MemoryData(GFAModule):
    def __init__(self, page):
        self._data = page['page_data']

    def as_base64(self):
        return self._data

    def as_np(self):
        return np.fromstring(self.as_string(), dtype=np.int32)

    def as_string(self):
        return base64.b64decode(self._data)


class MemoryDumpPage(GFAModule):
    def __init__(self, page):
        self.page = page
        self.metainfo = MetaInfo(page)
        self.data = MemoryData(page)


class MemoryDump(GFAModule):
    def __init__(self):
        self._page_list = []

    def rem_page(self, index):
        return self._page_list.pop(index)

    def add_page(self, page):
        self._page_list.append(MemoryDumpPage(page))

    def get_page(self, index):
        return self._page_list[index]

    def get_list(self):
        return self._page_list

    def clear(self):
        for i in self._page_list:
            self._page_list.remove(i)

    def __getitem__(self, index):
        return self._page_list[index]

    def __len__(self):
        return len(self._page_list)


class MemoryDumpManager(GFAModule):
    def __init__(self):
        self._mem_dump = []

    def new_dump(self):
        self._mem_dump.append(MemoryDump())
        return self._mem_dump[-1]

    def rem_dump(self, index):
        return self._mem_dump.pop(index)

    def get_dump(self, index):
        return self._mem_dump[index]

    def get_list(self):
        return self._mem_dump

    def clear(self):
        for i in self._mem_dump:
            self._page_list.remove(i)
    
    def __getitem__(self,index):
        return self._mem_dump[index]

    def __len__(self):
        return len(self._mem_dump)

    def __setitem__(self, index, page):
        self._mem_dump[index].add_page(page)


