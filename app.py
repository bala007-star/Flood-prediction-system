import streamlit as st
import pandas as pd
import joblib
import requests
import plotly.express as px
import numpy as np
import concurrent.futures

# --- CONFIGURATION ---
# ⚠️ REPLACE WITH YOUR ACTUAL API KEY
API_KEY = "c44c3b849ff5ae9d67c670713b54cd82"  # <--- PASTE YOUR KEY HERE
MODEL_PATH = "C:\\Users\\balan\\Final_Flood_Prediction\\flood_model.pkl"

# --- CONFIG: ALL 38 TAMIL NADU DISTRICTS WITH VULNERABILITY SCORES ---
# Vulnerability (vuln): 0.1 (Safe/Hilly) to 0.9 (High Risk/Coastal)
TN_CITIES = {
    "Ariyalur": {"lat": 11.1401, "lon": 79.0786, "vuln": 0.5},
    "Chengalpattu": {"lat": 12.6841, "lon": 79.9836, "vuln": 0.8},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "vuln": 0.9},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "vuln": 0.4},
    "Cuddalore": {"lat": 11.7480, "lon": 79.7714, "vuln": 0.9},
    "Dharmapuri": {"lat": 12.1211, "lon": 78.1582, "vuln": 0.2},
    "Dindigul": {"lat": 10.3673, "lon": 77.9803, "vuln": 0.3},
    "Erode": {"lat": 11.3410, "lon": 77.7172, "vuln": 0.5},
    "Kallakurichi": {"lat": 11.7384, "lon": 78.9639, "vuln": 0.4},
    "Kancheepuram": {"lat": 12.8342, "lon": 79.7036, "vuln": 0.7},
    "Kanyakumari": {"lat": 8.0883, "lon": 77.5385, "vuln": 0.85},
    "Karur": {"lat": 10.9601, "lon": 78.0766, "vuln": 0.6},
    "Krishnagiri": {"lat": 12.5186, "lon": 78.2137, "vuln": 0.2},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "vuln": 0.6},
    "Mayiladuthurai": {"lat": 11.1018, "lon": 79.6524, "vuln": 0.85},
    "Nagapattinam": {"lat": 10.7656, "lon": 79.8424, "vuln": 0.9},
    "Namakkal": {"lat": 11.2189, "lon": 78.1674, "vuln": 0.4},
    "Nilgiris": {"lat": 11.4102, "lon": 76.6950, "vuln": 0.1},
    "Perambalur": {"lat": 11.2358, "lon": 78.8810, "vuln": 0.3},
    "Pudukkottai": {"lat": 10.3797, "lon": 78.8208, "vuln": 0.6},
    "Ramanathapuram": {"lat": 9.3639, "lon": 78.8395, "vuln": 0.8},
    "Ranipet": {"lat": 12.9273, "lon": 79.3330, "vuln": 0.5},
    "Salem": {"lat": 11.6643, "lon": 78.1460, "vuln": 0.4},
    "Sivaganga": {"lat": 9.8433, "lon": 78.4809, "vuln": 0.4},
    "Tenkasi": {"lat": 8.9594, "lon": 77.3160, "vuln": 0.5},
    "Thanjavur": {"lat": 10.7870, "lon": 79.1378, "vuln": 0.8},
    "Theni": {"lat": 10.0104, "lon": 77.4777, "vuln": 0.3},
    "Thoothukudi": {"lat": 8.7642, "lon": 78.1348, "vuln": 0.8},
    "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047, "vuln": 0.6},
    "Tirunelveli": {"lat": 8.7139, "lon": 77.7567, "vuln": 0.6},
    "Tirupathur": {"lat": 12.4925, "lon": 78.5677, "vuln": 0.3},
    "Tiruppur": {"lat": 11.1085, "lon": 77.3411, "vuln": 0.4},
    "Tiruvallur": {"lat": 13.1430, "lon": 79.9113, "vuln": 0.8},
    "Tiruvannamalai": {"lat": 12.2253, "lon": 79.0747, "vuln": 0.4},
    "Tiruvarur": {"lat": 10.7661, "lon": 79.6378, "vuln": 0.85},
    "Vellore": {"lat": 12.9165, "lon": 79.1325, "vuln": 0.5},
    "Viluppuram": {"lat": 11.9401, "lon": 79.4861, "vuln": 0.7},
    "Virudhunagar": {"lat": 9.5680, "lon": 77.9624, "vuln": 0.3}
}

