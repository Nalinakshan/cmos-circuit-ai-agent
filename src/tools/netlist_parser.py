import re
from typing import List, Dict, Any
from src.models.cmos_circuit import MOSFETDevice, CMOSCircuit


class NetlistParser:
    """Parser for SPICE netlists to extract CMOS circuit information"""
    
    def __init__(self):
        self.netlist_lines = []
        self.devices = []
        self.power_supply = 5.0
        
    def parse_netlist(self, netlist_content: str) -> CMOSCircuit:
        """Parse SPICE netlist and extract circuit information"""
        self.netlist_lines = netlist_content.strip().split('\n')
        self.devices = []
        
        circuit_name = "CMOS_Circuit"
        
        for line in self.netlist_lines:
            line = line.strip()
            
            if not line or line.startswith('*') or line.startswith('.'):
                continue
                
            if len(self.netlist_lines) > 0 and line == self.netlist_lines[0]:
                circuit_name = line
                continue
            
            if line.startswith('M'):
                self._parse_mosfet(line)
            
            if line.startswith('VDD') or line.startswith('V'):
                self._parse_voltage_source(line)
        
        circuit = CMOSCircuit(
            name=circuit_name,
            netlist=netlist_content,
            devices=self.devices,
            power_supply=self.power_supply
        )
        
        return circuit
    
    def _parse_mosfet(self, line: str) -> None:
        """Parse MOSFET device line"""
        parts = line.split()
        
        if len(parts) < 7:
            return
        
        name = parts[0]
        device_type = "NMOS" if parts[5].lower().endswith('n') else "PMOS"
        
        width = 1.0
        length = 1.0
        
        for part in parts[6:]:
            if 'W=' in part.upper():
                width = self._extract_value(part)
            elif 'L=' in part.upper():
                length = self._extract_value(part)
        
        device = MOSFETDevice(
            name=name,
            device_type=device_type,
            width=width,
            length=length
        )
        
        self.devices.append(device)
    
    def _parse_voltage_source(self, line: str) -> None:
        """Parse voltage source for power supply"""
        parts = line.split()
        if len(parts) >= 3:
            try:
                voltage = float(parts[2])
                if voltage > 0:
                    self.power_supply = voltage
            except ValueError:
                pass
    
    def _extract_value(self, param: str) -> float:
        """Extract numerical value from parameter string"""
        match = re.search(r'=(\d+\.?\d*[eE]?-?\d*)', param)
        if match:
            value_str = match.group(1)
            if 'u' in param.lower():
                return float(value_str) * 1e-6
            elif 'n' in param.lower():
                return float(value_str) * 1e-9
            elif 'p' in param.lower():
                return float(value_str) * 1e-12
            else:
                return float(value_str)
        return 1.0
    
    def get_circuit_topology(self) -> Dict[str, Any]:
        """Extract circuit topology information"""
        topology = {
            "total_devices": len(self.devices),
            "nmos_count": sum(1 for d in self.devices if d.device_type == "NMOS"),
            "pmos_count": sum(1 for d in self.devices if d.device_type == "PMOS"),
            "devices": [
                {
                    "name": d.name,
                    "type": d.device_type,
                    "w": d.width,
                    "l": d.length,
                    "wl_ratio": d.width / d.length
                }
                for d in self.devices
            ]
        }
        return topology
