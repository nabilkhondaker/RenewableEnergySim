import logging

logger = logging.getLogger(__name__)

class LoadBalancer:
    def __init__(self, inverter, battery):
        self.inverter = inverter
        self.battery = battery

    def dispatch(self, pv_dc_kw: float, demand_ac_kw: float) -> dict:
        """
        Balances the power flow between PV, Battery, Load, and Grid.
        Prioritizes meeting local load, then charging battery, then exporting.
        """
        # 1. Convert PV DC to AC
        pv_ac_kw = self.inverter.convert_dc_to_ac(pv_dc_kw)
        
        net_power = pv_ac_kw - demand_ac_kw
        grid_import_kw = 0.0
        grid_export_kw = 0.0
        
        if net_power > 0:
            # We have excess power
            # Convert AC back to DC to charge battery (assuming AC coupled system for sim)
            excess_dc = net_power * 0.95 # rectifying loss
            unabsorbed_dc = self.battery.charge(excess_dc * 1000, 1.0) / 1000.0
            
            # Export whatever the battery couldn't take
            grid_export_kw = unabsorbed_dc * 0.95 # inverter loss
            
        elif net_power < 0:
            # We have a deficit
            deficit_dc = abs(net_power) / 0.95 # inverter loss taken into account
            unmet_dc = self.battery.discharge(deficit_dc * 1000, 1.0) / 1000.0
            
            # Import whatever the battery couldn't provide
            grid_import_kw = unmet_dc / 0.95
            
        return {
            "pv_ac_kw": pv_ac_kw,
            "grid_import_kw": grid_import_kw,
            "grid_export_kw": grid_export_kw,
            "battery_soc": self.battery.get_soc()
        }
