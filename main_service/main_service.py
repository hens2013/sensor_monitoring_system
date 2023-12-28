
from http import HTTPStatus

import yaml
from typing import List
import asyncio
import httpx
from config.config import load_yaml_file, TIME_DELAY
from config.environment_vars import URL
from sensors.sensors import TemperatureSensor, HumiditySensor, PressureSensor, BaseSensor


def create_sensors_from_yaml() -> List[BaseSensor]:
    """
    function that read the data from the sensor file and creates the objects.
    :return:
    """
    try:
        config = load_yaml_file()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return []

    sensors = []
    for sensor_config in config['sensors']:
        name = sensor_config['name']
        enabled = sensor_config['enabled']
        valid_range = (sensor_config['validRange']['min'], sensor_config['validRange']['max'])
        unit = sensor_config['unit']
        if name == 'TemperatureSensor':
            sensors.append(TemperatureSensor(enabled, valid_range, unit))
        elif name == 'HumiditySensor':
            sensors.append(HumiditySensor(enabled, valid_range, unit))
        elif name == 'PressureSensor':
            sensors.append(PressureSensor(enabled, valid_range, unit))

    return sensors


async def validate_sensor_data(sensor):
    """
    Asynchronously validate sensor data and send a notification if the data is out of the valid range.

    :param sensor: An instance of a sensor object with a method to read its value and properties defining its valid range and name.
    """

    # Read the current value from the sensor
    data = await sensor.read_value()

    # Check if the sensor data is outside the valid range
    if not (sensor.valid_range[0] <= data <= sensor.valid_range[1]):
        # Prepare a message payload for the notification
        message = f"{sensor.sensor_name} value is invalid, value is {data} {sensor.unit}"
        payload = {"message": message}

        try:
            # Send the notification asynchronously using httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(URL, json=payload)
            if response.status_code == HTTPStatus.OK:
                print('Sending notification by email or slack')
        except httpx.HTTPError as e:
            print(f"Error sending notification: {e}")
    else:
        # Log the valid sensor data
        print(f'{sensor.sensor_name} -> {data} {sensor.unit}')


async def main_service_loop(sensors):
    """
    Continuously checks and validates data from a list of sensors.

    :param sensors: A list of sensor objects to be monitored.
    """
    while True:
        # Create a list of tasks for validating each enabled sensor
        tasks = [validate_sensor_data(sensor) for sensor in sensors if sensor.enabled]

        # Run all sensor validation tasks concurrently
        await asyncio.gather(*tasks)

        await asyncio.sleep(TIME_DELAY)


if __name__ == '__main__':
    sensors = create_sensors_from_yaml()
    if sensors:
        enabled_sensors = [sensor.sensor_name for sensor in sensors if sensor.enabled]
        if enabled_sensors:
            print(f"{', '.join(enabled_sensors)} are enabled")
            asyncio.run(main_service_loop(sensors))
        else:
            print('No sensors are enabled')
    else:
        print('Failed to create any sensors')
