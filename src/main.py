import json
from src.crew.cmos_crew import SimpleCMOSAnalyzer


def main():
    """Main entry point for CMOS Circuit Analysis"""
    
    sample_netlist = """
CMOS Inverter Circuit
* Basic CMOS Inverter
M1 out in vdd vdd pmos W=20u L=1u
M2 out in gnd gnd nmos W=10u L=1u
VDD vdd 0 DC 5V
VIN in 0 DC 2.5V
.end
"""
    
    print("="*70)
    print("CMOS CIRCUIT ANALYSIS AGENT")
    print("="*70)
    print()
    
    analyzer = SimpleCMOSAnalyzer()
    
    print("Input Netlist:")
    print("-" * 70)
    print(sample_netlist)
    print("-" * 70)
    print()
    
    print("Analyzing circuit...")
    results = analyzer.analyze_circuit(sample_netlist)
    
    print("\nANALYSIS RESULTS")
    print("=" * 70)
    
    print(f"\nCircuit: {results['circuit_name']}")
    print(f"Total Devices: {results['summary']['total_devices']}")
    print(f"Supply Voltage: {results['analysis']['power_analysis']['supply_voltage']}V")
    
    print("\nCircuit Topology:")
    print(f"  NMOS Count: {results['topology']['nmos_count']}")
    print(f"  PMOS Count: {results['topology']['pmos_count']}")
    print(f"  Total Devices: {results['topology']['total_devices']}")
    
    print("\nDevice Details:")
    for device in results['topology']['devices']:
        print(f"  {device['name']}: {device['type']} (W/L = {device['wl_ratio']:.1f})")
    
    print("\nDesign Compliance Check:")
    compliance = results['analysis']['design_compliance']
    print(f"  Rules Passed: {compliance['rules_passed']}")
    print(f"  Rules Failed: {compliance['rules_failed']}")
    
    if compliance['violations']:
        print("  Violations:")
        for violation in compliance['violations']:
            print(f"    - {violation}")
    
    print("\nFault Detection Results:")
    print(f"  Total Issues: {results['summary']['total_faults']}")
    print(f"  Critical Issues: {results['summary']['critical_issues']}")
    print(f"  High Priority Issues: {results['summary']['high_priority_issues']}")
    
    if results['faults']:
        print("\n  Detected Faults:")
        for fault in results['faults']:
            print(f"\n    [{fault['severity']}] {fault['type']}")
            print(f"      Description: {fault['description']}")
            print(f"      Recommendation: {fault['recommendation']}")
    else:
        print("\n  ✓ No faults detected")
    
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    
    with open('analysis_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("✓ Results saved to analysis_report.json")


if __name__ == "__main__":
    main()
