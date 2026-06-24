import pytest
from src.models.solar_panel import SolarArray, SolarPanelConfig
from src.models.battery import BatteryESS

def test_solar_panel_power_output():
    config = SolarPanelConfig(area=2.0, efficiency=0.20)
    array = SolarArray(config, num_panels=10)
    
    # Under STC (Standard Test Conditions: 1000 W/m2, 25C)
    # Expected power = 0.20 * (2.0 * 10) * 1000 = 4000W
    power = array.calculate_power(irradiance=1000.0, temp_c=25.0)
    
    assert power == 4000.0
    
def test_solar_panel_temp_degradation():
    config = SolarPanelConfig(area=2.0, efficiency=0.20, temp_coefficient=0.005)
    array = SolarArray(config, num_panels=10)
    
    power_stc = array.calculate_power(1000.0, 25.0)
    power_hot = array.calculate_power(1000.0, 45.0) # 20 degrees hotter
    
    # Should produce less power when hot
    assert power_hot < power_stc

def test_battery_charge_and_discharge():
    # 10kWh battery, max charge 5kW
    battery = BatteryESS(capacity_kwh=10.0, max_charge_kw=5.0, efficiency=1.0)
    battery.current_charge_wh = 0.0 # Force empty
    
    # Charge with 2kW for 1 hour
    excess = battery.charge(power_w=2000.0, dt_hours=1.0)
    assert excess == 0.0
    assert battery.get_soc() == 0.2 # 2kWh / 10kWh
    
    # Discharge 1kW for 1 hour
    deficit = battery.discharge(required_power_w=1000.0, dt_hours=1.0)
    assert deficit == 0.0
    assert battery.get_soc() == 0.1 # 1kWh / 10kWh
