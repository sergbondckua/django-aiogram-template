import logging
from datetime import datetime

from aiogram.utils.markdown import text, hbold, quote_html, hcode

import pygismeteo

from robot.models import GisMeteoWeather


class GisMeteoWeatherReport:
    """This class represents a weather report for a specific weather station"""

    def __init__(self):
        self.forecast_request = GisMeteoWeather.objects.filter(active=True)
        self.logger = logging.getLogger(__name__)

    def get_weather_forecast(self) -> dict[int, str]:
        """ Get weather forecast """
        weather_forecast_dict = {}

        #  We iterate over the received data
        for data in self.forecast_request:
            gm = pygismeteo.Gismeteo(token=data.token, lang=data.language)

            #  We get a forecast with a step of 3 hours for the current day
            step3_forecast = gm.step3.by_id(id=data.locality_code, days=1)
            weather_data = self._processing_forecast_data(
                forecast=step3_forecast,
                precipitation_only=data.precipitation_only
            )

            if weather_data:
                forecast_message: str = f"{data.message}\n\n{weather_data}"
                weather_forecast_dict[data.chat_id] = forecast_message

        return weather_forecast_dict

    def _processing_forecast_data(
            self, forecast: list, precipitation_only: bool = False) -> str:
        """Process forecast data and return formatted message"""
        msg = ""
        self.logger.info(
            "Processing forecast data, precipitation only: %s",
            precipitation_only,
        )

        for step in forecast:
            if step.precipitation.type in {1, 2, 3, precipitation_only}:
                time = datetime.fromtimestamp(
                    step.date.unix).time().strftime("%H:%M")
                description = step.description.full
                temperature = step.temperature.air.c
                msg += text(
                    hbold("• " + time + ":"),
                    description,
                    hbold(str(int(temperature)) + "°C"),
                    "\n",
                )

        return msg
