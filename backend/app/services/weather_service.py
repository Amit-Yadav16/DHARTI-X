"""
Weather Service for DHARTI-X
Fetches real microclimate data from Open-Meteo for Palghar talukas with verified coordinates.
Includes an extensible adapter interface for future India Meteorological Department (IMD) integration.
"""

import httpx
from typing import Dict, Any, Optional, List

# Verified Coordinates for Palghar District Talukas (No Guessed Coordinates)
PALGHAR_TALUKA_COORDS = {
    "palghar": {"name": "Palghar (City/HQ)", "lat": 19.6967, "lon": 72.7699},
    "dahanu": {"name": "Dahanu", "lat": 19.9705, "lon": 72.7303},
    "talasari": {"name": "Talasari", "lat": 20.1264, "lon": 72.9238},
    "wada": {"name": "Wada", "lat": 19.6547, "lon": 73.1389},
    "jawhar": {"name": "Jawhar", "lat": 19.9056, "lon": 73.2308},
    "mokhada": {"name": "Mokhada", "lat": 19.9367, "lon": 73.3400},
    "vikramgad": {"name": "Vikramgad", "lat": 19.7978, "lon": 73.0970},
    "vasai": {"name": "Vasai", "lat": 19.3919, "lon": 72.8397}
}

class IMDWeatherAdapter:
    """
    Adapter interface reserved for India Meteorological Department (IMD) API / Agromet bulletins.
    Currently returns configuration status to prevent claiming false active integration.
    """
    @classmethod
    def is_configured(cls) -> bool:
        return False

    @classmethod
    def get_source_label(cls) -> str:
        return "IMD Agromet Advisory (Future Integration / Offline)"

class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    async def get_forecast(cls, taluka_name: str) -> Dict[str, Any]:
        key = taluka_name.strip().lower()
        coords_info = PALGHAR_TALUKA_COORDS.get(key)
        
        if not coords_info:
            coords_info = PALGHAR_TALUKA_COORDS["palghar"]

        lat = coords_info["lat"]
        lon = coords_info["lon"]
        display_name = coords_info["name"]

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
            "timezone": "Asia/Kolkata"
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(cls.BASE_URL, params=params)
                if res.status_code == 200:
                    data = res.json()
                    current = data.get("current", {})
                    daily = data.get("daily", {})

                    daily_forecasts: List[Dict[str, Any]] = []
                    dates = daily.get("time", [])
                    t_max = daily.get("temperature_2m_max", [])
                    t_min = daily.get("temperature_2m_min", [])
                    precip = daily.get("precipitation_sum", [])

                    for i in range(min(5, len(dates))):
                        daily_forecasts.append({
                            "date": dates[i],
                            "max_temp": t_max[i] if i < len(t_max) else None,
                            "min_temp": t_min[i] if i < len(t_min) else None,
                            "rain_sum_mm": precip[i] if i < len(precip) else 0.0
                        })

                    rain_val = current.get("precipitation", 0.0)
                    advisory = (
                        f"Rain alert in {display_name}: {rain_val} mm recorded. Delay foliar fertilizer spraying."
                        if rain_val > 5.0
                        else f"Optimal weather in {display_name}. Suitable for weeding and field preparation."
                    )

                    return {
                        "status": "success",
                        "taluka": display_name,
                        "lat": lat,
                        "lon": lon,
                        "temperature_c": current.get("temperature_2m"),
                        "humidity_pct": current.get("relative_humidity_2m"),
                        "precipitation_mm": rain_val,
                        "wind_speed_kmh": current.get("wind_speed_10m"),
                        "daily_forecast": daily_forecasts,
                        "advisory": advisory,
                        "provider": "Open-Meteo Free API (Live)",
                        "imd_adapter_status": "Standby (Adapter Ready)",
                        "is_demo": False
                    }
        except Exception:
            pass

        # Grounded fallback to clearly labelled sample climatology
        return {
            "status": "fallback",
            "taluka": display_name,
            "lat": lat,
            "lon": lon,
            "temperature_c": 28.5,
            "humidity_pct": 78,
            "precipitation_mm": 0.0,
            "wind_speed_kmh": 14.0,
            "daily_forecast": [
                {"date": "Day 1", "max_temp": 30.5, "min_temp": 24.0, "rain_sum_mm": 0.0},
                {"date": "Day 2", "max_temp": 31.0, "min_temp": 24.5, "rain_sum_mm": 1.2},
                {"date": "Day 3", "max_temp": 29.8, "min_temp": 23.8, "rain_sum_mm": 4.5}
            ],
            "advisory": f"Sample Advisory: Standard weather patterns observed for {display_name}.",
            "provider": "Labelled Demo Data (Palghar Climatology)",
            "imd_adapter_status": "Standby (Adapter Ready)",
            "is_demo": True
        }
