
import sys
import os
import pytest

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.global_orchestrator import GlobalSafetyOrchestrator

def test_day_100_capstone():
    print("Testing Day 100: Phase 4 Capstone - Global Safety Orchestrator...")
    
    orchestrator = GlobalSafetyOrchestrator()
    
    # 1. Test Safe Global Plan
    title1 = "Renewable energy transition plan"
    desc1 = "Shifting national power grids to solar and wind to mitigate climate_change."
    res1 = orchestrator.audit_global_plan(title1, desc1, "GreenEnergy_Inc", "EU")
    
    # Should pass all
    assert res1.is_authorized == True
    assert res1.verdicts["Science"] == "PASS"
    
    # 2. Test Plan with Fatal Violations
    title2 = "Rapid Industrial Expansion"
    desc2 = "New coal plants using uranium for fuel. Boost output via labor working hours expansion."
    res2 = orchestrator.audit_global_plan(title2, desc2, "BigOil_Corp", "USA")
    
    assert res2.is_authorized == False
    assert "REJECTED" in res2.verdicts["Policy"]
