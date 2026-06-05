from typing import Dict, List, Any
from src.models.cmos_circuit import CMOSCircuit


class CMOSAnalyzer:
    """Analyzer for CMOS circuit characteristics and design rules"""
    
    def __init__(self):
        self.design_rules = {
            "min_wl_ratio": 0.5,
            "max_wl_ratio": 100,
            "min_channel_length": 1e-7,
            "vgs_margin": 0.2,
        }
    
    def analyze_circuit(self, circuit: CMOSCircuit) -> Dict[str, Any]:
        """Perform comprehensive CMOS circuit analysis"""
        analysis = {
            "circuit_name": circuit.name,
            "device_count": len(circuit.devices),
            "topology_analysis": self._analyze_topology(circuit.devices),
            "power_analysis": self._analyze_power(circuit),
            "device_matching": self._check_device_matching(circuit.devices),
            "design_compliance": self._check_design_compliance(circuit.devices),
        }
        
        return analysis
    
    def _analyze_topology(self, devices: List) -> Dict[str, Any]:
        """Analyze circuit topology"""
        nmos_devices = [d for d in devices if d.device_type == "NMOS"]
        pmos_devices = [d for d in devices if d.device_type == "PMOS"]
        
        analysis = {
            "total_devices": len(devices),
            "nmos_count": len(nmos_devices),
            "pmos_count": len(pmos_devices),
            "complementary": "Balanced" if abs(len(nmos_devices) - len(pmos_devices)) <= 1 else "Unbalanced",
        }
        
        return analysis
    
    def _analyze_power(self, circuit: CMOSCircuit) -> Dict[str, Any]:
        """Analyze power characteristics"""
        power_analysis = {
            "supply_voltage": circuit.power_supply,
            "estimated_static_power": "Requires simulation",
            "estimated_dynamic_power": "Requires simulation",
            "power_efficiency": "Requires simulation",
        }
        
        return power_analysis
    
    def _check_device_matching(self, devices: List) -> Dict[str, Any]:
        """Check for proper device matching in differential pairs"""
        matching = {
            "mirror_pairs_found": 0,
            "matching_errors": [],
            "recommendations": []
        }
        
        nmos_ratios = [d.width / d.length for d in devices if d.device_type == "NMOS"]
        pmos_ratios = [d.width / d.length for d in devices if d.device_type == "PMOS"]
        
        if nmos_ratios and max(nmos_ratios) / min(nmos_ratios) > 2.0:
            matching["recommendations"].append("NMOS devices have significant W/L variation - check matching")
        
        if pmos_ratios and max(pmos_ratios) / min(pmos_ratios) > 2.0:
            matching["recommendations"].append("PMOS devices have significant W/L variation - check matching")
        
        return matching
    
    def _check_design_compliance(self, devices: List) -> Dict[str, Any]:
        """Check compliance with CMOS design rules"""
        compliance = {
            "rules_passed": 0,
            "rules_failed": 0,
            "violations": []
        }
        
        for device in devices:
            wl_ratio = device.width / device.length
            
            if wl_ratio < self.design_rules["min_wl_ratio"]:
                compliance["rules_failed"] += 1
                compliance["violations"].append(
                    f"{device.name}: W/L ratio too low ({wl_ratio:.2f})"
                )
            elif wl_ratio > self.design_rules["max_wl_ratio"]:
                compliance["rules_failed"] += 1
                compliance["violations"].append(
                    f"{device.name}: W/L ratio too high ({wl_ratio:.2f})"
                )
            else:
                compliance["rules_passed"] += 1
            
            if device.length < self.design_rules["min_channel_length"]:
                compliance["rules_failed"] += 1
                compliance["violations"].append(
                    f"{device.name}: Channel length below minimum"
                )
        
        return compliance
    
    def get_design_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a summary of the analysis"""
        summary = f"""
CMOS Circuit Analysis Summary: {analysis['circuit_name']}
{'='*60}

Topology:
  - Total Devices: {analysis['topology_analysis']['total_devices']}
  - NMOS: {analysis['topology_analysis']['nmos_count']}
  - PMOS: {analysis['topology_analysis']['pmos_count']}
  - Complementary: {analysis['topology_analysis']['complementary']}

Design Compliance:
  - Rules Passed: {analysis['design_compliance']['rules_passed']}
  - Rules Failed: {analysis['design_compliance']['rules_failed']}
  
Power:
  - Supply Voltage: {analysis['power_analysis']['supply_voltage']}V

Recommendations:
"""
        for rec in analysis['device_matching']['recommendations']:
            summary += f"  - {rec}\n"
        
        return summary
