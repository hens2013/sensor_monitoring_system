import yaml
from pathlib import Path

CONFIG_FILE_NAME = "config.yml"
CONFIG_FILE_PATH = Path(__file__).with_name(CONFIG_FILE_NAME)
SENSOR_VALUE_RANGE = 100
TIME_DELAY = 1


def load_yaml_file():
    """
    Load and parse a YAML file.
    :param file_path: Path to the YAML file.
    :return: Parsed YAML data.
    """
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {CONFIG_FILE_PATH}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")
