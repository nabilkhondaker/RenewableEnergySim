# Renewable Energy Sim

**Enterprise Python renewable energy microgrid simulator, engineered by Nabil Khondaker**

A comprehensive, modular simulation engine for modeling solar PV arrays, battery energy storage systems (BESS), MPPT controllers, load balancing, and real-world weather-driven microgrid operations. Built for accuracy, performance, and interactive visualization.

---

## ✨ Key Features

* **Physics-Based Solar Modeling:** Accurate PV power calculations incorporating irradiance, temperature coefficients, and scalable array sizing.
* **Advanced MPPT Control:** Perturb & Observe (P&O) algorithm implementation for maximum power point tracking with configurable step sizes.
* **Battery Energy Storage System (BESS):** Realistic charge/discharge dynamics, State of Charge (SOC) tracking, and power limits.
* **Intelligent Load Balancing & Dispatch:** Real-time energy management between PV generation, battery storage, and grid import/export.
* **Live Weather Integration:** Fetches historical/forecast weather data (irradiance, temperature) for location-specific simulations.
* **Interactive Streamlit Dashboard:** Beautiful, real-time visualizations with KPI cards, dual-axis power charts, and parameter controls.
* **Enterprise-Grade Architecture:** Modular design with clean separation of concerns, logging, configuration via YAML, and comprehensive tests.
* **Production Ready:** Packaged with `setup.py`, dependency management, and extensible for multi-node microgrids.

---

## 📁 Project Structure
```
RenewableEnergySim/
│
├── config/
│   ├── settings.yaml          # Global simulation parameters
│   └── logging_config.json    # Log rotation and formatting
│
├── data/
│   ├── cache/                 # Cached API responses
│   └── historical_weather.csv # Fallback data
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py          # Main simulation loop
│   │   ├── mppt.py            # Perturb & Observe algorithms
│   │   └── load_balancer.py   # Grid vs. Battery dispatch logic
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── solar_panel.py     # PV physics model
│   │   ├── battery.py         # Energy storage system (ESS) model
│   │   └── inverter.py        # DC-to-AC conversion efficiency mapping
│   │
│   ├── data_fetchers/
│   │   ├── __init__.py
│   │   └── weather_api.py     # OpenMeteo/NREL API integration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── math_helpers.py    # CFD integration stubs, efficiency curves
│       └── logger.py          # System-wide logging
│
├── dashboard/
│   ├── app.py                 # Streamlit web dashboard
│   ├── assets/
│   │   └── styles.css         # UI styling
│   └── components/
│       ├── live_charts.py     # Plotly real-time visualizations
│       └── kpi_cards.py       # Metrics display
│
├── tests/
│   ├── test_models.py
│   └── test_mppt.py
│
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🛠️ Tech Stack

* **Core Logic:** Python 3.9+, NumPy, Pandas
* **Visualization:** Matplotlib, Plotly, Streamlit
* **Data Handling:** Requests (for weather APIs), PyYAML
* **Testing:** pytest
* **Packaging:** setuptools

## 🧰 Concepts & Explanations
### 1. Photovoltaic (PV) Power Output
- **Concept:** A solar panel's power generation depends on its size, the amount of sunlight hitting it (irradiance), and its temperature. Solar panels actually lose efficiency as they get hotter than 25 degrees Celsius.
```
Temp_Loss = Temp_Coefficient * (Current_Temp_C - 25.0)
Actual_Efficiency = Base_Efficiency * (1 - Temp_Loss)
Power_Output = Actual_Efficiency * Total_Area * Irradiance
```

### 2. Perturb & Observe (P&O) MPPT Algorithm
- **Concept:** Maximum Power Point Tracking (MPPT) continuously searches for the "sweet spot" voltage that extracts the absolute maximum power from the solar panel at any given second. The P&O algorithm does this by "perturbing" (nudging) the voltage and "observing" what happens to the power.
```
delta_Power = current_power - previous_power
delta_Voltage = current_voltage - previous_voltage

If delta_Power > 0:
    // Power went up! Keep moving voltage in the same direction.
    If delta_Voltage > 0: increase voltage reference
    Else: decrease voltage reference
Else:
    // Power went down! We went too far, reverse direction.
    If delta_Voltage > 0: decrease voltage reference
    Else: increase voltage reference
```

### 3. 
- **Concept:** Tracking the battery's charge level requires calculating the energy added or removed over time (Power * Time = Energy), while factoring in charging/discharging efficiency losses (heat loss).
```
// Charging
Energy_Added = Input_Power * Time_Hours * Battery_Efficiency
New_Charge_Level = Old_Charge_Level + Energy_Added

// Discharging
Energy_Needed_From_Battery = (Required_Power * Time_Hours) / Battery_Efficiency
New_Charge_Level = Old_Charge_Level - Energy_Needed_From_Battery

// SOC Percentage
SOC = (New_Charge_Level / Total_Capacity) * 100
```

### 4. 
- **Concept:** Inverters (which convert DC power to AC power) do not have a flat efficiency rate. An inverter rated for 40kW might be 98% efficient when handling a 20kW load, but drops drastically to maybe 80% efficiency if it is only handling a 1kW load.
```
Load_Percentage = Current_DC_Power / Inverter_Rated_Max_Power

// Baseline 98% minus low-load penalty minus high-load heat penalty
Efficiency = 0.98 - (0.05 / (Load_Percentage + 0.01)) - (0.01 * Load_Percentage)

AC_Power_Output = Current_DC_Power * Efficiency
```

---

## ⚙️ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/nabilkhondaker/RenewableEnergySim.git
cd RenewableEnergySim
```
### 2. Install Dependencies
```bash
pip install -e .
# or
pip install -r requirements.txt
```
### 3. Run Headless Sim
```bash
python -m src.core.engine
```
### 4. Launch Interative Dashboard
```bash
cd dashboard
streamlit run app.py
```

---

## 📝 Configuration
Edit `config/settings.yaml` to customize simulation parameters such as panel specs, battery limits, location coordinates, and more.
