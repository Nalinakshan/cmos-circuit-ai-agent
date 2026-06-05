from typing import Optional
from pydantic import BaseModel


class MOSFETDevice(BaseModel):
    """Model for MOSFET device information"""
    name: str
    device_type: str  # NMOS or PMOS
    width: float
    length: float
    gate_voltage: Optional[float] = None
    drain_voltage: Optional[float] = None
    source_voltage: Optional[float] = None
    

class CMOSCircuit(BaseModel):
    """Model for CMOS Circuit"""
    name: str
    netlist: str
    devices: list
    power_supply: float
    temperature: float = 27.0  # Celsius


class SimulationResult(BaseModel):
    """Model for simulation results"""
    circuit_name: str
    simulation_type: str  # AC, DC, Transient
    metrics: dict
    success: bool
    error_message: Optional[str] = None
    
    
class FaultReport(BaseModel):
    """Model for fault detection report"""
    circuit_name: str
    fault_type: str
    severity: str  # Critical, High, Medium, Low
    description: str
    affected_devices: list
    recommendation: str
  
