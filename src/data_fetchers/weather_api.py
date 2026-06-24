import requests
import pandas as pd

class WeatherDataFetcher:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_daily_profile(self) -> pd.DataFrame:
        """Fetches hourly solar irradiance and temperature data."""
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "hourly": "temperature_2m,direct_normal_irradiance",
            "timezone": "auto",
            "past_days": 1,
            "forecast_days": 0
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame({
                "time": pd.to_datetime(data["hourly"]["time"]),
                "temperature_c": data["hourly"]["temperature_2m"],
                "irradiance_w_m2": data["hourly"]["direct_normal_irradiance"]
            })
            return df
        except Exception as e:
            print(f"API Error: {e}. Falling back to synthetic data.")
            return self._generate_synthetic_data()

    def _generate_synthetic_data(self) -> pd.DataFrame:
        """Generates a perfect bell curve of solar irradiance for testing."""
        hours = pd.date_range(start="00:00", end="23:00", freq="H")
        import numpy as np
        # Bell curve peaking at noon (hour 12)
        irradiance = 1000 * np.exp(-((np.arange(24) - 12)**2) / 10)
        temp = 15 + 10 * np.exp(-((np.arange(24) - 14)**2) / 20)
        
        return pd.DataFrame({
            "time": hours,
            "temperature_c": temp,
            "irradiance_w_m2": np.maximum(0, irradiance)
        })
