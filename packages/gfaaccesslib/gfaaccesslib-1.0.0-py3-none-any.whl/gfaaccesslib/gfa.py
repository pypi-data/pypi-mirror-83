from time import sleep

from gfaaccesslib.comm.communication import CommunicationManager, AsyncManager
from gfaaccesslib.modules.clockmanager import ClockManager
from gfaaccesslib.modules.exposecontroller import ExposeController
from gfaaccesslib.modules.powercontroller import PowerController
from gfaaccesslib.modules.datamanager import DataManager
from gfaaccesslib.modules.irqcontroller import IRQController
from gfaaccesslib.modules.adccontroller import ADCController
from gfaaccesslib.modules.telemetry import Telemetry
from gfaaccesslib.modules.system_info import SystemInfo
from gfaaccesslib.modules.pid import PID

from gfaaccesslib.modules.test import TestModule
from gfaaccesslib.raws.rawdatamanager import RawDataManager
from gfaaccesslib.raws.e2v_ccd230_42 import e2vccd23042
from gfaaccesslib.api_helpers import GFAStatus, GFAStatusType
from gfaaccesslib.modules.heartbeat import HeartBeat

__author__ = 'otger, David Roman'

API_VERSION = "0.6"


class GFA(object):
    """
    Creates an instance of the GFA object

    :param ip: IP number of the remote system
    :param port: Commands port number
    :param async_port: Raws port number
    :param ccd: CCD type
    :param auto_connect_async: If true the GFA constructor will automatically connect to the async port
    :param auto_update: If true hardware data will be acquired at initialization time
    """
    def __init__(self, ip, port=3000, async_port=None, ccd="e2v-ccd230-42", auto_connect_async=True, auto_update=True):
        self._ip = ip
        self._port = port
        self._async_port = async_port
        self._ccd_name = ccd
        self.comm = CommunicationManager(ip=ip, port=port)
        self.raws = RawDataManager()
        self._async_translator = None
        self.async_manager = None
        self.clockmanager = ClockManager(communication_manager=self.comm)
        self.powercontroller = PowerController(communication_manager=self.comm, auto_update=False)
        self.exposecontroller = ExposeController(communication_manager=self.comm, auto_update=False)
        self.adccontroller = ADCController(communication_manager=self.comm)
        self.buffers = DataManager(communication_manager=self.comm)
        self.irq = IRQController(communication_manager=self.comm, auto_update=False)
        self.telemetry = Telemetry(communication_manager=self.comm, auto_update=False)
        self.sys = SystemInfo(communication_manager=self.comm)
        self.pid = PID(communication_manager=self.comm)
        self.tests = TestModule(communication_manager=self.comm)
        self.heartbeat = HeartBeat(communication_manager=self.comm)

        if auto_update:
            self._ensure_compatible_api()
            self.remote_update()
        
        if async_port:
            self.async_manager = AsyncManager(ip=ip, async_port=async_port, auto_connect=auto_connect_async)
            self._setup_async()

        self._status = GFAStatus()

    def connect(self, ip=None, port=None, async_port=None):
        """
        Connects to the GFA system. Before exiting :attr:`~disconnect` must be called.

        :param ip: IP of remote system
        :param port: Command port
        :param async_port: Asyncs port
        """
        if ip and port:
            self.comm.set_parameters(ip, port)

        self._ensure_compatible_api()

        if ip and async_port:
            if not self.async_manager:
                self.async_manager = AsyncManager(ip=ip, async_port=async_port, auto_connect=True)
                self._setup_async()
            self.async_manager.set_parameters(ip, async_port)

        if self.async_manager:
            self.async_manager.connect()

    def disconnect(self):
        """
        Disconnects

        """
        self.close()

    def remote_update(self):
        self.irq.remote_get_status()
        self.exposecontroller.remote_get_status()
        self.powercontroller.remote_update_hw_conf()
        self.telemetry.remote_init_alarms()

    def _ensure_compatible_api(self):
        ans = self.sys.remote_api().answer
        if ans["version"] != API_VERSION:
            print("WARNING: API version mismatch: Server={}, Client={}".format(ans["version"], API_VERSION))
            sleep(5)

    def _setup_async(self):
        if self._ccd_name == "e2v-ccd230-42":
            self._async_translator = e2vccd23042(rawdatamanager=self.raws)
        if self._async_translator:
            self.async_manager.add_row_callback(self._async_translator.process_row)
            self.async_manager.add_new_image_callback(self._async_translator.process_start_exp)

    def close(self):
        """
        .. deprecated:: 0
            Use :func:`disconnect` instead.
        """
        if self.async_manager:
            self.async_manager.close()

    def update_status(self):
        self.exposecontroller.remote_get_status()
        if self.exposecontroller.status.idle_state:
            self._status.state = GFAStatusType.idle
        elif self.exposecontroller.status.configured_state:
            self._status.state = GFAStatusType.configured
        elif self.exposecontroller.status.power_up_state:
            self._status.state = GFAStatusType.power_up
        elif self.exposecontroller.status.power_down_state:
            self._status.state = GFAStatusType.power_down
        elif self.exposecontroller.status.ready_state:
            self._status.state = GFAStatusType.ready
        elif self.exposecontroller.status.error_state:
            self._status.state = GFAStatusType.error
        elif self.exposecontroller.status.exposing_state:
            self._status.state = GFAStatusType.exposing
        elif self.exposecontroller.status.telemetry_state:
            self._status.state = GFAStatusType.telemetry
        self._status.bias_enabled = self.exposecontroller.status.is_powered
        self.clockmanager.remote_get_info()
        self.adccontroller.remote_get_status()
        self._status.horizontal_transfers = self.clockmanager.info.processed_horizontal
        self._status.exposure_id = self.clockmanager.info.exposure_id

    def _get_status(self):
        return self._status

    status = property(_get_status)
