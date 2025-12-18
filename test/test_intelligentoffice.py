import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_occupied(self, sensor: Mock):
        pin=11
        sensor.return_value=True
        intelligent_office = IntelligentOffice()
        occupancy=intelligent_office.check_quadrant_occupancy(pin=pin)
        self.assertTrue(occupancy)

    @patch.object(GPIO, "input")
    def test_not_occupied(self, sensor: Mock):
        pin = 13
        sensor.return_value = False
        intelligent_office = IntelligentOffice()
        occupancy = intelligent_office.check_quadrant_occupancy(pin=pin)
        self.assertFalse(occupancy)