import json
import time
import numpy as np
from sklearn.linear_model import LinearRegression
import paho.mqtt.client as mqtt

# === Dummy trained model coefficients ===
# fan_speed = 4.5 * temp + 1.2 * hum - 3.8 * temp_out + 12
model_coef = np.array([4.5, 1.2, -3.8])
model_intercept = 12

# === MQTT Setup ===
BROKER = "test.mosquitto.org"  # or your IP address if ESP32 is on another device
TOPIC_SUB = "site/sensors/data"
TOPIC_PUB = "site/control/fan_speed"

def predict_fan_speed(temp_in, hum_in, temp_out):
    x = np.array([temp_in, hum_in, temp_out])
    y = np.dot(model_coef, x) + model_intercept
    return int(min(max(y, 0), 100))  # clamp between 0 and 100

# === MQTT Callbacks ===
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("Received:", data)

        temp = float(data.get("temp_in", 0))
        hum = float(data.get("hum_in", 0))
        temp_out = float(data.get("temp_out", 0))

        fan_speed = predict_fan_speed(temp, hum, temp_out)
        print(f"Predicted Fan Speed: {fan_speed}%")

        client.publish(TOPIC_PUB, str(fan_speed))

    except Exception as e:
        print("Error:", e)

# === MQTT Client Setup ===
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)

print("AI MQTT server running...")
client.loop_forever()