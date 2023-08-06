from gfaaccesslib.comm.command import CommandPacket
from .gfamodule import GFAModule

__author__ = 'david roman'


class SystemInfo(GFAModule):
    def __init__(self, communication_manager):
        super(SystemInfo, self).__init__(communication_manager)

    def remote_api(self):
        """
        Retrieves the API version of the remote system:w

        :return: Answer
        """
        c = CommandPacket(command='sysinfo.api')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_version(self):
        """
        Retrieves firmware, module and server version strings

        :return: Answer
        """
        c = CommandPacket(command='sysinfo.version')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_mac(self):
        """
        Retrieve remote MAC

        :return: Answer
        """
        c = CommandPacket(command='sysinfo.mac')

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_read_addr(self, base: int, reg: int):
        c = CommandPacket(command='sysinfo.read_addr')

        c.set_arg('base', base)
        c.set_arg('reg', reg)

        ans = self._comm.exec_std_command(c)
        return ans

    def remote_write_addr(self, base: int, reg: int, value: int):
        c = CommandPacket(command='sysinfo.write_addr')

        c.set_arg('base', base)
        c.set_arg('reg', reg)
        c.set_arg('value', value)

        ans = self._comm.exec_std_command(c)
        return ans
