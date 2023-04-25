import network
import socket
from time import sleep
from machine import Pin, I2C
import gc
gc.collect()
from bmp085 import BMP180
from umqtt.robust2 import MQTTClient
import json
mqtt_server = "test.mosquitto.org"
mqtt_port = 1883
client_id = "PUBLISHER NAME"
topic = "NAME OF TOPIC"
ssid = 'KTU guest' #Your network name
password = '200822.092932' #Your WiFi password


i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 1000000)

#Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    
    print('Connecting...')
    sleep(1)
ip = wlan.ifconfig()[0]
print('Connection successful')
print(f'Connected on {ip}')
mqtt_client = MQTTClient(client_id, mqtt_server, mqtt_port)
def connect_mqtt():
    print("Connecting to MQTT broker...")
    mqtt_client.connect()
    print("Connected to MQTT broker")

def main():
    connect_mqtt()
    
    while True:
        try:
            bmp = BMP180(i2c)
            bmp.oversample = 2
            bmp.sealevel = 101325
            temperature = bmp.temperature
            pres = bmp.pressure
            altitude = bmp.altitude
    
            pressure = "{:.2f}".format(pres)
            alti = "{:.2f}".format(altitude)
            

            message = {"Temperature": temperature,"Pressure": pressure}
            print("Sending message:", message)
            payload = json.dumps(message)
            mqtt_client.publish(topic, payload)

            sleep(5)

        except Exception as e:
            print("Error:", e)
            mqtt_client.reconnect()

if __name__ == "__main__":
    main()
