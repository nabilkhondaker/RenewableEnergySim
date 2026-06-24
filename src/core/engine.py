import yaml
from src.utils.logger import setup_logging, logger
from src.models.solar_panel import SolarArray, SolarPanelConfig
from src.models.battery import BatteryESS
from src.models.inverter import Inverter
from src.core.load_balancer import LoadBalancer
from src.data_fetchers.weather_api import WeatherDataFetcher

class SimulationEngine:
    def __init__(self, config_path="config/settings.yaml"):
        setup_logging()
        logger.info("Initializing Simulation Engine...")
        
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        # Init hardware models
        self.solar_array = SolarArray(SolarPanelConfig(), num_panels=100)
        self.battery = BatteryESS(capacity_kwh=50.0, max_charge_kw=25.0)
        self.inverter = Inverter(rated_power_kw=40.0)
        
        # Init control logic
        self.balancer = LoadBalancer(self.inverter, self.battery)
        self.weather_fetcher = WeatherDataFetcher(lat=33.9533, lon=-117.3961)

    def run(self):
        logger.info("Fetching environmental data...")
        weather_data = self.weather_fetcher.get_daily_profile()
        
        logger.info("Starting simulation loop...")
        results = []
        
        for index, row in weather_data.iterrows():
            # 1. Generate Power
            pv_dc_w = self.solar_array.calculate_power(row['irradiance_w_m2'], row['temperature_c'])
            pv_dc_kw = pv_dc_w / 1000.0
            
            # 2. Assume constant load for headless sim
            demand_kw = 15.0 
            
            # 3. Dispatch
            dispatch_state = self.balancer.dispatch(pv_dc_kw, demand_kw)
            
            # 4. Log step
            logger.debug(f"Time: {row['time']} | PV: {pv_dc_kw:.2f}kW | SOC: {dispatch_state['battery_soc']*100:.1f}%")
            results.append(dispatch_state)
            
        logger.info("Simulation complete.")
        return results

if __name__ == "__main__":
    engine = SimulationEngine()
    engine.run()
