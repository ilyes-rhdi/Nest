import paho.mqtt.client as mqtt
def on_message():
    return
def MQTTConn():
    # Connexion MQTT
    client = mqtt.Client()
    client.on_message = on_message

    # Connexion au broker MQTT
    client.connect("test.mosquitto.org", 1883, 60)  # ou ton propre broker local

    # S’abonner au topic du ESP32
    client.subscribe("site/sensors/data")  # à adapter selon ton topic MQTT
    return client 