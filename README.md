# End-to-End Time Series Forecasting System with REST API

A comprehensive machine learning solution for generating dynamic state-wise sales forecasts using advanced time-series analysis and XGBoost modeling. The system features a professional REST API backend and an interactive Streamlit frontend for real-time predictions.

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-REST_API-green?style=flat-square)
![XGBoost](https://img.shields.io/badge/XGBoost-ML_Model-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## US Dataset & Modeling Approach

- **US Dataset**: The forecasting pipeline is trained and evaluated on a comprehensive US sales dataset (see `data/final_feature_engineered_data.xlsx`) covering 43 US states and historical records from 2019 through 2023. The dataset contains raw sales history plus engineered features used as model inputs.

- **Models Implemented**: Four forecasting approaches were developed and evaluated in the project:
  - **SARIMA** — seasonal ARIMA used as a classical statistical baseline for univariate series.
  - **Prophet** — additive trend/seasonality model from Facebook/Meta for robust seasonality handling.
  - **XGBoost** — gradient-boosted tree regressor using the engineered feature set (production-ready, fast inference).
  - **LSTM** — recurrent neural network capturing longer temporal dependencies in sequences.

- **Automatic Best-Model Selection**: For each state the pipeline evaluates models on validation metrics (e.g., MAE, RMSE, MAPE) and automatically selects the best-performing model — the one with the lowest chosen metric. The API response includes `best_model` so the frontend and users know which model produced the returned forecasts.

---

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Technologies Used](#technologies-used)
- [Developer](#developer)

---

## 🎯 Overview

This project delivers an end-to-end machine learning forecasting pipeline that predicts sales trends across US states. The system combines:

- **Historical Time-Series Data**: Feature-engineered datasets spanning multiple years
- **XGBoost ML Model**: Production-ready gradient boosting model for accurate predictions
- **Flask REST API**: Scalable backend serving forecasting predictions
- **Streamlit Dashboard**: Interactive UI for exploring state-specific forecasts

The solution enables data-driven decision-making by providing 8-week sales forecasts for any US state with dynamic feature engineering and real-time model inference.

---

## 🏗️ Architecture

### System Architecture Overview

The system follows a **4-layer architecture** designed for scalability, maintainability, and production-ready deployment:

```
┌──────────────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER (Streamlit)                     │
│                  Interactive Web Dashboard                        │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ HTTP Requests (Port 8501)
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                      API LAYER (Flask)                           │
│              RESTful Backend with 4 Endpoints                    │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ Load Data & Model
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│              MODEL & INFERENCE LAYER                              │
│       XGBoost Engine + Feature Engineering Pipeline              │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ Read
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                  DATA STORAGE LAYER                               │
│      Excel Files + Serialized Model Files                        │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Interaction**: Select state and forecast weeks in Streamlit
2. **Frontend Request**: Send `GET /predict/<state>` to Flask API
3. **Data Retrieval**: Load state-specific features from Excel
4. **Feature Engineering**: Extract and prepare 9 input features
5. **Model Inference**: XGBoost generates predictions for each week
6. **Dynamic Updates**: Lag values and rolling stats updated sequentially
7. **API Response**: Return JSON with 8-week forecasts and metrics
8. **Visualization**: Render table, metrics, and interactive chart

### Detailed Component Breakdown

For a comprehensive architecture diagram with component interactions, data models, and deployment strategies, see [ARCHITECTURE.md](ARCHITECTURE.md)

---

## ✨ Features

### 🎨 Frontend (Streamlit)
- **Dynamic State Selection**: Load all 43 available US states from API
- **Flexible Forecasting**: Adjust forecast horizon (4-8 weeks) via slider
- **Interactive Visualizations**: Line chart with Plotly showing forecast trends
- **Performance Metrics**: Display best model, average forecast, peak forecast
- **Responsive Design**: Professional gradient-based UI with premium styling
- **Professional Captions**: Informative descriptions for API and developer

### 🔌 REST API (Flask)
- **State Management**: `/states` endpoint returns all available states
- **Health Check**: `/` and `/help` routes for API status and documentation
- **Smart Predictions**: `/predict/<state>` generates 8-week forecasts
- **Case-Insensitive State Matching**: Robust state lookup
- **Date-Anchored Forecasts**: Forecasts start from state's latest data date
- **Dynamic Feature Updates**: Lag values and rolling statistics updated per week

### 🧠 Machine Learning Model
- **XGBoost Gradient Boosting**: Production-ready ensemble model
- **Feature Set**: 9 input features including lags, rolling stats, and temporal info
- **Date-Aware Predictions**: Sequential forecasts with dynamic feature evolution
- **Scalable Inference**: Fast predictions for real-time use cases

### 📊 Data Engineering
- **Feature Engineering**: Lag features (1, 7, 30 days), rolling mean/std
- **State Encoding**: Numerical encoding for categorical state information
- **Temporal Features**: Day-of-week, month, holiday flags
- **Data Quality**: Cleaned historical data spanning 2019-2023

---

## 📁 Project Structure

```
End-to-End Time Series Forecasting System with API/
│
├── api/
│   └── app.py                              # Flask REST API application
│                                           # - Routes: /, /help, /states, /predict/<state>
│                                           # - Model inference engine
│
├── Frontend/
│   └── streamlit_app.py                    # Streamlit interactive dashboard
│                                           # - State selection & forecast weeks slider
│                                           # - Forecast table, metrics, chart
│                                           # - Professional UI/styling
│
├── models/
│   └── xgb_model.pkl                       # Serialized XGBoost model
│                                           # - Pre-trained on historical data
│                                           # - Ready for inference
│
├── data/
│   ├── final_feature_engineered_data.xlsx  # Feature-engineered dataset
│   │                                       # - 43 US states
│   │                                       # - 2019-2023 historical data
│   │                                       # - 9 engineered features
│   │
│   └── Forecasting Case- Study.xlsx        # Original case study data
│
├── Notebooks/
│   └── forecasting.ipynb                   # Jupyter notebook
│                                           # - EDA & data exploration
│                                           # - Feature engineering pipeline
│                                           # - Model training & evaluation
│                                           # - Hyperparameter tuning
│
├── .venv/                                  # Python virtual environment
│
└── README.md                               # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone or Download the Project
```bash
cd "End-to-End Time Series Forecasting System with API"
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install flask pandas numpy joblib scikit-learn xgboost streamlit plotly requests openpyxl
```

Or create a `requirements.txt` file:
```
Flask==2.3.0
pandas==2.0.0
numpy==1.24.0
joblib==1.2.0
scikit-learn==1.2.0
xgboost==1.7.0
streamlit==1.28.0
plotly==5.14.0
requests==2.31.0
openpyxl==3.10.0
```

Then install:
```bash
pip install -r requirements.txt
```

---

## 📖 Usage Guide

### Option 1: Run API and Frontend Separately (Recommended for Development)

**Terminal 1 - Start Flask API:**
```bash
cd api
python app.py
```
The API will run on `http://127.0.0.1:5000`

**Terminal 2 - Start Streamlit Frontend:**
```bash
cd Frontend
streamlit run streamlit_app.py
```
The dashboard will open at `http://localhost:8501`

### Option 2: Quick Start (API Only)
```bash
cd api
python app.py
```

Then visit API endpoints in browser:
- Health check: `http://127.0.0.1:5000/`
- API help: `http://127.0.0.1:5000/help`
- List states: `http://127.0.0.1:5000/states`
- Get forecast (Alabama): `http://127.0.0.1:5000/predict/Alabama`

### Using the Frontend Dashboard

1. **Select State**: Choose from dropdown (all 43 US states)
2. **Set Forecast Horizon**: Use slider to choose 4-8 weeks
3. **Generate Forecast**: Click "Generate Forecast" button
4. **View Results**:
   - **Metrics Card**: Best model, average forecast, peak forecast
   - **Forecast Table**: State-wise week labels and predicted sales by date
   - **Visualization**: Interactive line chart with hover details
5. **Compare States**: Select different states to compare forecasts

---

## 🔗 API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Endpoints

#### 1. **Home Route**
```
GET /
```
**Response:**
```
"Forecasting API Running!"
```

#### 2. **Help Route**
```
GET /help
```
**Response:**
```json
{
  "message": "Available API Routes",
  "routes": {
    "/": "Home Route",
    "/help": "API Documentation Route",
    "/predict/<state>": "Forecast next 8 weeks sales forecast for a state"
  }
}
```

#### 3. **List Available States**
```
GET /states
```
**Response:**
```json
{
  "states": [
    "Alabama",
    "Arizona",
    "Arkansas",
    ...
    "Wyoming"
  ]
}
```

#### 4. **Get Forecast for State**
```
GET /predict/<state>
```

**Parameters:**
- `state` (string, required): State name (case-insensitive)
  - Example: `Alabama`, `california`, `TEXAS`

**Response Success (200):**
```json
{
  "state": "Alabama",
  "best_model": "XGBoost",
  "forecast_next_8_weeks": [
    {
      "forecast_horizon": 1,
      "forecast_date": "2023-12-10",
      "prediction": 179553072.00
    },
    {
      "forecast_horizon": 2,
      "forecast_date": "2023-12-17",
      "prediction": 154248928.00
    },
    ...
  ]
}
```

**Response Error (404):**
```json
{
  "error": "State 'InvalidState' not found"
}
```

### Example API Calls

**Using Python:**
```python
import requests

# Get forecast for California
response = requests.get('http://127.0.0.1:5000/predict/California')
data = response.json()
print(data)
```

**Using cURL:**
```bash
curl http://127.0.0.1:5000/predict/California
```

**Using JavaScript:**
```javascript
fetch('http://127.0.0.1:5000/predict/Texas')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 💻 Technologies Used

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Core programming language |
| **Flask** | 2.3.0 | REST API framework |
| **XGBoost** | 1.7.0 | Machine learning model |
| **Pandas** | 2.0.0 | Data manipulation |
| **NumPy** | 1.24.0 | Numerical computing |
| **Scikit-learn** | 1.2.0 | ML utilities |
| **joblib** | 1.2.0 | Model serialization |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | 1.28.0 | Interactive web UI |
| **Plotly** | 5.14.0 | Interactive visualizations |
| **Pandas** | 2.0.0 | Data handling |
| **Requests** | 2.31.0 | HTTP client |

### Data & Storage
| Format | Purpose |
|--------|---------|
| **XLSX (Excel)** | Feature-engineered data storage |
| **PKL (Pickle)** | Serialized model storage |

---

## 👤 Developer

**Developed by:** Sai Mangena

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

---

## 📞 Support

For questions or issues, please reach out to the developer.

---

## 🎓 Learning Resources

- **XGBoost Documentation**: https://xgboost.readthedocs.io/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Time Series Forecasting**: https://machinelearningmastery.com/time-series-forecasting/

---

**Status:** Production Ready ✅
