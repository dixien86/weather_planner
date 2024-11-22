# planner/tests.py
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
import requests
from weather_planner.planner.models import Destination

MOCK_API_RESPONSE = {
    "current_weather": {
        "temperature": 15.0,
        "windspeed": 10.0,
        "winddirection": 90,
        "is_day": 1,
        "weathercode": 2,
    }
}


class WeatherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.destination = Destination.objects.create(
            name="Paris", latitude=48.8566, longitude=2.3522
        )

    def tearDown(self):
        self.destination.delete()

    @patch("weather_planner.planner.views.requests.get")
    def test_weather_endpoint(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_API_RESPONSE

        # Call the weather endpoint
        response = self.client.get(
            reverse("destination-weather", kwargs={"pk": self.destination.id})
        )

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("current_weather", response.json())
        self.assertEqual(response.json()["current_weather"]["temperature"], 15.0)

    def test_weather_endpoint_cache(self):
        # Simulate a cached response
        cache_key = f"weather_{self.destination.id}"
        cached_data = {
            "location": self.destination.name,
            "latitude": self.destination.latitude,
            "longitude": self.destination.longitude,
            "current_weather": {
                "temperature": 15.0,
                "windspeed": 10.0,
                "winddirection": 90,
                "is_day": 1,
                "description": "Partly cloudy",
            },
        }
        cache.set(cache_key, cached_data, timeout=3600)

        # Call the weather endpoint
        response = self.client.get(
            reverse("destination-weather", kwargs={"pk": self.destination.id})
        )

        # Assert the cached data is used
        self.assertEqual(response.status_code, 200)
        self.assertIn("current_weather", response.json())
        self.assertEqual(response.json()["current_weather"]["temperature"], 15.0)

    @patch("weather_planner.planner.views.requests.get")
    def test_error_in_request(self, mock_get):
        mock_get.return_value.status_code = 503
        mock_get.return_value.json.return_value = MOCK_API_RESPONSE

        # Call the weather endpoint
        response = self.client.get(
            reverse("destination-weather", kwargs={"pk": self.destination.id})
        )

        # Assert: Check the error message returned
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, {"error": "An unexpected error occurred. Please try again later."})

    @patch("weather_planner.planner.views.requests.get")
    def test_network_error(self, mock_get):
        # Arrange: Make requests.get raise an exception (simulate a network error)
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Call the weather endpoint
        response = self.client.get(
            reverse("destination-weather", kwargs={"pk": self.destination.id})
        )

        # Assert: Verify the error message is returned
        self.assertEqual(response.status_code,503)