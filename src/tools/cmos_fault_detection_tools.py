from typing import List
from src.models.cmos_circuit import CMOSCircuit, FaultReport


class CMOSFaultDetector:
    """Detects faults and design issues in CMOS circuits"""
    
    def __init__(self):
        self.fault_database = {
            "body_effect": "Substrate bias effect causing threshold voltage variation",
            "short_circuit": "Crowbar current between VDD and GND in CMOS gates",
            "leakage": "Excessive static current consumption",
            "saturation": "Device operating in triode region instead of saturation",
            "wl_mismatch": "W/L ratio mismatch between matched pairs",
        }
    
    def detect_faults(self, circuit: CMOSCircuit) -> List[FaultReport]:
        """Detect potential faults in CMOS circuit"""
        faults = []
        
        faults.extend(self._check_complementary_pairs(circuit.devices))
        faults.extend(self._check_device_sizing(circuit.devices))
        faults.extend(self._check_body_biasing(circuit.devices))
        faults.extend(self._check_power_distribution(circuit))
        
        return faults
    
    def _check_complementary_pairs(self, devices: List) -> List[FaultReport]:
        """Check for proper NMOS-PMOS complementary pairs"""
        faults = []
        
        nmos_count = sum(1 for d in devices if d.device_type == "NMOS")
        pmos_count = sum(1 for d in devices if d.device_type == "PMOS")
        
        if nmos_count == 0:
            faults.append(FaultReport(
                circuit_name="Unknown",
                fault_type="missing_nmos",
                severity="Critical",
                description="No NMOS devices found in circuit",
                affected_devices=[],
                recommendation="Add NMOS devices to complete CMOS topology"
            ))
        
        if pmos_count == 0:
            faults.append(FaultReport(
                circuit_name="Unknown",
                fault_type="missing_pmos",
                severity="Critical",
                description="No PMOS devices found in circuit",
                affected_devices=[],
                recommendation="Add PMOS devices to complete CMOS topology"
            ))
        
        return faults
    
    def _check_device_sizing(self, devices: List) -> List[FaultReport]:
        """Check for improper device sizing"""
        faults = []
        
        nmos_devices = [d for d in devices if d.device_type == "NMOS"]
        pmos_devices = [d for d in devices if d.device_type == "PMOS"]
        
        if nmos_devices and pmos_devices:
            avg_nmos_wl = sum(d.width/d.length for d in nmos_devices) / len(nmos_devices)
            avg_pmos_wl = sum(d.width/d.length for d in pmos_devices) / len(pmos_devices)
            
            if avg_pmos_wl < avg_nmos_wl * 1.5:
                faults.append(FaultReport(
                    circuit_name="Unknown",
                    fault_type="pmos_undersized",
                    severity="High",
                    description="PMOS devices may be undersized relative to NMOS",
                    affected_devices=[d.name for d in pmos_devices],
                    recommendation="Increase PMOS W/L ratio (typically 2-3x NMOS)"
                ))
        
        return faults
    
    def _check_body_biasing(self, devices: List) -> List[FaultReport]:
        """Check for body biasing issues"""
        faults = []
        
        pmos_devices = [d for d in devices if d.device_type == "PMOS"]
        
        if pmos_devices:
            faults.append(FaultReport(
                circuit_name="Unknown",
                fault_type="body_bias_check",
                severity="Medium",
                description="Ensure PMOS bulk connected to VDD and NMOS bulk to GND",
                affected_devices=[d.name for d in pmos_devices],
                recommendation="Verify bulk connections in netlist for body effect minimization"
            ))
        
        return faults
    
    def _check_power_distribution(self, circuit: CMOSCircuit) -> List[FaultReport]:
        """Check power distribution issues"""
        faults = []
        
        if circuit.power_supply > 3.3 and len(circuit.devices) > 10:
            faults.append(FaultReport(
                circuit_name=circuit.name,
                fault_type="power_dissipation",
                severity="Medium",
                description="High supply voltage with multiple devices may cause excessive power dissipation",
                affected_devices=[d.name for d in circuit.devices],
                recommendation="Consider power management techniques or verify thermal design"
            ))
        
        return faults
    
    def get_fault_summary(self, faults: List[FaultReport]) -> str:
        """Generate summary of detected faults"""
        if not faults:
            return "No faults detected! Circuit design looks good."
        
        critical = [f for f in faults if f.severity == "Critical"]
        high = [f for f in faults if f.severity == "High"]
        medium = [f for f in faults if f.severity == "Medium"]
        
        summary = f"""
CMOS Fault Detection Report
{'='*60}

Total Issues Found: {len(faults)}
  - Critical: {len(critical)}
  - High: {len(high)}
  - Medium: {len(medium)}

Issues:
"""
        
        for fault in faults:
            summary += f"\n[{fault.severity}] {fault.fault_type}: {fault.description}\n"
            summary += f"  Recommendation: {fault.recommendation}\n"
        
        return summary
