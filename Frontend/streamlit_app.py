import os
from urllib.parse import quote

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


API_BASE_URL = "https://end-to-end-time-series-forecasting.onrender.com"

# Page config
st.set_page_config(
    page_title="Time Series Forecasting System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(15, 118, 110, 0.16), transparent 28%),
            radial-gradient(circle at top right, rgba(245, 158, 11, 0.14), transparent 26%),
            linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        color: #0f172a;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }

    h1, h2, h3, h4, p, label, .stMarkdown, .stCaption {
        color: #0f172a !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #0f766e 100%);
        color: white;
        padding: 28px 30px;
        border-radius: 24px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
        margin-bottom: 1.25rem;
    }

    .hero-card h1,
    .hero-card p,
    .hero-card span {
        color: white !important;
        margin: 0;
    }

    .subtle-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: white;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.85rem;
        margin-bottom: 0.85rem;
    }

    .stSidebar {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.22);
    }

    .stSidebar .stSelectbox,
    .stSidebar .stButton {
        color: #0f172a;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.82);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0px 10px 30px rgba(15, 23, 42, 0.07);
        backdrop-filter: blur(8px);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0f766e 0%, #134e4a 48%, #0ea5e9 100%);
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        letter-spacing: 0.2px;
        box-shadow: 0 10px 22px rgba(15, 118, 110, 0.22);
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        filter: saturate(1.06) brightness(1.03);
        box-shadow: 0 12px 26px rgba(15, 118, 110, 0.28);
        border: none;
    }

    .stButton > button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton > button:focus {
        outline: 2px solid rgba(14, 165, 233, 0.35);
        outline-offset: 2px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.16);
        padding: 16px 18px;
        border-radius: 16px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stDataFrame"] {
        background: white;
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.14);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td, thead tr th {
        text-align: center !important;
        vertical-align: middle !important;
    }

    thead tr th {
        background: #e2e8f0 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    tbody tr:nth-child(even) {
        background: #f8fafc;
    }

    .stPlotlyChart {
        background: white;
        border-radius: 14px;
        padding: 0.5rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }

    </style>
""", unsafe_allow_html=True)

# Hero
st.markdown(
    """
    <div class="hero-card">
        <div class="subtle-chip">Sales forecasting dashboard</div>
        <h1>End-to-End Time Series Forecasting System</h1>
        <p>Generate dynamic state-wise sales forecasts using
