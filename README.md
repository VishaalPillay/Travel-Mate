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
├── docker-compose.yml           # 🐳 Spools up local PostgreSQL + PostGIS database
├── 📱 mobile_app/               # FLUTTER (Tourist Interface)
│   ├── assets/
│   │   ├── tflite_models/       # 🧠 Offline AI models (e.g., movement_classifier.tflite)
│   │   └── data/                # 💾 Pre-loaded JSONs (PCR Numbers, Hospital locations)
│   ├── lib/
│   │   ├── core/                # Global services (Location, Background Service)
│   │   ├── features/
│   │   │   ├── map_view/        # 🗺️ MapmyIndia Hybrid implementation
│   │   │   ├── silent_guardian/ # 🤖 Offline Edge AI logic (Sensor listeners)
│   │   │   ├── sos_emergency/   # 🚨 Smart Routing logic (Routes SOS to local PCR)
│   │   │   └── offline_mode/    # 📶 Mesh/SMS fallback logic
│   └── pubspec.yaml             # Deps: mappls_gl, tflite_flutter, sensors_plus
│
├── ⚙️ backend_engine/          # FASTAPI (Authority Brain)
│   ├── app/
│   │   ├── api/v1/              # Endpoints for SOS, Routes, and Zone Updates
│   │   ├── ml_engine/           # 🧠 Risk Scoring AI (Weather + Terrain logic)
│   │   │   ├── risk_scorer.py   # The Logic: (Weather + Terrain + History) = Score
│   │   │   └── trained_models/  # Saved Scikit-Learn model (.pkl)
│   │   ├── db/                  # Database Models & Schemas
│   │   └── services/            # Geofencing logic ("Is user in Red Zone?")
│   ├── requirements.txt         # Deps: fastapi, uvicorn, geoalchemy2, scikit-learn
│
└── 🗃️ data_pipeline/           # DATA PROCESSING
    ├── raw_data/                # 📄 Extracted data from J&K Intelligence PDF
    └── scripts/                 # 🐍 Scripts to seed DB (CSV -> PostGIS)

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






    
