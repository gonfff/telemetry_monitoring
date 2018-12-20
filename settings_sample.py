# -*- coding: utf-8 -*-

HOST = 'xxx.xxx.xxx.xxx'
MQTT_PORT = 1883
TELEGRAM_API_TOKEN = 'hash'
EXCH_API_AUTH = ('login', 'password')
EXCH_API_URL = 'api_url'
# USER_BROKER =
# PASSWD_BROKER =
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
