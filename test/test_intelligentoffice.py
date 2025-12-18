import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock

from sympy.physics.units import hours

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


    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_good_air_quality(self, sensor: Mock, buzzer: Mock):
        sensor.return_value=True
        intelligent_office = IntelligentOffice()
        intelligent_office.buzzer_on = True
        intelligent_office.monitor_air_quality()
        self.assertFalse(intelligent_office.buzzer_on)
        buzzer.assert_called_once_with(intelligent_office.BUZZER_PIN,False)

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_bad_air_quality(self, sensor: Mock, buzzer: Mock):
        sensor.return_value = False
        intelligent_office = IntelligentOffice()
        intelligent_office.buzzer_on = False
        intelligent_office.monitor_air_quality()
        self.assertTrue(intelligent_office.buzzer_on)
        buzzer.assert_called_once_with(intelligent_office.BUZZER_PIN, True)

