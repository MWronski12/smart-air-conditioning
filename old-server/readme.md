## Python environment configuration

create venv: `python3 -m venv venv` and activate it: `source venv/bin/activate`

install requirements: `pip install -r requirements.txt`

create `private.py` in `rest_server` directory and set variables:
```python
# Path: private.py

INFLUXDB_HOST = 
INFLUXDB_PORT =
INFLUXDB_TOKEN =
INFLUXDB_ORG =
INFLUXDB_BUCKET =
```

## MQTT configuration

MQTT topic structure:
```
pbl5/<room_id>/<device_id>/sensor: {temperature: float, humidity: float, ...}
pbl5/<room_id>/<device_id>/controller: {fan_speed: int, cooling: bool, ...}
```

## Firebase configuration

To connect to Firebase you have to provide file `pbl5-firebase-admin-key.json` containing private Firebase Admin key.

To connect to Firebase you have to provide file `pbl5-firebase-admin-key.json` containing private Firebase Admin key.