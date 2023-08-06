import logging
from abc import ABC

import psutil
from pysnmp.error import PySnmpError
from pysnmp.hlapi import asyncio as pysnmp_asyncio
from pysnmp.hlapi.asyncio import (
    CommunityData,
    SnmpEngine,
    ContextData,
    UdpTransportTarget,
    ObjectType,
    ObjectIdentity,
)

from prtg_pyprobe.sensors.helpers import SensorDefinitionGroup


class SensorBase(ABC):
    def __getitem__(self, kind):
        return self.kind

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def kind(self) -> str:
        raise NotImplementedError

    @property
    def definition(self) -> dict:
        raise NotImplementedError

    async def work(self, *args, **kwargs) -> None:
        raise NotImplementedError


class SensorPSUtilBase(SensorBase, ABC):
    @property
    def temperature_settings_group(self):
        probe_health_def_group_temperature = SensorDefinitionGroup(name="temperature", caption="Temperature Settings")
        probe_health_def_group_temperature.add_field(
            field_type="radio",
            name="celfar",
            caption="Choose between Celsius or Fahrenheit display",
            help="Choose wether you want to return the value in Celsius or Fahrenheit",
            options={"1": "Celsius", "2": "Fahrenheit"},
            default="1",
        )
        return probe_health_def_group_temperature

    @property
    def diskspace_settings_group(self):
        probe_health_def_group_diskspace = SensorDefinitionGroup(name="diskspace", caption="Disk Space Settings")
        probe_health_def_group_diskspace.add_field(
            field_type="radio",
            name="diskfull",
            caption="Full Display of all disk space values",
            help="Choose wether you want to get all disk space data or only percentages.",
            options={"1": "Percentages", "2": "Full Information"},
            default="1",
        )
        return probe_health_def_group_diskspace

    @staticmethod
    def get_system_temperatures(fahrenheit):
        if not hasattr(psutil, "sensors_temperatures"):
            return None
        temperatures = psutil.sensors_temperatures(fahrenheit=fahrenheit)
        if temperatures == {}:
            return None

        return temperatures

    @staticmethod
    def get_system_partitions():
        return psutil.disk_partitions()

    @staticmethod
    def get_partition_usage(partition):
        return psutil.disk_usage(partition[1])

    @staticmethod
    def get_memory_usage():
        vmemory = psutil.virtual_memory()
        swapmemory = psutil.swap_memory()

        return vmemory, swapmemory

    @staticmethod
    def get_cpu_load():
        return psutil.getloadavg()


class SensorSNMPBase(SensorBase, ABC):
    @property
    def snmp_specific_settings_group(self):
        snmp_group_snmp_specifications = SensorDefinitionGroup(name="snmpspecific", caption="SNMP Specific")
        snmp_group_snmp_specifications.add_field(
            field_type="edit",
            name="community",
            caption="Community String",
            required="1",
            help="Please enter the community string.",
        )
        snmp_group_snmp_specifications.add_field(
            field_type="integer",
            name="port",
            caption="SNMP Port",
            required="1",
            help="Please enter SNMP Port.",
        )
        snmp_group_snmp_specifications.add_field(
            field_type="radio",
            name="snmp_version",
            caption="SNMP Version",
            required="1",
            help="Choose your SNMP Version",
            options={"0": "V1", "1": "V2c", "2": "V3"},
            default="1",
        )
        return snmp_group_snmp_specifications

    async def get(
        self,
        target: str,
        oids: list,
        credentials: CommunityData,
        port: int = 161,
        engine: SnmpEngine = SnmpEngine(),
        context: ContextData = ContextData(),
    ) -> list:
        (error_indication, error_status, error_index, var_binds,) = await pysnmp_asyncio.getCmd(
            engine,
            credentials,
            UdpTransportTarget((target, port)),
            context,
            *self.construct_object_types(oids),
        )
        if error_indication:
            logging.error(error_indication)
            raise PySnmpError(error_indication)
        elif error_status:
            msg = f"{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}"
            logging.error(msg)
            raise PySnmpError(msg)
        return var_binds

    async def get_bulk(
        self,
        target: str,
        oids: list,
        credentials: CommunityData,
        port: int = 161,
        engine: SnmpEngine = SnmpEngine(),
        context: ContextData = ContextData(),
    ):
        # todo:  Probably we won't need bulk get
        result = []
        var_binds = self.construct_object_types(oids)
        initial_var_binds = var_binds
        while True:
            (error_indication, error_status, error_index, var_bind_table,) = await pysnmp_asyncio.nextCmd(
                engine,
                credentials,
                UdpTransportTarget((target, port)),
                context,
                *var_binds,
                lookupValues=True,
                lookupNames=True,
            )

            if error_indication:
                logging.error(error_indication)
                raise PySnmpError(error_indication)
            elif error_status:
                msg = f"{error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1][0] or '?'}"
                logging.error(msg)
                raise PySnmpError(msg)
            else:
                for var_bind_row in var_bind_table:
                    result.append(var_bind_row)

                var_binds = var_bind_table[-1]
                if pysnmp_asyncio.isEndOfMib(var_binds):
                    break

                for idx, var_bind in enumerate(var_binds):
                    if initial_var_binds[0][idx].isPrefixOf(var_bind[0]):
                        break

                else:
                    break

        return result

    @staticmethod
    def construct_object_types(list_of_oids: list) -> list:
        object_types = []
        for oid in list_of_oids:
            object_types.append(ObjectType(ObjectIdentity(oid)))
        return object_types

    @staticmethod
    def cast(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                return str(value)
