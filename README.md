# 🏔️ Travel-Mate: Intelligent Tourist Safety System (J&K Prototype)

**Travel-Mate** is a specialized safety platform designed for the high-risk, high-altitude terrain of Jammu & Kashmir. It operates on a **Hybrid Architecture** (Online + Offline) to ensure tourist safety even in "Red Zones" with zero connectivity.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Mobile App** | **Flutter** (Dart) | Cross-platform, Offline-first architecture. |
| **Maps & Nav** | **MapmyIndia (Mappls)** | Indigenous maps with government-grade road safety data. |
| **Edge AI** | **TensorFlow Lite** | Offline anomaly detection (Falls/Inactivity) on the phone. |
| **Backend API** | **FastAPI** (Python) | High-performance async API for geospatial logic. |
| **Risk AI** | **Scikit-learn** | Server-side risk scoring (Avalanche/Flood prediction). |
| **Database** | **PostgreSQL + PostGIS** | Spatial database for "Point-in-Polygon" geofencing. |
| **Real-time** | **Firebase (FCM)** | Instant alerts for disasters (Avalanches, Shootings). |

---

## 📂 Project Structure (Monorepo)

We use a feature-first monorepo structure to keep Mobile, Backend, and Data logic in sync.

```text
travel-mate-core/
├── README.md
├── docker-compose.yml           # Database (PostGIS) setup
│
├── 📱 mobile_app/               # FLUTTER (The Tourist Node)
│   ├── assets/
│   │   ├── images/
│   │   └── tflite_models/       # 🧠 [NEW] Store your .tflite files here
│   │       └── movement_classifier.tflite
│   │
│   ├── lib/
│   │   ├── main.dart
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   ├── location_service.dart
│   │   │   │   └── background_service.dart  # Keeps "Silent Guardian" alive when app is closed
│   │   │   └── database/        # Local SQLite (Offline Red Zones)
│   │   │
│   │   └── features/
│   │       ├── map_view/        # Mappls Map Screen
│   │       │
│   │       ├── silent_guardian/ # 🤖 [NEW] THE OFFLINE AI GUARD
│   │       │   ├── logic/
│   │       │   │   ├── sensor_stream.dart   # Listens to Accelerometer (X,Y,Z)
│   │       │   │   └── anomaly_detector.dart # Runs TFLite model on sensor data
│   │       │   └── screens/
│   │       │       └── safety_check_ui.dart # "Are you okay?" countdown popup
│   │       │
│   │       └── sos_emergency/   # SMS/Mesh Fallback Logic
│   │
│   └── pubspec.yaml             # Add: tflite_flutter, sensors_plus, mappls_gl
│
├── ⚙️ backend_engine/          # FASTAPI (The Authority Brain)
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── sos.py
│   │   │       │   └── routes.py # Calls the Smart Route Predictor
│   │   │
│   │   ├── ml_engine/           # 🧠 [NEW] THE RISK PREDICTOR
│   │   │   ├── __init__.py
│   │   │   ├── risk_scorer.py   # The Logic: (Weather + Terrain + History) = Score
│   │   │   └── trained_models/
│   │   │       └── route_risk_model.pkl # Saved Scikit-Learn model
│   │   │
│   │   ├── core/
│   │   │   └── disaster_feed.py # Polls SASE/IMD for Avalanches/Floods
│   │   │
│   │   └── db/                  # PostgreSQL Models
│   │
│   └── requirements.txt         # Add: scikit-learn, pandas, geoalchemy2
│
└── 🗃️ data_pipeline/           # DATA PROCESSING
    ├── raw_data/
    │   ├── red_zones_jk.geojson # Digitized from PDF Page 9
    │   └── accident_history.csv # Fake data for training the Risk Model
    └── scripts/
        └── train_risk_model.py  # Script to generate the .pkl file for Backend

```
---

## 🚀 Key Features & Implementation

### 1. 🤖 The Silent Guardian (Offline Edge AI)
* **What it is:** Detects if a tourist is injured or unconscious in a remote area without internet.
* **How it works:**
    * **Sensors:** App listens to Accelerometer & Gyroscope data via `sensors_plus`.
    * **Model:** Runs `movement_classifier.tflite` locally to classify state (Walking, Stopped, Fall Detected).
    * **Trigger:** If `Location == Red_Zone` AND `Inactivity > 45 mins`, it triggers a local alarm. No reaction = Auto-SOS via SMS.

### 2. 🛡️ Dynamic Geofencing (The "Static" Shield)
* **What it is:** Instant warnings when entering restricted border areas (LoC Buffer) or flood zones.
* **How it works:**
    * **PostGIS:** We store "Red Zones" (e.g., Gurez) as Polygons in the database.
    * **Query:** `ST_Contains(Red_Zone_Polygon, User_GPS)` runs efficiently on the backend.
    * **Delivery:** Triggers a High-Priority Firebase Notification (Overrides Silent Mode).

### 3. 🧠 Smart Route Predictor (Risk AI)
* **What it is:** Recommends the *Safest* route, not just the fastest, based on live hazards.
* **How it works:**
    * **Scikit-learn Model:** Calculates a `Risk_Score` (0-100) for a route.
    * **Inputs:** `Weather_Forecast` (Rain > 50mm) + `Terrain_Data` (Steep Slope) + `History` (Previous Landslides).
    * **Output:** If Score > 70, the API returns a "Warning" payload with the route.

### 4. 🚨 Smart SOS Routing
* **What it is:** Calls the *correct* local police station, not a generic control room.
* **How it works:**
    * Uses the **J&K Intelligence Database**.
    * **Logic:** User in `Baramulla` presses SOS -> App queries local DB -> Calls `Baramulla PCR (01952-234410)` directly.

### 5. 🕸️ J&K Resiliency Mesh (Offline B2B Layer)
* **What it is:** A decentralized "Store-and-Forward" network that functions when cellular towers are down or destroyed.
* **How it works:**
    * **Protocol:** Uses **Bluetooth Low Energy (BLE)** & **Wi-Fi Direct** (via `nearby_connections`) to create a P2P mesh between phones.
    * **The Hop:** If a tourist in a "Red Zone" (No Signal) triggers SOS, the packet hops to nearby devices (Tourist B → Shepherd C → Army Truck).
    * **Gateway Nodes:** The packet travels until it hits a **B2B Node** (Police Tablet/Checkpost) which acts as a "Super Sink" to upload data to the cloud.
    * **Security:** Packets are AES-256 encrypted; intermediate phones relay the message without seeing the content.

---

## 👨‍💻 Developer Notes

1.  **MapmyIndia Keys:**
    * Get your keys from the Mappls Dev Portal.
    * Add them to `mobile_app/lib/core/constants/api_keys.dart` (**Do NOT commit this file**).

2.  **Database Setup:**
    * Run `docker-compose up -d` to start the PostGIS server.
    * Run `python data_pipeline/scripts/seed_db.py` to populate the J&K data (Hospitals, Zones) from our raw CSVs.

3.  **Testing Offline Mode:**
    * Use the Android Emulator "Extended Controls" to simulate "No Signal" while testing the Silent Guardian feature.






    
