import json
import os
from typing import Dict

from heaty.quantity.scalar import Quantity as Qty


ROOT_PATH = os.getcwd()

RESOURCES_PATH = os.path.dirname(__file__)
RESOURCES_PATH = os.path.split(RESOURCES_PATH)[0]
RESOURCES_PATH = os.path.join(RESOURCES_PATH, 'resources')

SETTINGS_PATH = os.path.join(ROOT_PATH, 'settings')


def find_file(default_path: str, file_name: str):
    if not os.path.exists(default_path):
        return os.path.join(ROOT_PATH, 'resources', file_name)
    else:
        return os.path.join(default_path, file_name)


class Paths:
    cfg_file = os.path.normpath(os.path.join(SETTINGS_PATH, 'paths.json'))
    paths: Dict[str, str] = {
        'PROJECT_PATH': os.path.join(ROOT_PATH, 'projects'),
        'EXPORT_PATH': os.path.join(ROOT_PATH, 'export')
    }

    @classmethod
    def create_paths(cls):
        for path in cls.paths.values():
            if not os.path.exists(path):
                os.mkdir(path)

    @classmethod
    def write_config_file(cls):
        with open(cls.cfg_file, 'w') as fh:
            json.dump(cls.paths, fh)

    @classmethod
    def read_config_file(cls):
        with open(cls.cfg_file) as fh:
            cls.paths = json.load(fh)

    @staticmethod
    def validate(path: str) -> bool:
        if os.path.exists(path):
            return True
        return False


class Units:
    cfg_file = os.path.normpath(os.path.join(SETTINGS_PATH, 'units.json'))

    volume_flow_rate: str = 'volume flow rate'
    pressure: str = 'pressure'
    temperature: str = 'temperature'
    temperature_difference: str = 'temperature difference'
    temperature_gradient: str = 'temperature gradient'
    area: str = 'area'
    volume: str = 'volume'
    length: str = 'length'
    air_permeability: str = 'air permeability'
    air_change_rate: str = 'air change rate'
    power_flux: str = 'thermal power flux'
    power: str = 'thermal power'
    transmittance: str = 'transmittance'

    units: Dict[str, str] = {
        volume_flow_rate: 'm ** 3 / hr',
        pressure: 'Pa',
        temperature: 'degC',
        temperature_difference: 'K',
        temperature_gradient: 'K / m',
        area: 'm ** 2',
        volume: 'm ** 3',
        length: 'm',
        air_permeability: 'm ** 3 / (m ** 2 * hr)',
        air_change_rate: '1 / hr',
        power_flux: 'W / m ** 2',
        power: 'W',
        transmittance: 'W / (m ** 2 * K)'
    }

    basic_qties: Dict[str, Qty] = {
        volume_flow_rate: Qty(1.0, 'm ** 3 / hr'),
        pressure: Qty(1.0, 'Pa'),
        temperature: Qty(1.0, 'degC'),
        temperature_difference: Qty(1.0, 'K'),
        temperature_gradient: Qty(1.0, 'K / m'),
        area: Qty(1.0, 'm ** 2'),
        volume: Qty(1.0, 'm ** 3'),
        length: Qty(1.0, 'm'),
        air_permeability: Qty(1.0, 'm ** 3 / (m ** 2 * hr)'),
        air_change_rate: Qty(1.0, '1 / hr'),
        power_flux: Qty(1.0, 'W / m ** 2'),
        power: Qty(1.0, 'W'),
        transmittance: Qty(1.0, 'W / (m ** 2 * K)')
    }

    @classmethod
    def write_config_file(cls):
        with open(cls.cfg_file, 'w') as fh:
            json.dump(cls.units, fh)

    @classmethod
    def read_config_file(cls):
        with open(cls.cfg_file) as fh:
            cls.units = json.load(fh)

    @classmethod
    def default_unit(cls, quantity: str) -> str:
        return cls.units.get(quantity)

    @classmethod
    def validate(cls, quantity: str, unit: str) -> bool:
        basic_quantity = cls.basic_qties[quantity]
        if basic_quantity.check_unit(unit):
            return True
        else:
            return False


def create_settings_path():
    if not os.path.exists(SETTINGS_PATH):
        os.mkdir(SETTINGS_PATH)


def load_program_settings():
    try:
        Paths.read_config_file()
        Units.read_config_file()
    except FileNotFoundError:
        create_settings_path()
        Paths.create_paths()
        Paths.write_config_file()
        Units.write_config_file()
