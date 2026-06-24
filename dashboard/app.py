import sys
import os
import streamlit as st

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.solar_panel import SolarArray, SolarPanelConfig
from src.models.battery import BatteryESS
from src.data_fetchers.weather_api import WeatherDataFetcher
from dashboard.components.kpi_cards import render_kpi_cards
from dashboard.components.live_charts import render_main_dashboard

# Setup Page
st.set_page_config(page_title="ESS Simulator", layout="wide")

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("⚡ Multi-Node Microgrid Simulator by Nabil Khondaker")

# --- Sidebar UI ---
st.sidebar.header("Control Parameters")
num_panels = st.sidebar.slider("PV Array Size (Panels)", 10, 500, 100)
battery_capacity = st.sidebar.number_input("ESS Capacity (kWh)", 10.0, 500.0, 50.0)
load_demand_kw = st.sidebar.slider("Base Load (kW)", 1.0, 50.0, 15.0)

# --- Engine Initialization ---
config = SolarPanelConfig()
array = SolarArray(config, num_panels=num_panels)
battery = BatteryESS(capacity_kwh=battery_capacity, max_charge_kw=battery_capacity/2)
fetcher = WeatherDataFetcher(lat=33.9533, lon=-117.3961)

# --- Simulation Execution ---
with st.spinner("Compiling Dispatch Data..."):
    df = fetcher.get_daily_profile()
    
    results = {
        "time": df["time"].tolist(),
        "pv_generation_kw": [], "load_kw": [], "battery_soc": [],
        "grid_import_kw": [], "grid_export_kw": []
    }
    
    for _, row in df.iterrows():
        pv_kw = array.calculate_power(row["irradiance_w_m2"], row["temperature_c"]) / 1000.0
        net_power = pv_kw - load_demand_kw
        grid_import, grid_export = 0.0, 0.0
        
        if net_power > 0:
            excess_w = battery.charge(net_power * 1000, dt_hours=1.0)
            grid_export = excess_w / 1000.0
        else:
            deficit_w = battery.discharge(abs(net_power) * 1000, dt_hours=1.0)
            grid_import = deficit_w / 1000.0
            
        results["pv_generation_kw"].append(pv_kw)
        results["load_kw"].append(load_demand_kw)
        results["battery_soc"].append(battery.get_soc() * 100)
        results["grid_import_kw"].append(grid_import)
        results["grid_export_kw"].append(grid_export)

# --- Component Rendering ---
render_kpi_cards(results)
render_main_dashboard(results)