machine learning and time-series analysis.
</p>
    </div>
    """,
    unsafe_allow_html=True
)


# Sidebar
st.sidebar.header("Forecast Settings")

DEFAULT_STATES = [
    "Alabama",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Florida",
    "Georgia",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Mexico",
    "New York",
    "North Carolina",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Virginia",
    "Vermont",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming"
]


@st.cache_data(ttl=300)
def load_states():
    try:
        response = requests.get(f"{API_BASE_URL}/states", timeout=10)
        response.raise_for_status()
        states = response.json().get("states", [])
        return states if states else DEFAULT_STATES
    except Exception:
        return DEFAULT_STATES


# State dropdown
states = load_states()

selected_state = st.sidebar.selectbox(
    "Select State",
    states
)

forecast_weeks = st.sidebar.slider(
    "Forecast Weeks",
    min_value=4,
    max_value=8,
    value=8
)

# Forecast button
forecast_button = st.sidebar.button(
    "Generate Forecast"
)

st.sidebar.markdown("---")
st.sidebar.caption("Forecasts are generated using the selected state's most recent feature set.")

# API URL
API_URL = f"{API_BASE_URL}/predict/{quote(selected_state, safe='')}"

# Generate forecast
if forecast_button:
    with st.spinner("Generating forecast..."):
        try:
            response = requests.get(API_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            st.error(f"Failed to generate forecast from the API: {exc}")
            st.stop()
        except ValueError:
            st.error("The API returned an invalid JSON response.")
            st.stop()


    # Success message
    st.success(
        f"Forecast generated successfully for {selected_state}"
    )

    # Error handling
    if "error" in data:

        st.error(data["error"])

    else:

        # Best model
        best_model = data["best_model"]

        forecast_data = data[
            "forecast_next_8_weeks"
        ]

        # Convert to dataframe
        forecast_df = pd.DataFrame(
            forecast_data
        )

        forecast_df = forecast_df.rename(
            columns={
                "forecast_date": "Forecast Date",
                "prediction": "Predicted Sales"
            }
        )

        forecast_df.insert(
            0,
            "State Forecast Week",
            [
                f"{selected_state} - Week {idx + 1}"
                for idx in range(len(forecast_df))
            ]
        )

        forecast_df["Predicted Sales"] = forecast_df[
            "Predicted Sales"
        ].round(2)

        forecast_df = forecast_df.head(forecast_weeks)

        forecast_df = forecast_df[
            ["State Forecast Week", "Forecast Date", "Predicted Sales"]
        ]

        styled_forecast_df = forecast_df.style.format(
            {"Predicted Sales": "{:,.2f}"}
        ).set_properties(
            **{"text-align": "center"}
        ).set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("text-align", "center"),
                    ("background-color", "#ede9fe"),
                    ("color", "#1e1b4b"),
                    ("font-weight", "700"),
                    ("padding", "0.8rem 0.6rem")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("text-align", "center"),
                    ("padding", "0.8rem 0.6rem")
                ]
            }
        ])
                # =========================
        # TOP NAVIGATION TABS
        # =========================

        tab1, tab2, tab3 = st.tabs([

            "📊 Dashboard",

            "📋 Forecast Table",

            "📈 Visualization"

        ])

        # =========================
        # DASHBOARD TAB
        # =========================

        with tab1:

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Best Model",
                    best_model,
                    help=f"Selected state: {selected_state}"
                )

            with col2:

                avg_prediction = round(
                    forecast_df[
                        "Predicted Sales"
                    ].mean(),
                    2
                )

                st.metric(
                    "Average Forecast",
                    f"{avg_prediction:,.0f}"
                )

            with col3:

                max_prediction = round(
                    forecast_df[
                        "Predicted Sales"
                    ].max(),
                    2
                )

                st.metric(
                    "Peak Forecast",
                    f"{max_prediction:,.0f}"
                )

            st.markdown("---")

            st.subheader(
                f"📌 Forecast Summary — {selected_state}"
            )

            st.info(
                f"""
                The XGBoost forecasting model predicts
                the next {forecast_weeks} weeks of sales
                for {selected_state} using historical
                time-series features and recursive forecasting.
                """
            )

        # =========================
        # FORECAST TABLE TAB
        # =========================

        with tab2:

            st.subheader(
                f"📋 Forecast Table — {selected_state}"
            )

            st.table(styled_forecast_df)

        # =========================
        # VISUALIZATION TAB
        # =========================

        with tab3:

            st.subheader(
                f"📈 Forecast Visualization — {selected_state}"
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(

                    x=forecast_df[
                        "State Forecast Week"
                    ],

                    y=forecast_df[
                        "Predicted Sales"
                    ],

                    mode="lines+markers",

                    line=dict(
                        color="#0f766e",
                        width=4,
                        shape="spline"
                    ),

                    marker=dict(
                        size=10,
                        color="#f59e0b",
                        line=dict(
                            color="#ffffff",
                            width=1.5
                        )
                    ),

                    hovertemplate=
                    "Week: %{x}<br>"
                    "Sales: %{y:,.2f}"
                    "<extra></extra>"

                )
            )

            fig.update_layout(

                template="plotly_white",

                title=dict(

                    text=
                    f"8 Week Forecast - {selected_state}",

                    font=dict(
                        size=24,
                        color="#0f172a"
                    )

                ),

                xaxis_title="Forecast Week",

                yaxis_title="Predicted Sales",

                hovermode="x unified",

                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                ),

                paper_bgcolor=
                "rgba(0,0,0,0)",

                plot_bgcolor=
                "rgba(255,255,255,1)",

                font=dict(
                    color="#0f172a"
                )

            )

            fig.update_xaxes(

                showgrid=True,

                gridcolor=
                "rgba(148, 163, 184, 0.22)",

                tickangle=-20,

                tickfont=dict(
                    color="#334155"
                )

            )

            fig.update_yaxes(

                showgrid=True,

                gridcolor=
                "rgba(148, 163, 184, 0.22)",

                tickformat=",",

                tickfont=dict(
                    color="#334155"
                )

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# Footer
st.markdown("---")

st.caption(
    "Developed using Flask REST API, Sarima, Prophet, XGBoost, LSTM, Streamlit, and Plotly for interactive time-series forecasting."
)
# Developer credit (separate and styled)
st.markdown(
    "<div style='text-align: right; font-size:12px; color:#475569'>Developed by <strong>Sai Mangena</strong></div>",
    unsafe_allow_html=True,
)