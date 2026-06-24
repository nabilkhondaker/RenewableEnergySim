import pytest
from src.core.mppt import MPPTController

def test_mppt_perturb_and_observe():
    mppt = MPPTController(step_size=0.5)
    mppt.v_ref = 24.0
    mppt.prev_p = 100.0
    mppt.prev_v = 23.5
    
    # Current state: Voltage went UP (23.5 -> 24.0), Power went UP (100 -> 110)
    # P&O logic dictates it should keep increasing voltage
    next_v = mppt.optimize(v_current=24.0, i_current=110/24.0) 
    
    assert next_v == 24.5 # Step size added
    
    # Current state: Voltage went UP (24.0 -> 24.5), Power went DOWN (110 -> 105)
    # P&O logic dictates it went too far, should decrease voltage
    next_v2 = mppt.optimize(v_current=24.5, i_current=105/24.5)
    
    assert next_v2 == 24.0 # Step size subtracted
