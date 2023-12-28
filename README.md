# sensor_monitoring_system

sensor monitoring system

The system simulates monitoring sensors in real-time and alerts each there is an invalid value if one of the sensors.
The metadata about the sensors is taken from config.yml.
This file includes the data for each sensor if it enables and valid range.
If the main service detects an invalid value, it notify the alert service.
The alert service sends a message to a channel in Slack, if it doesn't work, an email is sent


to activate the system -
* the first two run from the terminal
- python -m venv env
- source env/bin/activate (for linux), .\env_name\Scripts\activate(windows)
- pip install -r requirments.txt
- uvicorn alert_system.app:app --reload  --port 5000 #activate the alert system on local host
- actiave main_service.py

link to video with slack -> https://drive.google.com/file/d/1w9sCAD0qqsgXIW3g5DA56Xhf9Ze9_3UF/view?usp=sharing
link to video with email -> https://drive.google.com/file/d/1ynR3GOGJyHPDNy0btS3YI6tjfQ_lTuFx/view?usp=sharing

