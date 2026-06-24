class BatteryESS:
    def __init__(self, capacity_kwh: float, max_charge_kw: float, efficiency: float = 0.95):
        self.capacity_wh = capacity_kwh * 1000
        self.max_charge_w = max_charge_kw * 1000
        self.efficiency = efficiency
        self.current_charge_wh = self.capacity_wh * 0.5 # Start at 50% SOC

    def charge(self, power_w: float, dt_hours: float) -> float:
        """Charges battery, returns unabsorbed (excess) power in Watts."""
        available_capacity = self.capacity_wh - self.current_charge_wh
        max_input = min(power_w, self.max_charge_w)
        
        energy_to_add = max_input * dt_hours * self.efficiency
        
        if energy_to_add <= available_capacity:
            self.current_charge_wh += energy_to_add
            return power_w - max_input # Return clipped power
        else:
            self.current_charge_wh = self.capacity_wh
            excess_energy = energy_to_add - available_capacity
            return power_w - (max_input - (excess_energy / dt_hours / self.efficiency))

    def discharge(self, required_power_w: float, dt_hours: float) -> float:
        """Discharges battery, returns deficit power if empty."""
        energy_needed = (required_power_w * dt_hours) / self.efficiency
        
        if self.current_charge_wh >= energy_needed:
            self.current_charge_wh -= energy_needed
            return 0.0 # Met all demand
        else:
            provided_energy = self.current_charge_wh
            self.current_charge_wh = 0.0
            deficit_energy = energy_needed - provided_energy
            return (deficit_energy * self.efficiency) / dt_hours

    def get_soc(self) -> float:
        """Returns State of Charge (0.0 to 1.0)"""
        return self.current_charge_wh / self.capacity_wh