# --- PAGE SETUP ---
st.set_page_config(page_title="TN Disaster Response System", page_icon="🏛️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] { background-color: #222; border: 1px solid #444; padding: 15px; border-radius: 10px; color: white; }
    div[data-testid="stMetricLabel"] > label { color: #aaa !important; }
    div[data-testid="stMetricValue"] { color: #fff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER FUNCTION ---
def render_header():
    st.markdown("""
        <div style="background-color:#003366;padding:20px;border-radius:10px;text-align:center;border-bottom:5px solid #ffcc00;">
            <h1 style="color:white;margin:0;">🏛️ TAMIL NADU DISASTER RESPONSE SYSTEM</h1>
            <p style="color:#dcdcdc;">State Emergency Operation Centre (SEOC) - AI Division</p>
        </div>
        <div style="background-color:#222;color:#ff4b4b;padding:10px;font-weight:bold;font-family:monospace;">
            🔴 LIVE ALERTS: Heavy rainfall predicted in Coastal Districts. | 📞 HELPLINE: 1070
        </div>
        <br>
    """, unsafe_allow_html=True)

render_header()

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return None

model = load_model()

# --- WEATHER FUNCTIONS ---
def get_live_weather(city):
    """Fetches weather using Coordinates if available"""
    if city in TN_CITIES:
        lat = TN_CITIES[city]["lat"]
        lon = TN_CITIES[city]["lon"]
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return {
                'City': city,
                'Temperature': data['main']['temp'],
                'Rainfall': data.get('rain', {}).get('1h', 0),
                'WindSpeed': data['wind']['speed'],
                'Lat': data['coord']['lat'],
                'Lon': data['coord']['lon']
            }
        return None
    except:
        return None

def get_forecast(city):
    """Fetches 5-day forecast"""
    if city in TN_CITIES:
        lat, lon = TN_CITIES[city]["lat"], TN_CITIES[city]["lon"]
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            forecast_list = []
            for item in data['list']:
                forecast_list.append({
                    "Time": item['dt_txt'],
                    "Rainfall": item.get('rain', {}).get('3h', 0)
                })
            return pd.DataFrame(forecast_list)
    except:
        return None
    return None

# --- OPTIMIZED BATCH PROCESS (MULTI-THREADING) ---
def fetch_city_weather(args):
    """Helper function to fetch data for a single city in a thread"""
    city, coords, sim_city, sim_temp, sim_rain, sim_wind = args
    
    # Logic A: Simulation Override
    if city == sim_city:
        return {
            'City': city, 
            'Temperature': sim_temp, 
            'Rainfall': sim_rain, 
            'WindSpeed': sim_wind, 
            'Lat': coords['lat'], 
            'Lon': coords['lon']
        }
    else:
        return get_live_weather(city)

def get_state_risk_data(sim_city=None, sim_temp=None, sim_rain=None, sim_wind=None):
    """Fetches weather for all cities in PARALLEL (Fast)"""
    results = []
    if not model: return pd.DataFrame()
    
    # Prepare arguments for all cities
    city_args = [
        (city, coords, sim_city, sim_temp, sim_rain, sim_wind) 
        for city, coords in TN_CITIES.items()
    ]
    
    # --- PARALLEL EXECUTION START ---
    # We use 10 threads to fetch data simultaneously
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_city = {executor.submit(fetch_city_weather, arg): arg[0] for arg in city_args}
        
        for future in concurrent.futures.as_completed(future_to_city):
            weather = future.result()
            
            if weather:
                # 1. Base Prediction
                input_df = pd.DataFrame([{
                    'Temperature': weather['Temperature'], 
                    'Rainfall': weather['Rainfall'], 
                    'WindSpeed': weather['WindSpeed']
                }])
                base_risk = model.predict(input_df)[0]
                
                # 2. Vulnerability Logic
                vuln_score = TN_CITIES.get(weather['City'], {}).get("vuln", 0.5)
                
                if weather['Rainfall'] > 50 and vuln_score > 0.7:
                    final_risk = 2
                    reason = "Critical: High Rainfall in Low-Lying Area"
                elif base_risk == 2:
                    final_risk = 2
                    reason = "AI Prediction: Extreme Weather"
                elif base_risk == 1 and vuln_score > 0.6:
                    final_risk = 2
                    reason = "Warning: Moderate Rain in Flood-Prone Zone"
                else:
                    final_risk = base_risk
                    reason = "Standard Prediction"

                # 3. Assign Colors
                if final_risk == 2:
                    color, risk_label = "#EF553B", "High"
                elif final_risk == 1:
                    color, risk_label = "#FFA15A", "Moderate"
                else:
                    color, risk_label = "#00CC96", "Low"

                # 4. Citizen Reports (Purple Dot Check)
                if 'citizen_reports' in st.session_state and weather['City'] in st.session_state['citizen_reports']:
                     report_status = st.session_state['citizen_reports'][weather['City']]
                     if "Flooded" in report_status or "Critical" in report_status:
                         color = "#9c27b0" # Purple
                         risk_label = f"CITIZEN ALERT: {report_status}"
                         reason = "Verified by Ground Report"

                weather['Risk Level'] = risk_label
                weather['Color'] = color
                weather['Reason'] = reason
                results.append(weather)
                
    return pd.DataFrame(results)

# ==============================================================================
# SIDEBAR
# ==============================================================================

# --- SIMULATION MODE ---
st.sidebar.header("🛠️ Simulation Mode")
use_simulation = st.sidebar.checkbox("Enable Manual Override")
sim_city, sim_temp, sim_rain, sim_wind = None, None, None, None

if use_simulation:
    st.sidebar.warning("⚠️ You are controlling the weather manually.")
    sim_city = st.sidebar.selectbox("Select City to Simulate", list(TN_CITIES.keys()))
    sim_temp = st.sidebar.slider("Simulate Temperature (°C)", 15, 45, 28)
    sim_rain = st.sidebar.slider("Simulate Rainfall (mm)", 0, 300, 120)
    sim_wind = st.sidebar.slider("Simulate Wind Speed (m/s)", 0, 50, 15)

# --- CITIZEN REPORTING ---
st.sidebar.markdown("---")
st.sidebar.subheader("📢 Citizen Flood Report")
st.sidebar.caption("Report ground-level conditions.")

report_city = st.sidebar.selectbox("Report Location", list(TN_CITIES.keys()))
report_status = st.sidebar.radio("Current Condition:", ["✅ Safe / Normal", "⚠️ Water Logging (Ankle Deep)", "🌊 Flooded (Knee Deep)", "🚨 Critical (House Entry)"])
uploaded_file = st.sidebar.file_uploader("📸 Upload Live Photo (Required)", type=['jpg', 'png'])

if st.sidebar.button("Broadcast Alert"):
    if uploaded_file is not None:
        if 'citizen_reports' not in st.session_state: st.session_state['citizen_reports'] = {}
        st.session_state['citizen_reports'][report_city] = report_status
        st.sidebar.success(f"✅ Verified & Broadcasted for {report_city}!")
        st.toast(f"🚨 CITIZEN ALERT: {report_status} in {report_city}!", icon="📣")
        st.rerun()
    else:
        st.sidebar.error("⚠️ Please upload a photo to verify.")

# ==============================================================================
# MAIN INTERFACE
# ==============================================================================

# --- MAP SECTION ---
st.subheader("🗺️ Live State-Wide Risk Map")
map_style = st.radio("Select Map View:", ("Light Theme (Default)", "Street Map (Detailed)", "Satellite (Real Imagery)"), horizontal=True)

with st.spinner("Scanning satellite weather data..."):
    map_data = get_state_risk_data(sim_city, sim_temp, sim_rain, sim_wind)

if not map_data.empty:
    if map_style == "Satellite (Real Imagery)":
        mapbox_style = "white-bg"
        mapbox_layers = [{"below": 'traces', "sourcetype": "raster", "sourceattribution": "Esri", "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}]
    elif map_style == "Street Map (Detailed)":
        mapbox_style, mapbox_layers = "open-street-map", []
    else:
        mapbox_style, mapbox_layers = "carto-positron", []

    fig = px.scatter_mapbox(map_data, lat="Lat", lon="Lon", color="Risk Level", size_max=15, zoom=6.5, hover_name="City", hover_data={"Lat": False, "Lon": False, "Temperature": True, "Rainfall": True, "Reason": True}, color_discrete_map={"Low": "#00CC96", "Moderate": "#FFA15A", "High": "#EF553B"}, mapbox_style=mapbox_style, height=600)
    if mapbox_layers: fig.update_layout(mapbox_layers=mapbox_layers)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox=dict(center=dict(lat=11.1271, lon=78.6569), zoom=6.5))
    st.plotly_chart(fig, use_container_width=True)

# --- DEEP DIVE SECTION ---
st.markdown("---")
st.subheader("🔍 Deep Dive Analysis")
col1, col2 = st.columns([1, 2])

with col1:
    target_city = st.selectbox("Select District", list(TN_CITIES.keys()) + ["Other"])
    if target_city == "Other": target_city = st.text_input("Enter City Name")
    analyze_btn = st.button("Analyze Current Risk")

with col2:
    if analyze_btn:
        # Determine Weather
        if use_simulation and target_city == sim_city:
            current_weather = {'Temperature': sim_temp, 'Rainfall': sim_rain, 'WindSpeed': sim_wind}
            st.info(f"🧪 Using SIMULATED Data for {target_city}")
        else:
            current_weather = get_live_weather(target_city)

        if current_weather:
            # Predict
            input_df = pd.DataFrame([{'Temperature': current_weather['Temperature'], 'Rainfall': current_weather['Rainfall'], 'WindSpeed': current_weather['WindSpeed']}])
            base_risk = model.predict(input_df)[0]
            
            # Vulnerability Logic
            vuln_score = TN_CITIES.get(target_city, {}).get("vuln", 0.5)
            if current_weather['Rainfall'] > 50 and vuln_score > 0.7: pred = 2
            elif base_risk == 2: pred = 2
            elif base_risk == 1 and vuln_score > 0.6: pred = 2
            else: pred = base_risk
            
            # Display Cards
            c1, c2, c3 = st.columns(3)
            c1.metric("🌡 Temp", f"{current_weather['Temperature']}°C")
            c2.metric("🌧 Rain (1h)", f"{current_weather['Rainfall']}mm")
            c3.metric("💨 Wind", f"{current_weather['WindSpeed']} m/s")
            
            # Display Alert
            if pred == 2: st.error(f"🚨 **HIGH FLOOD RISK IN {target_city.upper()}!**\n\nImmediate Action Required.")
            elif pred == 1: st.warning(f"⚠️ **MODERATE RISK**.\n\nStay alert.")
            else: st.success(f"✅ **SAFE**.\n\nNo flood risk.")

            # Forecast Graph
            st.markdown("---")
            st.subheader("📅 5-Day Rainfall Forecast Trend")
            if use_simulation and target_city == sim_city:
                dates = pd.date_range(start=pd.Timestamp.now(), periods=5)
                fake_rain = [max(0, x) for x in np.random.normal(loc=sim_rain, scale=10, size=5)]
                forecast_df = pd.DataFrame({"Time": dates, "Rainfall": fake_rain})
                st.caption("⚠️ Simulation Mode: Displaying projected impact.")
            else:
                with st.spinner("Fetching future forecast..."): forecast_df = get_forecast(target_city)

            if forecast_df is not None:
                fig_forecast = px.line(forecast_df, x="Time", y="Rainfall", title=f"Trend for {target_city}", markers=True)
                fig_forecast.update_traces(line_color='#00CC96', line_width=3)
                fig_forecast.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
                st.plotly_chart(fig_forecast, use_container_width=True)
                
            # Report Button
            report_text = f"OFFICIAL REPORT: {target_city} | Status: {pred} | Rain: {current_weather['Rainfall']}mm"
            st.download_button("📄 Download Official Situation Report", report_text, file_name=f"Report_{target_city}.txt")