from src.utils.math_helpers import calculate_inverter_efficiency_curve

class Inverter:
    def __init__(self, rated_power_kw: float):
        self.rated_power_kw = rated_power_kw

    def convert_dc_to_ac(self, dc_power_kw: float) -> float:
        """Converts DC power from panels/battery to AC power for the grid/load."""
        if dc_power_kw <= 0:
            return 0.0
            
        load_percentage = dc_power_kw / self.rated_power_kw
        
        # Overload protection
        if load_percentage > 1.1:
            dc_power_kw = self.rated_power_kw * 1.1 
            load_percentage = 1.1
            
        efficiency = calculate_inverter_efficiency_curve(load_percentage)
        return dc_power_kw * efficiency
