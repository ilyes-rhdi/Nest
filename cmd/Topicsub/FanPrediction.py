import pandas as pd
import joblib
import pandas as pd
import numpy as np
import json
from datetime import datetime
from MqttConnection.mqtt import MQTTConn


energy_model = joblib.load(r"C:\Users\PC\OneDrive\Documents\ilyes\projet\nest\fan_model_energy.pkl")
thermal_model = joblib.load(r"C:\Users\PC\OneDrive\Documents\ilyes\projet\nest\fan_model_energy.pkl")

import requests

def process_and_predict(data_json):
    try:
        data = json.loads(data_json)
        data["timestamp"] = datetime.now()
        df = pd.DataFrame([data])

        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.day
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day'] / 31)
        df['day_cos'] = np.cos(2 * np.pi * df['day'] / 31)

        df['delta_temp'] = df['temperature_C'] - df['outside_temperature_C']
        df['delta_humidity'] = df['humidity_percent'] - df['outside_humidity_percent']

        features = df.drop(columns=['timestamp'])
        pred_thermal = thermal_model.predict(features)[0]
        pred_energy = energy_model.predict(features)[0]

        final_fan_speed = 0.4 * pred_thermal + 0.6 * pred_energy

        print(f"✅ Fan speed prédite: {final_fan_speed:.2f} RPM")

        # Ajoute la prédiction au dictionnaire original
        data["fan_speed_rpm"] = round(final_fan_speed, 2)

        # Convertit timestamp en string pour envoi API
        data["timestamp"] = data["timestamp"].isoformat()

        # 🔄 Envoi vers PocketBase
        response = requests.post(
            "http://localhost:8090/api/collections/mesures/records",
            json=data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            print("📤 Donnée insérée dans PocketBase.")
        else:
            print("❌ Erreur d'insertion dans PocketBase:", response.text)

        return final_fan_speed

    except Exception as e:
        print("❌ Erreur de traitement :", e)
        return None

def on_message(client, userdata, msg):
    print(f"\n📥 Message reçu sur le topic {msg.topic}")
    payload = msg.payload.decode()
    print(f"🧾 Payload brut : {payload}")
    fan_speed = process_and_predict(payload)

    if fan_speed is not None:
        # Ici tu peux publier vers un autre topic si tu veux renvoyer la vitesse au ESP32
        client.publish("site/control/fan_speed", json.dumps({"fan_speed_rpm": fan_speed}))

client= MQTTConn()

print("🟢 Client MQTT démarré. En attente de données...")
client.loop_forever()
