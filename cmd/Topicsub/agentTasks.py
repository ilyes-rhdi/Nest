from langchain_google_genai import ChatGoogleGenerativeAI
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json
from datetime import datetime
import streamlit as st
import plotly.express as px
from langchain.agents import Tool, initialize_agent
from MqttConnection.mqtt import MQTTConn


MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
DATA_TOPIC = "site/sensors/data"
POWER_TOPIC = "telecom/command"
ALERT_TOPIC = "system/alert"

# === Actions ===
def reduce_power():
    client.publish(POWER_TOPIC, "sleep")
    print("💤 Mise en veille déclenchée")
    return "Commande envoyée pour mise en veille."

def send_alert(message="🚨 Anomalie détectée dans le système !"):
    client.publish(ALERT_TOPIC, message)
    print(f"🚨 Alerte envoyée : {message}")
    return message

# === Outils de l'agent ===
tools = [
    Tool(
        name="ReducePower",
        func=lambda x: reduce_power(),
        description="Met en veille les appareils inutilisés via MQTT"
    ),
    Tool(
        name="SendAlert",
        func=lambda x: send_alert(),
        description="Envoie une alerte système en cas d'anomalie détectée"
    )
]

# === Agent LangChain ===
openai_api_key = "AIzaSyBYcrA_BKmuQ5o9r_rO9kqLU_quKm6Fs0M" 

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="ta_clé_api_gemini")

# Création de l'agent
agent = initialize_agent(
    tools,
    llm,
    agent_type="zero-shot-react-description",
    verbose=True
)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        flux = payload.get("flux")
        temp_int = payload.get("temperature_C")
        temp_ext = payload.get("outside_temperature_C_")
        hum_int = payload.get("humidity_percent")
        hum_ext = payload.get("outside_humidity_percent")
        power = payload.get("power_consumption_W")

        print("📡 Données reçues :")
        print(f"  📶 Flux : {flux} Hz")
        print(f"  🌡️ Température int/ext : {temp_int}/{temp_ext} °C")
        print(f"  💧 Humidité int/ext : {hum_int}/{hum_ext} %")
        print(f"  ⚡ Conso électrique : {power} W")

        prompt = f"""
        Voici les dernières données du système :
        - Flux des appels : {flux} Hz
        - Température interne : {temp_int} °C
        - Température externe : {temp_ext} °C
        - Humidité interne : {hum_int} %
        - Humidité externe : {hum_ext} %
        - Consommation électrique actuelle : {power} W

        Ta mission est de :
        1. Mettre les appareils en veille si le flux est bas (< 40 Hz) et les conditions sont normales (pas trop chaud, pas trop humide).
        2. Détecter les anomalies comme :
            - Consommation > 200 W
            - Température interne > 70 °C
            - Humidité interne ou externe > 90 %
            - Valeurs manquantes ou incohérentes
        3. Si une anomalie est détectée, utilise 'SendAlert' pour envoyer une alerte.
        """
        agent.run(prompt)

    except Exception as e:
        print(f"Erreur de parsing MQTT : {e}")

client=MQTTConn()

print("🔌 Agent intelligent lancé. En attente de messages MQTT...")
client.loop_forever()
