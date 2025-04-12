from nest_models.security import verify_faces_against_database
from MqttConnection.mqtt import MQTTConn
import machine
import time
import json
from datetime import datetime

# === MQTT Configuration ===
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
STREAM_TOPIC = "site/security/stream"
ALERT_TOPIC = "system/alert"

# === Buzzer + LED rouge ===
led = machine.Pin(17, machine.Pin.OUT)
buzzer = machine.Pin(18, machine.Pin.OUT)
led.value(0)
buzzer.value(0)

class SecurityStreamHandler(MQTTConn):
    def __init__(self):
        super().__init__(broker=MQTT_BROKER, port=MQTT_PORT)
        self.client.on_message = self.on_message
        self.client.subscribe(STREAM_TOPIC)
        print("🟢 Abonné au topic de stream :", STREAM_TOPIC)

    def trigger_intruder_alert(self):
        msg = f"🚨 INTRUSION DETECTED at {datetime.now().isoformat()}"
        self.client.publish(ALERT_TOPIC, msg.encode())
        print(msg)

        # Activer buzzer et LED pendant 5 secondes
        led.value(1)
        buzzer.value(1)
        time.sleep(5)
        led.value(0)
        buzzer.value(0)

    def on_message(self, client, userdata, msg):
        if msg.topic == STREAM_TOPIC:
            url = msg.payload.decode()
            print("🎥 Stream reçu :", url)

            try:
                # ✅ On utilise ta vraie fonction ici
                matches = verify_faces_against_database(url)

                if not matches:
                    print("❌ Aucun visage reconnu — INTRU détecté.")
                    self.trigger_intruder_alert()
                else:
                    print("✅ Visage(s) reconnu(s). Aucun danger.")
            except Exception as e:
                print("❌ Erreur pendant la vérification :", str(e))

# === Lancement du système ===
if __name__ == "__main__":
    client = SecurityStreamHandler()
    client.loop_forever()