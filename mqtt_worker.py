import paho.mqtt.client as mqtt
import settings
import time
from db.worker import add_state
PAYLOAD_HEADER = ['cont_id', 'modem_signal', 'temperature', 'location_age',
                  'latitude', 'longitude', 'date_raw', 'time_raw', 'speed',
                  'altitude', 'satellites']

def on_message(client, userdata, message):
    #logger
    print("received message =", str(message.payload.decode("utf-8")))
    payload = str(message.payload.decode("utf-8")).split(',')
    payload = {PAYLOAD_HEADER[i]: val for i, val in enumerate(payload)}
    add_state(payload)


client = mqtt.Client("MQTT_worker")
client.on_message = on_message
print("connecting to broker ", settings.HOST)
client.connect(settings.HOST)  # connect
client.loop_start()  # start loop to process received messages

while True:

    client.subscribe(settings.TOPIC_NAME)  # subscribe
    time.sleep(2)
