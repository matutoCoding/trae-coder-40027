from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class StorageTank:
    id: str
    name: str
    tank_type: str
    capacity: float
    material: str
    medium: str
    location: str
    diameter: float
    height: float
    design_pressure: float
    design_temperature: float
    install_date: str
    last_inspection_date: str
    status: str
    current_volume: float
    current_level: float
    current_temperature: float
    current_pressure: float
    nitrogen_pressure: float
    description: str = ""


@dataclass
class ReceiveRecord:
    id: str
    tank_id: str
    tank_name: str
    medium: str
    supplier: str
    vehicle_no: str
    driver: str
    receive_date: str
    receive_time: str
    before_volume: float
    after_volume: float
    receive_volume: float
    before_level: float
    after_level: float
    temperature: float
    density: float
    operator: str
    inspector: str
    status: str
    remark: str = ""


@dataclass
class DispatchRecord:
    id: str
    tank_id: str
    tank_name: str
    medium: str
    customer: str
    vehicle_no: str
    driver: str
    dispatch_date: str
    dispatch_time: str
    before_volume: float
    after_volume: float
    dispatch_volume: float
    before_level: float
    after_level: float
    temperature: float
    density: float
    operator: str
    inspector: str
    status: str
    remark: str = ""


@dataclass
class InspectionRecord:
    id: str
    inspection_date: str
    inspection_time: str
    inspector: str
    location: str
    check_items: List[str]
    abnormal_items: List[str]
    status: str
    remark: str = ""


@dataclass
class NitrogenSealRecord:
    id: str
    tank_id: str
    tank_name: str
    record_date: str
    record_time: str
    inlet_pressure: float
    tank_pressure: float
    set_pressure: float
    valve_status: str
    operator: str
    status: str
    remark: str = ""


@dataclass
class GasDetector:
    id: str
    location: str
    detector_type: str
    gas_type: str
    current_value: float
    alarm_threshold: float
    unit: str
    status: str
    last_calibration: str
    next_calibration: str


@dataclass
class FireFightingEquipment:
    id: str
    name: str
    type: str
    location: str
    quantity: int
    install_date: str
    last_check_date: str
    status: str
    remark: str = ""


@dataclass
class HotWorkPermit:
    id: str
    permit_no: str
    work_location: str
    work_type: str
    work_content: str
    applicant: str
    apply_date: str
    start_time: str
    end_time: str
    guardian: str
    approver: str
    approve_date: str
    status: str
    remark: str = ""


@dataclass
class EmergencyDrill:
    id: str
    drill_name: str
    drill_type: str
    drill_date: str
    location: str
    organizer: str
    participants: int
    duration: float
    status: str
    summary: str = ""


@dataclass
class LightningProtectionCheck:
    id: str
    check_date: str
    check_location: str
    inspector: str
    grounding_resistance: float
    standard_resistance: float
    equipment_status: str
    status: str
    remark: str = ""


@dataclass
class CofferdamRecord:
    id: str
    record_date: str
    location: str
    liquid_level: float
    liquid_type: str
    discharge_status: str
    operator: str
    status: str
    remark: str = ""
