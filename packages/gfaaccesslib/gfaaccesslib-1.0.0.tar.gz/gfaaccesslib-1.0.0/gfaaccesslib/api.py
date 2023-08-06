#!/usr/bin/env python2.7
from .gfa import GFA
from .api_exceptions import OperationNotPermitted, BadValue
from .api_helpers import GFAStatus, GFAExposureLock
from .logger import log

GFA_LIB_VERSION = '0.1'
GFA_IFACE_VERSION = '0.3'

COMMAND_PORT = 32000
ASYNC_PORT = 32001

'''
API interface for DESI GFA devices

Authors:
    - Otger Ballester: otger@ifae.es

This file will remain as a list of desired features. Real library can be found at gfa.py file
'''


class GFAApi(object):
    def __init__(self, ip, async_subscribe=True, ccd="e2v-ccd230-42"):
        self._ip = ip
        self._acq_lock = GFAExposureLock()
        self._cmd_port = COMMAND_PORT
        self._asyncport = ASYNC_PORT if async_subscribe else None
        self._gfa = GFA(ip=ip, port=self._cmd_port, async_port=self._asyncport, ccd=ccd)
        if async_subscribe:
            self._gfa.async_manager.add_end_image_callback(self._acq_lock.async_callback_release)

    def get_lib_instance(self):
        return self._gfa

    def get_raw_manager(self):
        return self._gfa.raws

    def set_default_values(self):
        """
        Apply default values to voltages, clock timings, ccd geometry

        :return:
        """
        self._gfa.powercontroller.voltages.set_default_values()
        self._gfa.powercontroller.remote_set_voltages()
        self._gfa.clockmanager.time_conf.set_default_values()
        self._gfa.clockmanager.remote_set_clock_timings()
        self._gfa.clockmanager.geom_conf.set_default_values()
        self._gfa.clockmanager.remote_set_ccd_geom()

    def set_voltages_config(self, config=None):
        """
        Loads a configuration to GFA

        Args:
            config (GFAVoltagesConfiguration): Configuration Values
        Returns:
            True
        Raises:
            ValueError: if some value is out of range
            GFATimeOut
            GFAConnectionRefused
        """
        if config:
            self._gfa.powercontroller.voltages.update(config)
        self._gfa.powercontroller.remote_set_voltages()

    def get_voltages_config(self):
        """Returns current configuration set on GFA device

        Returns:
            config (GFAVoltagesConfiguration): Current configuration values set at GFA device. Configuration, not real values.
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.powercontroller.remote_get_configured_voltages()
        return self._gfa.powercontroller.voltages

    def bias_powerup(self):
        """The GFA device will have a hardcoded default values obtained from system characterization. If DESI plans to
        set a tailored configuration for each GFA, upper layers must deal with values to be set up using set_config

        Once powerup_bias_voltage is launched the GFA will check if it can be done and start the sequence to power up.

        Returns:
            True or raise an exception
        Raises:
            OperationNotPermitted: This operation can not be initiated on current GFA status
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.exposecontroller.remote_get_status()
        if self._gfa.exposecontroller.status.idle_state:
            raise OperationNotPermitted("GFA must be configured to power up")

        if not self._gfa.exposecontroller.status.configured_state:
            raise OperationNotPermitted("GFA must be in 'configured' state to power up")
        self._gfa.exposecontroller.remote_power_up()

    def bias_powerdown(self):
        """If bias are powered and GFA can power down Bias voltages, it will power it down
        GFA will follow the sequence required to power down bias once it has checked status allows to power down bias

        Returns:
            True or raise an Exception
        Raises:
            DACCommError: Error communicating with DAC on GFA
            OperationNotPermitted: This operation can not be initiated on current GFA status
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.exposecontroller.remote_get_status()
        if not self._gfa.exposecontroller.status.is_powered:
            raise OperationNotPermitted("GFA must be powered to power down")

        self._gfa.exposecontroller.remote_power_down()

    def set_clocks_timings(self, gfa_time_conf=None):
        """Sets actual readout times configuration. This values should be hardcoded on GFA device

        Args:
            config (GFATimeConfiguration): Settings for all times involved in reading the CCD
        Returns:
            True
        Raises:
            BadValue
            GFATimeOut
            GFAConnectionRefused
        """
        log.info('Setting clocks timings: {0}'.format(gfa_time_conf))
        if gfa_time_conf is not None:
            if not gfa_time_conf.check():
                raise BadValue("Some time value is invalid")
        ans = self._gfa.clockmanager.remote_set_clock_timings(gfa_time_conf)
        return ans

    def get_clocks_timings(self):
        """Gets actual readout times configuration

        Args:
        Returns:
            config (GFATimeConfiguration): Settings for all times involved in reading the CCD
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.clockmanager.remote_get_clock_timings()
        return self._gfa.clockmanager.time_conf

    def get_status(self):
        """Returns current status of the GFA and exposure progress if it is the case

        Returns:
            status (GFAStatus): current status of the GFA
        """
        self._gfa.update_status()
        return self._gfa.status

    def get_telemetry(self, name=None):
        """Returns current telemetry values

        Args:
            name (string): If set, it returns only requested value. if not set, it returns all values
        Returns:
            telemetry (GFATelemetry): All values when name is not set
            value (float): When name is set
        Raises:
            GFATimeOut
            GFAConnectionRefused
            UnknownValue: name was set to an unknown value

        """
        pass

    def get_exposure_stack(self):
        """

        Returns:
            stack (GFAExposureStack): Stack set on GFA device

        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.clockmanager.remote_get_stack_contents()
        return self._gfa.clockmanager.stack

    def set_exposure_stack(self, stack):
        """

        Returns:
            stack (GFAExposureStack): Stack set on GFA device

        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.clockmanager.remote_set_stack_contents(stack)
        return self._gfa.clockmanager.stack

    def set_ccd_geometry(self, geom):
        """Used to change ccd geometry. Default values are already hard coded on GFA

        Args:
            geom (GFACCDGeom)
        Returns:
            True
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.clockmanager.remote_set_ccd_geom(geom)

    def get_ccd_geometry(self):
        """Get current CCD geometry values set on GFA device

        Returns:
            geom (GFACCDGeom)
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        self._gfa.clockmanager.remote_get_ccd_geom()
        return self._gfa.clockmanager.geom_conf

    def set_telemetry_configuration(self, telem_config):
        """Used to change GFAs telemetry configuration

        Args:
            telem_config (GFATelemetryConfig)
        Returns:
            True
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """

    def get_telemetry_configuration(self):
        """Get current CCD Telemetry configuration

        Returns:
            telem_config (GFATelemetryConfig)
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """

    # def set_interlock_configuration(self, lock_config):
    #     """Used to change GFAs interlocks configuration
    #
    #     Args:
    #         lock_config (GFAInterlocksConfig)
    #     Returns:
    #         True
    #     Raises:
    #         GFATimeOut
    #         GFAConnectionRefused
    #     """
    #
    # def get_interlock_configuration(self):
    #     """Get current GFA interlock configuration
    #
    #     Returns:
    #         lock_config (GFAInterlocksConfig)
    #     Raises:
    #         GFATimeOut
    #         GFAConnectionRefused
    #     """

    def expose(self, blocking=True):
        """Generate an exposure following current Exposure configuration

        Args:
            blocking: command will wait until exposure has finished. Usable only when GFA configured to receive
                async packages
        Returns:
            RAW Data if blocking set to True (ToDo define how are they implemented (Numpy Array maybe))
            Object to be able to join thread and recover real return if blocking set to False
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        if self._asyncport:
            if self._acq_lock.is_locked:
                raise OperationNotPermitted('GFA is already locked in an exposure')
            self._acq_lock.acquire()
        retval = self._gfa.exposecontroller.remote_start_stack_exec()
        if self._asyncport and blocking:
            self._acq_lock.acquire()
            # will wait here until async releases. then we have to release our second acquire
            self._acq_lock.release()
        return retval

    def clear_ccd(self, half=False, blocking=True):
        """Clears the CCD
        Args:
            half: dump only storage area
            blocking: set to True if we want to wait for command to end
        Returns:
            True if blocking set to True
            Object to be able to join thread and get real return if blocking set to False
        Raises:
            GFATimeOut
            GFAConnectionRefused
        """
        # We have to create a stack contents to dump the CCD
        if half:
            rows_2_dump = self._gfa.clockmanager.geom_conf.storage_rows
        else:
            rows_2_dump = self._gfa.clockmanager.geom_conf.storage_rows + \
                            self._gfa.clockmanager.geom_conf.storage_rows
        g = self._gfa.clockmanager.stack
        g.clear()
        g.add_dump_rows_cmd(rows_2_dump)
        self._gfa.clockmanager.remote_set_stack_contents()
        self.expose(blocking)

    def store_charge(self):
        """Exercise clocks to store data from image section to storage section"""

        # We have to create a stack contents to dump the CCD
        g = self._gfa.clockmanager.stack
        g.clear()
        g.add_dump_rows_cmd(self._gfa.clockmanager.geom_conf.storage_rows)
        self._gfa.clockmanager.remote_set_stack_contents()
        self._gfa.exposecontroller.remote_start_stack_exec()

    def set_expose_callback(self, callback, args=[], kwargs={}):
        """
        Set a callback to be executed once expose finishes

        :param callback: callable
        :param args: list of arguments
        :param kwargs: keyworded arguments
        :return:
        """
        # This will register a callback at self._gfa.async

    def close(self):
        """
        Close sockets and join threads

        :return:
        """
        self._gfa.close()
