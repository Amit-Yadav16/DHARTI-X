"""
Weather Information Specialist Agent
Fetches and interprets verified Open-Meteo telemetry for Palghar talukas.
Supports 5-day daily forecasts and agricultural risk evaluation.
"""

from typing import Dict, Any
from app.services.weather_service import WeatherService

class WeatherInformationAgent:
    def __init__(self, gemini_service=None):
        self.name = "Weather Information Agent"
        self.gemini = gemini_service
        self.sources = [
            "Open-Meteo Automated Weather API",
            "Palghar District Microclimate Station Network",
            "IMD Agromet Advisory Interface (Standby)"
        ]

    async def get_weather_advisory(self, taluka: str, query: str = "") -> Dict[str, Any]:
        weather = await WeatherService.get_forecast(taluka)
        temp = weather.get("temperature_c", 28.5)
        rain = weather.get("precipitation_mm", 0.0)
        humidity = weather.get("humidity_pct", 78)
        daily = weather.get("daily_forecast", [])

        forecast_summary = ""
        if daily and len(daily) > 0:
            forecast_summary = " 3-day trend: " + ", ".join([f"{d['date']}: {d.get('max_temp', '--')}°C (rain {d.get('rain_sum_mm', 0)}mm)" for d in daily[:3]])

        text = (
            f"Weather update for {weather.get('taluka', taluka)}: "
            f"Temperature is {temp}°C, humidity at {humidity}%, and precipitation is {rain} mm.{forecast_summary} "
        )

        if rain > 5.0:
            text += "Heavy rain detected. Ensure field drainage channels are open and postpone chemical/fertilizer spraying."
        else:
            text += "Weather conditions are favorable for crop maintenance and fertilizer application."

        return {
            "agent": self.name,
            "text": text,
            "telemetry": weather,
            "daily_forecast": daily,
            "sources": self.sources,
            "is_demo": weather.get("is_demo", False),
            "disclaimer": "Forecast is general microclimate data and not a guaranteed field-level measurement."
        }
