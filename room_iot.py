import paho.mqtt.client as mqtt
import mysql.connector
import json
from datetime import datetime, timedelta

my_database = mysql.connector.connect(

        host = "localhost",
        user = "root",
        password = "YOUR PASSWORD",
        database = "room_IOT"

)

cursor = my_database.cursor()
def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("Connected to mqtt")
    else:
         print("There is a failure,error code "+str(rc))
def on_message(client, userdata, message):
    #parsing temperature data from mqtt
    payload = message.payload.decode('utf-8')
    print("Received MQTT message ", payload)
    data = json.loads(payload)
    temp = data["Temperature"]

    #we insert data to temprature table
    sql = "INSERT INTO temperature(value,timestamp) VALUE (%s,NOW())"
    val = (temp,)
    cursor.execute(sql, val)
    my_database.commit()

    #calculation minimum, maximum and avarage

    today = datetime.now().strftime('%Y-%m-%d')
    sql = "SELECT MIN(value),MAX(value) FROM temperature WHERE DATE(timestamp)=%s"
    val = (today,)
    cursor.execute(sql,val)
    result = cursor.fetchone()
    min_today = result[0]
    max_today = result[1]

    #calculate avarage of yesterday

    yesterday = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
    sql = "SELECT AVG(value) FROM temperature WHERE DATE(timestamp)= %s"
    val = (yesterday,)
    cursor.execute(sql,val)
    result = cursor.fetchone()
    avg_yesterday = result[0]
    #if yesterday is not ave_yesterday is not None
    if avg_yesterday is not None:
        sql = "INSERT INTO temprature_statistic (avarage_yesterday,current_today,min_today,max_today,avg_today,timestamp) VALUES (%s,%s,%s,%s,%s, NOW())"
        val = (avg_yesterday,temp,min_today,max_today,None)
        cursor.execute(sql,val)
        my_database.commit()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org")
client.subscribe("NAME OF TOPIC")

client.loop_forever()
