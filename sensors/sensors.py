import random
from config import config

class BaseSensor:
    """
    Base class for different types of sensors.
    """

    def __init__(self, sensor_name, enabled, valid_range, unit):
        if not valid_range[0] < valid_range[1]:
            raise ValueError("Invalid valid_range: min must be less than max")

        self.sensor_name = sensor_name
        self.enabled = enabled
        self.valid_range = valid_range
        self.unit = unit

    def _generate_sensor_value(self):
        """
        Generates a random sensor value for the test
        """
        try:
            return random.randint(self.valid_range[0] - config.SENSOR_VALUE_RANGE,
                                  self.valid_range[1] + config.SENSOR_VALUE_RANGE)
        except ValueError as e:
            raise ValueError(f"Error generating sensor value: {e}")

    async def read_value(self):
        """
        Asynchronously reads the sensor value.
        """
        return self._generate_sensor_value()


class TemperatureSensor(BaseSensor):
    """
    Sensor class for measuring temperature.
    """

    def __init__(self, enabled, valid_range, unit):
        super().__init__(self.__class__.__name__, enabled, valid_range, unit)
        if unit not in ['C', 'F']:
            raise ValueError("Invalid unit for TemperatureSensor: must be 'C' or 'F'")


class HumiditySensor(BaseSensor):
    """
    Sensor class for measuring humidity.
    """

    def __init__(self, enabled, valid_range, unit):
        super().__init__(self.__class__.__name__, enabled, valid_range, unit)
        if unit != '%':
            raise ValueError("Invalid unit for HumiditySensor: must be '%'")


class PressureSensor(BaseSensor):
    """
    Sensor class for measuring pressure.
    """

    def __init__(self, enabled, valid_range, unit):
        super().__init__(self.__class__.__name__, enabled, valid_range, unit)
        if unit not in ['Pa', 'Psi']:
            raise ValueError("Invalid unit for PressureSensor: must be 'Pa' or 'psi'")

