# Nest
# 🧠 Intelligent Telecom Shelter System

Système d’IA complet pour un **shelter télécom autonome**, alliant optimisation énergétique, régulation thermique, sécurité d’accès et surveillance technique.

---

## 🚀 Objectifs

- Maintenir automatiquement une température stable avec une consommation minimale.
- Gérer les accès grâce à une reconnaissance faciale sécurisée.
- Superviser l’état des composants, déclencher des alarmes et mettre en veille en cas de faible activité ou d’anomalie.

---

## 🧩 Composants IA du Système

### 1. 🔥 Modèle de Régression – Contrôle du ventilateur
- **But** : prédire la vitesse optimale du ventilateur (`fan_speed_rpm`) en fonction des conditions internes et externes.
- **Entrées** :
  - `temperature_in`, `temperature_out`
  - `humidity_in`, `humidity_out`
  - `power_consumption`, `hour`, `day_of_week`, `is_weekend`
- **Technos** : `scikit-learn`, `xgboost`

---

### 2. 🧍‍♂️ Reconnaissance Faciale – Sécurité d’accès
- **But** : identifier si la personne est autorisée ou non.
- **Étapes** :
  - Détection de visage : `MTCNN`
  - Extraction des features : `FaceNet`
  - Vérification : comparaison avec base de données d’employés
- **Résultats** : `access_granted` ou `access_denied`
- **Technos** : `OpenCV`, `FaceNet`, `FastAPI`

---

### 3. 🤖 Agent IA – Supervision & Mise en veille
- **But** : assurer la surveillance globale du shelter
  - Met en veille les composants non utilisés
  - Détecte des anomalies : surchauffe, trafic excessif, etc.
  - Gère l’activation des ventilateurs et alarmes
- **Entrées** :
  - `temperature_in`, `power_status`, `network_traffic`, etc.
- **Techno** : `Reinforcement Learning` (Stable-Baselines3), règles hybrides

---

## 📦 Stack technique

| Composant        | Technologie        |
|------------------|-------------------|
| API Backend      | FastAPI           |
| Communication    | MQTT + Redis Pub/Sub |
| IA & Modélisation| scikit-learn, FaceNet, Stable-Baselines3 |
| Détection Visage | MTCNN, OpenCV     |
| Stockage         | Pocketbase, InfluxDB |
| Monitoring       | Grafana, Prometheus |

---

## 📁 Structure du projet
### cmd pour mqtt connection et integration des models 
### models pour les models et les fichers notbooks de creation et traitement de data 
### Backend pocketbase avec system :
🔹 Authentication & Authorization:
✅ JWT (JSON Web Tokens) – Secure login for different roles.
✅ RBAC (Role-Based Access Control) – Defin acces gerant de secteur , ingenieur 

## ⚙️ Fonctionnalités Clés

- 🔄 **Ventilation intelligente** : ajuste la vitesse en temps réel
- 🔐 **Reconnaissance faciale** : gestion des accès sécurisée
- 🌡 **Surveillance intelligente** : détecte surchauffes, pics de trafic
- 💤 **Veille automatique** : désactive les composants non nécessaires
- 🚨 **Alerte en temps réel** : sur anomalies détectées

