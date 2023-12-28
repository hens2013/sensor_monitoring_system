from sensors.sensors import PressureSensor, TemperatureSensor, HumiditySensor


def test_temperature_sensor_creation():
    """ Test creation of TemperatureSensor with valid parameters """
    sensor = TemperatureSensor(enabled=True, valid_range=(0, 100), unit='C')
    assert sensor.sensor_name == 'TemperatureSensor'
    assert sensor.enabled
    assert sensor.valid_range == (0, 100)
    assert sensor.unit == 'C'


def test_humidity_sensor_creation():
    """ Test creation of HumiditySensor with valid parameters """
    sensor = HumiditySensor(enabled=True, valid_range=(0, 100), unit='%')
    assert sensor.sensor_name == 'HumiditySensor'
    assert sensor.enabled
    assert sensor.valid_range == (0, 100)
    assert sensor.unit == '%'


def test_pressure_sensor_creation():
    """ Test creation of PressureSensor with valid parameters """
    sensor = PressureSensor(enabled=True, valid_range=(0, 1000), unit='Pa')
    assert sensor.sensor_name == 'PressureSensor'
    assert sensor.enabled
    assert sensor.valid_range == (0, 1000)
    assert sensor.unit == 'Pa'
