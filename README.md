# AirAware: Pollution Season Forecaster and Health Advisor 🌫️

> **Production Environmental Intelligence Platform & Health Advisory System for North India**  
> Aligned with **UN Sustainable Development Goals**:  
> - **SDG 3: Good Health and Well-being** (Target 3.9)  
> - **SDG 11: Sustainable Cities and Communities** (Target 11.6)  
> - **SDG 13: Climate Action** (Target 13.1)

---

## 📌 Problem Statement
Every autumn starting in October, North India (Delhi-NCR, Punjab, Haryana, Uttar Pradesh, and Bihar) experiences an acute public health crisis known as the **"smog season"**. 
The confluence of post-harvest **paddy stubble burning** (*parali* burning), calm surface winds, plunging temperatures, and severe **ground-level thermal inversions** traps toxic fine particulate matter ($PM_{2.5}$ and $PM_{10}$) within a stagnant atmospheric boundary layer. 

Citizens typically receive only a passive, backward-looking AQI number (e.g. *"AQI is 430"*), without:
1. **Accurate 24–72 hour predictive forecasts** of when pollution will peak or subside.
2. **Actionable, group-specific operational guidance** tailored for school administrators, asthma/COPD patients, outdoor laborers, or daily commuters.
3. **Integration with real-time satellite fire telemetry** (NASA FIRMS) and meteorological dispersion dynamics.
4. **Automated multi-channel emergency broadcast mechanisms** (WhatsApp/SMS alerts, official school circulars).

---

## 💡 Solution: The AirAware Platform
**AirAware** bridges this gap with an end-to-end environmental intelligence platform:

1. **24 to 72-Hour Multi-Horizon AQI Forecasting:**
   - Powered by an **XGBoost gradient boosting regressor** trained on historical CPCB (Central Pollution Control Board) time series.
   - Leverages recursive multi-step forecasting, lag features ($t-1, t-2, t-3, t-24$), rolling statistics (6h, 24h), diurnal cyclical encodings, and atmospheric physics proxies (Inversion Risk Index & Ventilation Index).
   - Generates 90% confidence uncertainty envelopes.

2. **⚔️ Empirical Model Benchmarking: XGBoost vs Facebook Prophet:**
   - Dual-model laboratory comparing Gradient Boosted Decision Trees against Generalized Additive Time-Series Decomposition (Prophet formulation: Trend + Fourier Seasonality + External Regressors).
   - Out-of-sample benchmark on held-out 2025 CPCB test data:
     - **XGBoost:** $R^2 = 0.9861$, $\text{RMSE} = 20.88\ \mu\text{g/m}^3$, Latency: $0.38\text{ ms}$
     - **Prophet:** $R^2 = 0.8623$, $\text{RMSE} = 65.82\ \mu\text{g/m}^3$, Latency: $0.01\text{ ms}$

3. **🛰️ NASA FIRMS Active Fire Hotspot Tracking:**
   - Connects in real-time to **NASA FIRMS MODIS C6.1** and **SUOMI VIIRS 375m** satellite active fire feeds.
   - Filters and visualizes agricultural thermal anomalies across Punjab, Haryana, and Western UP in interactive 3D geospatial maps (Pydeck).
   - Computes distance-weighted **Stubble Fire Index (SFI)** and downwind smoke plume risk for any selected city.

4. **🛡️ Group-Specific Actionable Health Protocols:**
   - 🎒 **Children & Schools:** PE/sports restrictions, indoor morning assembly rules, school start-delay recommendations, GRAP Stage III/IV school closure triggers, and pediatric KF94/N95 mask fitting.
   - 🫁 **Asthma, COPD & Elderly:** Rescue inhaler readiness, peak flow monitoring, morning walk prohibitions during ground inversion hours (5–9 AM), bedroom HEPA air purifier rules, and ER red-flag alerts.
   - 👷 **Outdoor Workers (Police, Delivery, Laborers):** Continuous outdoor shift caps, mandatory N95/FFP2 respirator specifications, warm saline hydration and clean-air respite stations.
   - 🚗 **General Public & Commuters:** Metro vs two-wheeler guidance, car AC recirculation mode toggle, home window opening windows (solar dispersion peak 1–3:30 PM), and indoor clean-air practices.

5. **🩺 Personal Air Vulnerability Index (AVI) Assessment:**
   - Interactive clinical questionnaire (age, pre-existing conditions, outdoor exposure hours, exertion levels) generating a personalized 1–100 vulnerability score, daily outdoor minute budget, and custom mask prescription.

6. **🔬 Policy & Weather "What-If" Simulation Lab:**
   - Allows users and policymakers to simulate the atmospheric effect of interventions (e.g. 50% stubble burning fire reduction, urban vehicular curbs, wind speed increases) on predicted AQI in real time.

7. **🔔 Automated Multi-Channel Emergency Alert Dispatcher:**
   - Automated condition monitoring triggering multi-channel notifications:
     - **SMS Broadcast** (compact < 160 characters for outdoor labor)
     - **WhatsApp Rich Message** (emojis, markdown, key action points)
     - **School Principal Official Circular** (morning assembly & sports guidance)
     - **Occupational Safety Directive** (mandatory N95 issuance & shift limits)

