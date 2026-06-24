# Renewable Energy Sim

**Enterprise Python renewable energy microgrid simulator**

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
