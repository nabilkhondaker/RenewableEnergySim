import numpy as np
from dataclasses import dataclass

@dataclass
class SolarPanelConfig:
    area: float = 1.6 # m^2
    efficiency: float = 0.20 # 20%
    temp_coefficient: float = 0.004 # 0.4% per degree C over 25
    nominal_voltage: float = 36.0 # V

class SolarArray:
    def __init__(self, config: SolarPanelConfig, num_panels: int):
        self.config = config
        self.num_panels = num_panels
        self.total_area = config.area * num_panels

    def calculate_power(self, irradiance: float, temp_c: float) -> float:
        """
        Calculates DC power output based on environmental factors.
        Returns Power in Watts.
        """
        if irradiance <= 0:
            return 0.0
            
        # Temperature degradation factor
        temp_loss = max(0, (temp_c - 25.0) * self.config.temp_coefficient)
        actual_efficiency = self.config.efficiency * (1 - temp_loss)
        
        power_w = actual_efficiency * self.total_area * irradiance
        return power_w

    def get_iv_curve(self, irradiance: float) -> tuple:
        """Simulates an I-V curve for MPPT algorithm testing."""
        v = np.linspace(0, self.config.nominal_voltage * 1.2, 100)
        i_sc = (irradiance / 1000.0) * 8.5 # Approx short circuit current
        i = i_sc - 1e-7 * (np.exp(v / 2.5) - 1) # Simplified diode equation
        i[i < 0] = 0
        return v, i
