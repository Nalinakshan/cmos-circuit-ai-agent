from typing import Dict, Any, List
from src.tools.netlist_parser import NetlistParser
from src.tools.cmos_analyzer import CMOSAnalyzer
from src.tools.cmos_fault_detection_tools import CMOSFaultDetector


class SimpleCMOSAnalyzer:
    """Simplified CMOS analyzer for quick analysis"""
    
    def __init__(self):
        self.parser = NetlistParser()
        self.analyzer = CMOSAnalyzer()
        self.fault_detector = CMOSFaultDetector()
    
    def analyze_circuit(self, netlist: str) -> dict:
        """Perform complete CMOS circuit analysis"""
        
        # Parse netlist
        circuit = self.parser.parse_netlist(netlist)
        
        # Perform analysis
        analysis = self.analyzer.analyze_circuit(circuit)
        
        # Detect faults
        faults = self.fault_detector.detect_faults(circuit)
        
        # Compile results
        results = {
            "circuit_name": circuit.name,
            "topology": self.parser.get_circuit_topology(),
            "analysis": analysis,
            "faults": [
                {
                    "type": f.fault_type,
                    "severity": f.severity,
                    "description": f.description,
                    "recommendation": f.recommendation
                }
                for f in faults
            ],
            "summary": {
                "total_devices": len(circuit.devices),
                "total_faults": len(faults),
                "critical_issues": sum(1 for f in faults if f.severity == "Critical"),
                "high_priority_issues": sum(1 for f in faults if f.severity == "High"),
            }
        }
        
        return results
