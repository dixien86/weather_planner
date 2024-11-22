# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Destination, Schedule, Weather
from .serializers import DestinationSerializer, ScheduleSerializer
import requests
from django.core.cache import cache
from django.conf import settings

from rest_framework.exceptions import APIException
import logging


# Custom Exception
class ThirdPartyAPIException(APIException):
    status_code = 503
    default_detail = "Service Unavailable: Failed to fetch weather data."
    default_code = "service_unavailable"


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    @action(detail=True, methods=['get'])
    def weather(self, request, pk=None):
        destination = self.get_object()
        cache_key = f"weather_{destination.id}"

        # Try to fetch cached weather data
        try:
            cached_weather = cache.get(cache_key)
            if cached_weather:
                return Response(cached_weather)
        except Exception as e:
            logging.error(f"Cache error: {e}")

        # Fetch weather data from API
        try:
            weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={destination.latitude}&longitude={destination.longitude}&current_weather=true"
            response = requests.get(weather_api_url, timeout=10)

            response.raise_for_status()

            # Handle non-200 responses
            if response.status_code != 200:
                logging.error(f"Weather API error: {response.status_code}")
                raise ThirdPartyAPIException()

            # Extract and format weather data
            weather_data = response.json().get("current_weather", {})
            weather_description = settings.WEATHER_CODE_DESCRIPTIONS.get(
                weather_data.get("weathercode", -1), "Unknown weather condition"
            )

            formatted_response = {
                "location": destination.name,
                "latitude": destination.latitude,
                "longitude": destination.longitude,
                "current_weather": {
                    "temperature": weather_data.get("temperature"),
                    "windspeed": weather_data.get("windspeed"),
                    "winddirection": weather_data.get("winddirection"),
                    "is_day": weather_data.get("is_day") == 1,
                    "description": weather_description,
                },
            }

            # Cache the response
            try:
                cache.set(cache_key, formatted_response, timeout=3600)
            except Exception as e:
                logging.error(f"Cache set error: {e}")

            return Response(formatted_response)

        except requests.exceptions.RequestException as e:
            logging.error(f"Weather API request failed: {e}")
            raise ThirdPartyAPIException()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return Response(
                {"error": "An unexpected error occurred. Please try again later."},
                status=500,
            )


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer



