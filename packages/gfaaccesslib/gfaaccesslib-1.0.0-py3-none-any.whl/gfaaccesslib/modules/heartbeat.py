#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gfaaccesslib.comm.command import CommandPacket
from .gfamodule import GFAModule
from gfaaccesslib.api_helpers import HeartBeatStatus
from .logger import log

__author__ = "Otger Ballester"
__copyright__ = "Copyright 2020"
__credits__ = ["Otger Ballester"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Otger Ballester"
__email__ = "otger@ifae.es"
__status__ = "Production"


class HeartBeat(GFAModule):
    def __init__(self, communication_manager):
        super().__init__(communication_manager)
        self.status = HeartBeatStatus()

    def remote_set_config(self, address: str, interval: int = 30, retries: int = 3):
        """
        Configure the heartbeat functionality at gfaserver
        :param address: IP or address of the server to ping
        :param interval: Interval of ping tests in seconds
        :param retries: Consecutive number of fails on the ping to cancel stack execution and shutdown bias
        :return:
        """
        c = CommandPacket(command='heartbeat.configure')
        c.set_arg('address', str(address))
        c.set_arg('interval', str(interval))
        c.set_arg('retries', str(retries))

        ans = self._comm.exec_std_command(c)
        self.status.address = address
        self.status.interval = interval
        self.status.retries = retries
        log.debug('heartbeat.configure answer: {0}'.format(ans.json))
        return ans

    def remote_get_config(self):
        c = CommandPacket(command='heartbeat.get_config')

        ans = self._comm.exec_std_command(c)
        self.status.address = ans.json['answer']['address']
        self.status.interval = int(ans.json['answer']['interval'])
        self.status.retries = int(ans.json['answer']['retries'])
        log.debug('heartbeat.get_config answer: {0}'.format(ans.json))
        return ans

    def remote_get_status(self):
        c = CommandPacket(command='heartbeat.status')

        ans = self._comm.exec_std_command(c)
        self.status.enabled = bool(int(ans.json['answer']['running']))
        self.status.errors = int(ans.json['answer']['errors'])
        self.status.last_ping_ts = float(ans.json['answer']['last_ping_ts'])
        self.status.last_ping_error_ts = float(ans.json['answer']['last_error_ts'])

        log.debug('heartbeat.status answer: {0}'.format(ans.json))
        return ans

    def remote_enable_heartbeat(self):
        c = CommandPacket(command='heartbeat.start')

        ans = self._comm.exec_std_command(c)
        self.status.enabled = True
        log.debug('heartbeat.start answer: {0}'.format(ans.json))
        return ans

    def remote_disable_heartbeat(self):
        c = CommandPacket(command='heartbeat.stop')

        ans = self._comm.exec_std_command(c)
        self.status.enabled = False
        log.debug('heartbeat.stop answer: {0}'.format(ans.json))
        return ans

    def remote_update(self):
        self.remote_get_status()
        self.remote_get_config()
