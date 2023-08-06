#!/usr/bin/python
# -*- coding: utf-8 -*-
from gfaaccesslib.comm.command import CommandPacket
from gfaaccesslib.api_helpers import GFATimeConfiguration
from .gfamodule import GFAModule
from .logger import log

__author__ = 'otger'


class TestModule(GFAModule):
    def __init__(self, communication_manager):
        super(TestModule, self).__init__(communication_manager)

    def echo(self, message: str):

        c = CommandPacket(command='echo', module='tests')
        c.set_arg('message', message)

        ans = self._comm.exec_std_command(c)
        return ans

    def wait(self, millisecs: int):

        c = CommandPacket(command='waitforms', module='tests')
        c.set_arg('millisecs', millisecs)

        ans = self._comm.exec_std_command(c)
        return ans