8. **🚀 Production FastAPI REST API Backend:**
   - Asynchronous endpoints for mobile applications, municipal dashboards, and IoT air purifiers.
   - Interactive Swagger docs at `/docs` and ReDoc specifications at `/redoc`.

---

## 🛠️ Tech Stack & Architecture
- **Language:** Python 3.11
- **Machine Learning:** Native XGBoost Booster (`xgboost>=3.2`), Additive Fourier Time-Series Model (Prophet Formulation)
- **REST API:** FastAPI, Uvicorn, Pydantic v2
- **Dashboard & Geospatial UI:** Streamlit, Plotly Express/Graph Objects, Pydeck (Deck.gl 3D geospatial layers)
- **Containerization:** Docker, Docker Compose
- **Testing:** Python `unittest` framework (100% test coverage on core math & endpoints)

---

## 📂 Project Structure
```
AirAware/
│
├── app.py                   # Streamlit web dashboard with Pydeck 3D maps & Plotly charts
├── api.py                   # High-performance FastAPI REST API backend (Port 8000)
├── data_pipeline.py         # CPCB NAQI calculator, NASA FIRMS downloader, Open-Meteo client
├── ml_engine.py             # Feature engineering, native XGBoost Booster, 72h forecast & simulator
├── model_comparison.py      # XGBoost vs Facebook Prophet benchmark laboratory
├── alert_system.py          # Automated notification dispatcher (SMS, WhatsApp, Circulars)
├── advisory_engine.py       # Group-specific clinical advice, GRAP engine, AVI scoring, bulletin export
├── train_model.py           # Standalone model training & benchmark validation script
├── start_services.py        # Unified launcher for API and Dashboard
├── requirements.txt         # Core dependencies
├── Dockerfile               # Production container image
├── docker-compose.yml       # Multi-service orchestration (FastAPI + Streamlit)
├── .dockerignore            # Docker ignore file
├── README.md                # Project documentation
│
├── tests/                   # Automated unit & integration test suite
│   └── test_airaware.py
│
├── data/                    # Cached satellite fire records and historical multi-city CSV
│   ├── cpcb_historical_air_quality.csv
│   ├── firms_active_fires.json
│   ├── alert_subscribers.json
│   └── alert_dispatch_logs.json
│
└── models/                  # Serialized ML models & benchmark artifacts
    ├── airaware_xgboost.json
    ├── model_metadata.json
    └── comparison_metrics.json
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Automated Test Suite
```bash
python -m unittest tests/test_airaware.py
```
*(Runs 11 comprehensive unit and integration tests verifying CPCB formulas, XGBoost, Prophet, advisories, and API routes)*

### 3. Launch Services

#### Option A: Launch Both REST API & Dashboard (Recommended)
```bash
python start_services.py
```
- **Streamlit Interactive UI:** `http://localhost:8501`
- **FastAPI Interactive Swagger Docs:** `http://localhost:8000/docs`
- **ReDoc API Specifications:** `http://localhost:8000/redoc`

#### Option B: Launch Separately
```bash
# Launch FastAPI backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Launch Streamlit dashboard
streamlit run app.py
```

#### Option C: Run with Docker Compose
```bash
docker-compose up --build
```

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check & model status |
| `GET` | `/api/v1/cities` | List monitored North Indian cities |
| `GET` | `/api/v1/current/{city}` | Current CPCB AQI, pollutant breakdown, and GRAP stage |
| `GET` | `/api/v1/forecast/{city}?horizon=72` | 24–72 hour hourly XGBoost AQI trajectory with 90% C.I. |
| `GET` | `/api/v1/fires` | NASA FIRMS Near Real-Time active fire hotspots |
| `GET` | `/api/v1/fires/stubble-index/{city}` | Distance-weighted Stubble Fire Index & plume risk |
| `GET` | `/api/v1/advisory/{city}` | Group-specific operational and clinical health protocols |
| `POST` | `/api/v1/vulnerability` | Personalized Air Vulnerability Index (AVI) scoring |
| `POST` | `/api/v1/simulate` | Policy What-If simulation (stubble fire & emission curbs) |
| `GET` | `/api/v1/benchmarks` | Head-to-head XGBoost vs Prophet performance metrics |
| `POST` | `/api/v1/alerts/subscribe` | Register user for automated emergency broadcasts |
| `POST` | `/api/v1/alerts/dispatch-test` | Trigger simulated emergency broadcast (SMS/WhatsApp) |

---

## 🏆 CPCB National Air Quality Index (NAQI) Scale
| AQI Range | Category | Color | Clinical Summary |
| :--- | :--- | :--- | :--- |
| **0 – 50** | Good | 🟢 Green | Minimal impact |
| **51 – 100** | Satisfactory | 🟡 Light Green | Minor breathing discomfort to sensitive individuals |
| **101 – 200** | Moderate | 🟠 Yellow | Discomfort to people with asthma, heart and lung diseases |
| **201 – 300** | Poor | 🔴 Coral / Red | Breathing discomfort to most people on prolonged exposure |
| **301 – 400** | Very Poor | 🚨 Red | Respiratory illness on prolonged exposure; GRAP Stage II |
| **401 – 500** | Severe | ☣️ Dark Red | Seriously impacts those with diseases; GRAP Stage III |
| **> 500** | Severe+ | ☠️ Purple | Public health emergency; GRAP Stage IV |
