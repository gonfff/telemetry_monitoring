HOST = 'xxx.xxx.xxx.xxx'
MQTT_PORT = 1883
# USER =
# PASSWD =
TOPIC_NAME = 'TELEMETRY'

DATABASES = {
    'REDIS': {
        'host': HOST,
        'port': 6379,
        'password': 'password',
        'decode_responses': True
    },
    'POSTGRES': {
        'drivername': 'postgres',
        'host': HOST,
        'port': '5432',
        'username': 'username',
        'password': 'password',
        'database': 'broker'
    }
}
