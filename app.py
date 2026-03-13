# import streamlit as st
# import pandas as pd
# import joblib
# import requests
# import plotly.express as px
# import numpy as np
# import concurrent.futures

# # --- CONFIGURATION ---
# # ⚠️ REPLACE WITH YOUR ACTUAL API KEY
# API_KEY = "c44c3b849ff5ae9d67c670713b54cd82"  # <--- PASTE YOUR KEY HERE
# MODEL_PATH = "C:\\Users\\balan\\Final_Flood_Prediction\\flood_model.pkl"

# # --- CONFIG: ALL 38 TAMIL NADU DISTRICTS WITH VULNERABILITY SCORES ---
# # Vulnerability (vuln): 0.1 (Safe/Hilly) to 0.9 (High Risk/Coastal)
# TN_CITIES = {
#     "Ariyalur": {"lat": 11.1401, "lon": 79.0786, "vuln": 0.5},
#     "Chengalpattu": {"lat": 12.6841, "lon": 79.9836, "vuln": 0.8},
#     "Chennai": {"lat": 13.0827, "lon": 80.2707, "vuln": 0.9},
#     "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "vuln": 0.4},
#     "Cuddalore": {"lat": 11.7480, "lon": 79.7714, "vuln": 0.9},
#     "Dharmapuri": {"lat": 12.1211, "lon": 78.1582, "vuln": 0.2},
#     "Dindigul": {"lat": 10.3673, "lon": 77.9803, "vuln": 0.3},
#     "Erode": {"lat": 11.3410, "lon": 77.7172, "vuln": 0.5},
#     "Kallakurichi": {"lat": 11.7384, "lon": 78.9639, "vuln": 0.4},
#     "Kancheepuram": {"lat": 12.8342, "lon": 79.7036, "vuln": 0.7},
#     "Kanyakumari": {"lat": 8.0883, "lon": 77.5385, "vuln": 0.85},
#     "Karur": {"lat": 10.9601, "lon": 78.0766, "vuln": 0.6},
#     "Krishnagiri": {"lat": 12.5186, "lon": 78.2137, "vuln": 0.2},
#     "Madurai": {"lat": 9.9252, "lon": 78.1198, "vuln": 0.6},
#     "Mayiladuthurai": {"lat": 11.1018, "lon": 79.6524, "vuln": 0.85},
#     "Nagapattinam": {"lat": 10.7656, "lon": 79.8424, "vuln": 0.9},
#     "Namakkal": {"lat": 11.2189, "lon": 78.1674, "vuln": 0.4},
#     "Nilgiris": {"lat": 11.4102, "lon": 76.6950, "vuln": 0.1},
#     "Perambalur": {"lat": 11.2358, "lon": 78.8810, "vuln": 0.3},
#     "Pudukkottai": {"lat": 10.3797, "lon": 78.8208, "vuln": 0.6},
#     "Ramanathapuram": {"lat": 9.3639, "lon": 78.8395, "vuln": 0.8},
#     "Ranipet": {"lat": 12.9273, "lon": 79.3330, "vuln": 0.5},
#     "Salem": {"lat": 11.6643, "lon": 78.1460, "vuln": 0.4},
#     "Sivaganga": {"lat": 9.8433, "lon": 78.4809, "vuln": 0.4},
#     "Tenkasi": {"lat": 8.9594, "lon": 77.3160, "vuln": 0.5},
#     "Thanjavur": {"lat": 10.7870, "lon": 79.1378, "vuln": 0.8},
#     "Theni": {"lat": 10.0104, "lon": 77.4777, "vuln": 0.3},
#     "Thoothukudi": {"lat": 8.7642, "lon": 78.1348, "vuln": 0.8},
#     "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047, "vuln": 0.6},
#     "Tirunelveli": {"lat": 8.7139, "lon": 77.7567, "vuln": 0.6},
#     "Tirupathur": {"lat": 12.4925, "lon": 78.5677, "vuln": 0.3},
#     "Tiruppur": {"lat": 11.1085, "lon": 77.3411, "vuln": 0.4},
#     "Tiruvallur": {"lat": 13.1430, "lon": 79.9113, "vuln": 0.8},
#     "Tiruvannamalai": {"lat": 12.2253, "lon": 79.0747, "vuln": 0.4},
#     "Tiruvarur": {"lat": 10.7661, "lon": 79.6378, "vuln": 0.85},
#     "Vellore": {"lat": 12.9165, "lon": 79.1325, "vuln": 0.5},
#     "Viluppuram": {"lat": 11.9401, "lon": 79.4861, "vuln": 0.7},
#     "Virudhunagar": {"lat": 9.5680, "lon": 77.9624, "vuln": 0.3}
# }

# # --- PAGE SETUP ---
# st.set_page_config(page_title="TN Disaster Response System", page_icon="🏛️", layout="wide")

# # --- CUSTOM CSS ---
# st.markdown("""
#     <style>
#     div[data-testid="stMetric"] { background-color: #222; border: 1px solid #444; padding: 15px; border-radius: 10px; color: white; }
#     div[data-testid="stMetricLabel"] > label { color: #aaa !important; }
#     div[data-testid="stMetricValue"] { color: #fff !important; font-weight: bold; }
#     </style>
#     """, unsafe_allow_html=True)

# # --- HEADER FUNCTION ---
# def render_header():
#     st.markdown("""
#         <div style="background-color:#003366;padding:20px;border-radius:10px;text-align:center;border-bottom:5px solid #ffcc00;">
#             <h1 style="color:white;margin:0;">🏛️ TAMIL NADU DISASTER RESPONSE SYSTEM</h1>
#             <p style="color:#dcdcdc;">State Emergency Operation Centre (SEOC) - AI Division</p>
#         </div>
#         <div style="background-color:#222;color:#ff4b4b;padding:10px;font-weight:bold;font-family:monospace;">
#             🔴 LIVE ALERTS: Heavy rainfall predicted in Coastal Districts. | 📞 HELPLINE: 1070
#         </div>
#         <br>
#     """, unsafe_allow_html=True)

# render_header()

# # --- LOAD MODEL ---
# @st.cache_resource
# def load_model():
#     try:
#         return joblib.load(MODEL_PATH)
#     except FileNotFoundError:
#         return None

# model = load_model()

# # --- WEATHER FUNCTIONS ---
# def get_live_weather(city):
#     """Fetches weather using Coordinates if available"""
#     if city in TN_CITIES:
#         lat = TN_CITIES[city]["lat"]
#         lon = TN_CITIES[city]["lon"]
#         url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
#     else:
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

#     try:
#         response = requests.get(url)
#         data = response.json()
#         if response.status_code == 200:
#             return {
#                 'City': city,
#                 'Temperature': data['main']['temp'],
#                 'Rainfall': data.get('rain', {}).get('1h', 0),
#                 'WindSpeed': data['wind']['speed'],
#                 'Lat': data['coord']['lat'],
#                 'Lon': data['coord']['lon']
#             }
#         return None
#     except:
#         return None

# def get_forecast(city):
#     """Fetches 5-day forecast"""
#     if city in TN_CITIES:
#         lat, lon = TN_CITIES[city]["lat"], TN_CITIES[city]["lon"]
#         url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
#     else:
#         url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        
#     try:
#         response = requests.get(url)
#         data = response.json()
#         if response.status_code == 200:
#             forecast_list = []
#             for item in data['list']:
#                 forecast_list.append({
#                     "Time": item['dt_txt'],
#                     "Rainfall": item.get('rain', {}).get('3h', 0)
#                 })
#             return pd.DataFrame(forecast_list)
#     except:
#         return None
#     return None

# # --- OPTIMIZED BATCH PROCESS (MULTI-THREADING) ---
# def fetch_city_weather(args):
#     """Helper function to fetch data for a single city in a thread"""
#     city, coords, sim_city, sim_temp, sim_rain, sim_wind = args
    
#     # Logic A: Simulation Override
#     if city == sim_city:
#         return {
#             'City': city, 
#             'Temperature': sim_temp, 
#             'Rainfall': sim_rain, 
#             'WindSpeed': sim_wind, 
#             'Lat': coords['lat'], 
#             'Lon': coords['lon']
#         }
#     else:
#         return get_live_weather(city)

# def get_state_risk_data(sim_city=None, sim_temp=None, sim_rain=None, sim_wind=None):
#     """Fetches weather for all cities in PARALLEL (Fast)"""
#     results = []
#     if not model: return pd.DataFrame()
    
#     # Prepare arguments for all cities
#     city_args = [
#         (city, coords, sim_city, sim_temp, sim_rain, sim_wind) 
#         for city, coords in TN_CITIES.items()
#     ]
    
#     # --- PARALLEL EXECUTION START ---
#     # We use 10 threads to fetch data simultaneously
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         # Submit all tasks
#         future_to_city = {executor.submit(fetch_city_weather, arg): arg[0] for arg in city_args}
        
#         for future in concurrent.futures.as_completed(future_to_city):
#             weather = future.result()
            
#             if weather:
#                 # 1. Base Prediction
#                 input_df = pd.DataFrame([{
#                     'Temperature': weather['Temperature'], 
#                     'Rainfall': weather['Rainfall'], 
#                     'WindSpeed': weather['WindSpeed']
#                 }])
#                 base_risk = model.predict(input_df)[0]
                
#                 # 2. Vulnerability Logic
#                 vuln_score = TN_CITIES.get(weather['City'], {}).get("vuln", 0.5)
                
#                 if weather['Rainfall'] > 50 and vuln_score > 0.7:
#                     final_risk = 2
#                     reason = "Critical: High Rainfall in Low-Lying Area"
#                 elif base_risk == 2:
#                     final_risk = 2
#                     reason = "AI Prediction: Extreme Weather"
#                 elif base_risk == 1 and vuln_score > 0.6:
#                     final_risk = 2
#                     reason = "Warning: Moderate Rain in Flood-Prone Zone"
#                 else:
#                     final_risk = base_risk
#                     reason = "Standard Prediction"

#                 # 3. Assign Colors
#                 if final_risk == 2:
#                     color, risk_label = "#EF553B", "High"
#                 elif final_risk == 1:
#                     color, risk_label = "#FFA15A", "Moderate"
#                 else:
#                     color, risk_label = "#00CC96", "Low"

#                 # 4. Citizen Reports (Purple Dot Check)
#                 if 'citizen_reports' in st.session_state and weather['City'] in st.session_state['citizen_reports']:
#                      report_status = st.session_state['citizen_reports'][weather['City']]
#                      if "Flooded" in report_status or "Critical" in report_status:
#                          color = "#9c27b0" # Purple
#                          risk_label = f"CITIZEN ALERT: {report_status}"
#                          reason = "Verified by Ground Report"

#                 weather['Risk Level'] = risk_label
#                 weather['Color'] = color
#                 weather['Reason'] = reason
#                 results.append(weather)
                
#     return pd.DataFrame(results)

# # ==============================================================================
# # SIDEBAR
# # ==============================================================================

# # --- SIMULATION MODE ---
# st.sidebar.header("🛠️ Simulation Mode")
# use_simulation = st.sidebar.checkbox("Enable Manual Override")
# sim_city, sim_temp, sim_rain, sim_wind = None, None, None, None

# if use_simulation:
#     st.sidebar.warning("⚠️ You are controlling the weather manually.")
#     sim_city = st.sidebar.selectbox("Select City to Simulate", list(TN_CITIES.keys()))
#     sim_temp = st.sidebar.slider("Simulate Temperature (°C)", 15, 45, 28)
#     sim_rain = st.sidebar.slider("Simulate Rainfall (mm)", 0, 300, 120)
#     sim_wind = st.sidebar.slider("Simulate Wind Speed (m/s)", 0, 50, 15)

# # --- CITIZEN REPORTING ---
# st.sidebar.markdown("---")
# st.sidebar.subheader("📢 Citizen Flood Report")
# st.sidebar.caption("Report ground-level conditions.")

# report_city = st.sidebar.selectbox("Report Location", list(TN_CITIES.keys()))
# report_status = st.sidebar.radio("Current Condition:", ["✅ Safe / Normal", "⚠️ Water Logging (Ankle Deep)", "🌊 Flooded (Knee Deep)", "🚨 Critical (House Entry)"])
# uploaded_file = st.sidebar.file_uploader("📸 Upload Live Photo (Required)", type=['jpg', 'png'])

# if st.sidebar.button("Broadcast Alert"):
#     if uploaded_file is not None:
#         if 'citizen_reports' not in st.session_state: st.session_state['citizen_reports'] = {}
#         st.session_state['citizen_reports'][report_city] = report_status
#         st.sidebar.success(f"✅ Verified & Broadcasted for {report_city}!")
#         st.toast(f"🚨 CITIZEN ALERT: {report_status} in {report_city}!", icon="📣")
#         st.rerun()
#     else:
#         st.sidebar.error("⚠️ Please upload a photo to verify.")

# # ==============================================================================
# # MAIN INTERFACE
# # ==============================================================================

# # --- MAP SECTION ---
# st.subheader("🗺️ Live State-Wide Risk Map")
# map_style = st.radio("Select Map View:", ("Light Theme (Default)", "Street Map (Detailed)", "Satellite (Real Imagery)"), horizontal=True)

# with st.spinner("Scanning satellite weather data..."):
#     map_data = get_state_risk_data(sim_city, sim_temp, sim_rain, sim_wind)

# if not map_data.empty:
#     if map_style == "Satellite (Real Imagery)":
#         mapbox_style = "white-bg"
#         mapbox_layers = [{"below": 'traces', "sourcetype": "raster", "sourceattribution": "Esri", "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}]
#     elif map_style == "Street Map (Detailed)":
#         mapbox_style, mapbox_layers = "open-street-map", []
#     else:
#         mapbox_style, mapbox_layers = "carto-positron", []

#     fig = px.scatter_mapbox(map_data, lat="Lat", lon="Lon", color="Risk Level", size_max=15, zoom=6.5, hover_name="City", hover_data={"Lat": False, "Lon": False, "Temperature": True, "Rainfall": True, "Reason": True}, color_discrete_map={"Low": "#00CC96", "Moderate": "#FFA15A", "High": "#EF553B"}, mapbox_style=mapbox_style, height=600)
#     if mapbox_layers: fig.update_layout(mapbox_layers=mapbox_layers)
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox=dict(center=dict(lat=11.1271, lon=78.6569), zoom=6.5))
#     st.plotly_chart(fig, use_container_width=True)

# # --- DEEP DIVE SECTION ---
# st.markdown("---")
# st.subheader("🔍 Deep Dive Analysis")
# col1, col2 = st.columns([1, 2])

# with col1:
#     target_city = st.selectbox("Select District", list(TN_CITIES.keys()) + ["Other"])
#     if target_city == "Other": target_city = st.text_input("Enter City Name")
#     analyze_btn = st.button("Analyze Current Risk")

# with col2:
#     if analyze_btn:
#         # Determine Weather
#         if use_simulation and target_city == sim_city:
#             current_weather = {'Temperature': sim_temp, 'Rainfall': sim_rain, 'WindSpeed': sim_wind}
#             st.info(f"🧪 Using SIMULATED Data for {target_city}")
#         else:
#             current_weather = get_live_weather(target_city)

#         if current_weather:
#             # Predict
#             input_df = pd.DataFrame([{'Temperature': current_weather['Temperature'], 'Rainfall': current_weather['Rainfall'], 'WindSpeed': current_weather['WindSpeed']}])
#             base_risk = model.predict(input_df)[0]
            
#             # Vulnerability Logic
#             vuln_score = TN_CITIES.get(target_city, {}).get("vuln", 0.5)
#             if current_weather['Rainfall'] > 50 and vuln_score > 0.7: pred = 2
#             elif base_risk == 2: pred = 2
#             elif base_risk == 1 and vuln_score > 0.6: pred = 2
#             else: pred = base_risk
            
#             # Display Cards
#             c1, c2, c3 = st.columns(3)
#             c1.metric("🌡 Temp", f"{current_weather['Temperature']}°C")
#             c2.metric("🌧 Rain (1h)", f"{current_weather['Rainfall']}mm")
#             c3.metric("💨 Wind", f"{current_weather['WindSpeed']} m/s")
            
#             # Display Alert
#             if pred == 2: st.error(f"🚨 **HIGH FLOOD RISK IN {target_city.upper()}!**\n\nImmediate Action Required.")
#             elif pred == 1: st.warning(f"⚠️ **MODERATE RISK**.\n\nStay alert.")
#             else: st.success(f"✅ **SAFE**.\n\nNo flood risk.")

#             # Forecast Graph
#             st.markdown("---")
#             st.subheader("📅 5-Day Rainfall Forecast Trend")
#             if use_simulation and target_city == sim_city:
#                 dates = pd.date_range(start=pd.Timestamp.now(), periods=5)
#                 fake_rain = [max(0, x) for x in np.random.normal(loc=sim_rain, scale=10, size=5)]
#                 forecast_df = pd.DataFrame({"Time": dates, "Rainfall": fake_rain})
#                 st.caption("⚠️ Simulation Mode: Displaying projected impact.")
#             else:
#                 with st.spinner("Fetching future forecast..."): forecast_df = get_forecast(target_city)

#             if forecast_df is not None:
#                 fig_forecast = px.line(forecast_df, x="Time", y="Rainfall", title=f"Trend for {target_city}", markers=True)
#                 fig_forecast.update_traces(line_color='#00CC96', line_width=3)
#                 fig_forecast.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
#                 st.plotly_chart(fig_forecast, use_container_width=True)
                
#             # Report Button
#             report_text = f"OFFICIAL REPORT: {target_city} | Status: {pred} | Rain: {current_weather['Rainfall']}mm"
#             st.download_button("📄 Download Official Situation Report", report_text, file_name=f"Report_{target_city}.txt")

import streamlit as st
import pandas as pd
import joblib
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import concurrent.futures
from datetime import datetime, timedelta
import random
import json
import io

# ============================================================
# CONFIGURATION
# ============================================================
API_KEY    = "c44c3b849ff5ae9d67c670713b54cd82"
MODEL_PATH = "C:\\Users\\balan\\Final_Flood_Prediction\\flood_model.pkl"

TN_CITIES = {
    "Ariyalur":        {"lat": 11.1401,"lon": 79.0786,"vuln":0.5,"pop":754894,  "elevation":72},
    "Chengalpattu":    {"lat": 12.6841,"lon": 79.9836,"vuln":0.8,"pop":2556244, "elevation":30},
    "Chennai":         {"lat": 13.0827,"lon": 80.2707,"vuln":0.9,"pop":7088000, "elevation":6},
    "Coimbatore":      {"lat": 11.0168,"lon": 76.9558,"vuln":0.4,"pop":3458045, "elevation":411},
    "Cuddalore":       {"lat": 11.7480,"lon": 79.7714,"vuln":0.9,"pop":2605914, "elevation":15},
    "Dharmapuri":      {"lat": 12.1211,"lon": 78.1582,"vuln":0.2,"pop":1506843, "elevation":384},
    "Dindigul":        {"lat": 10.3673,"lon": 77.9803,"vuln":0.3,"pop":2159775, "elevation":273},
    "Erode":           {"lat": 11.3410,"lon": 77.7172,"vuln":0.5,"pop":2251744, "elevation":174},
    "Kallakurichi":    {"lat": 11.7384,"lon": 78.9639,"vuln":0.4,"pop":1370281, "elevation":90},
    "Kancheepuram":    {"lat": 12.8342,"lon": 79.7036,"vuln":0.7,"pop":1166401, "elevation":83},
    "Kanyakumari":     {"lat": 8.0883, "lon": 77.5385,"vuln":0.85,"pop":1870374,"elevation":10},
    "Karur":           {"lat": 10.9601,"lon": 78.0766,"vuln":0.6,"pop":1064493, "elevation":122},
    "Krishnagiri":     {"lat": 12.5186,"lon": 78.2137,"vuln":0.2,"pop":1879809, "elevation":400},
    "Madurai":         {"lat": 9.9252, "lon": 78.1198,"vuln":0.6,"pop":3038252, "elevation":101},
    "Mayiladuthurai":  {"lat": 11.1018,"lon": 79.6524,"vuln":0.85,"pop":918356, "elevation":12},
    "Nagapattinam":    {"lat": 10.7656,"lon": 79.8424,"vuln":0.9,"pop":1616450, "elevation":5},
    "Namakkal":        {"lat": 11.2189,"lon": 78.1674,"vuln":0.4,"pop":1726601, "elevation":168},
    "Nilgiris":        {"lat": 11.4102,"lon": 76.6950,"vuln":0.1,"pop":735394,  "elevation":2240},
    "Perambalur":      {"lat": 11.2358,"lon": 78.8810,"vuln":0.3,"pop":565223,  "elevation":136},
    "Pudukkottai":     {"lat": 10.3797,"lon": 78.8208,"vuln":0.6,"pop":1618345, "elevation":45},
    "Ramanathapuram":  {"lat": 9.3639, "lon": 78.8395,"vuln":0.8,"pop":1353445, "elevation":8},
    "Ranipet":         {"lat": 12.9273,"lon": 79.3330,"vuln":0.5,"pop":1210277, "elevation":100},
    "Salem":           {"lat": 11.6643,"lon": 78.1460,"vuln":0.4,"pop":3482056, "elevation":278},
    "Sivaganga":       {"lat": 9.8433, "lon": 78.4809,"vuln":0.4,"pop":1339101, "elevation":75},
    "Tenkasi":         {"lat": 8.9594, "lon": 77.3160,"vuln":0.5,"pop":1407627, "elevation":110},
    "Thanjavur":       {"lat": 10.7870,"lon": 79.1378,"vuln":0.8,"pop":2402781, "elevation":58},
    "Theni":           {"lat": 10.0104,"lon": 77.4777,"vuln":0.3,"pop":1243630, "elevation":304},
    "Thoothukudi":     {"lat": 8.7642, "lon": 78.1348,"vuln":0.8,"pop":1750176, "elevation":12},
    "Tiruchirappalli": {"lat": 10.7905,"lon": 78.7047,"vuln":0.6,"pop":2722290, "elevation":78},
    "Tirunelveli":     {"lat": 8.7139, "lon": 77.7567,"vuln":0.6,"pop":3077716, "elevation":60},
    "Tirupathur":      {"lat": 12.4925,"lon": 78.5677,"vuln":0.3,"pop":1111812, "elevation":530},
    "Tiruppur":        {"lat": 11.1085,"lon": 77.3411,"vuln":0.4,"pop":2479052, "elevation":303},
    "Tiruvallur":      {"lat": 13.1430,"lon": 79.9113,"vuln":0.8,"pop":3728104, "elevation":18},
    "Tiruvannamalai":  {"lat": 12.2253,"lon": 79.0747,"vuln":0.4,"pop":2464875, "elevation":200},
    "Tiruvarur":       {"lat": 10.7661,"lon": 79.6378,"vuln":0.85,"pop":1264277,"elevation":8},
    "Vellore":         {"lat": 12.9165,"lon": 79.1325,"vuln":0.5,"pop":3936331, "elevation":216},
    "Viluppuram":      {"lat": 11.9401,"lon": 79.4861,"vuln":0.7,"pop":3458243, "elevation":30},
    "Virudhunagar":    {"lat": 9.5680, "lon": 77.9624,"vuln":0.3,"pop":1942288, "elevation":82},
}

RESOURCES = {
    "Boats":         {"Chennai":12,"Cuddalore":8,"Nagapattinam":10,"Thanjavur":6,"Tiruvallur":9,"Tiruvarur":7},
    "Relief Camps":  {"Chennai":5,"Cuddalore":4,"Nagapattinam":6,"Kancheepuram":3,"Chengalpattu":4,"Tiruvarur":5},
    "Helicopters":   {"Chennai":3,"Madurai":2,"Coimbatore":2,"Tiruchirappalli":1},
    "NDRF Teams":    {"Chennai":4,"Cuddalore":3,"Nagapattinam":3,"Thanjavur":2,"Tiruvallur":2},
    "Medical Units": {"Chennai":8,"Madurai":5,"Coimbatore":4,"Salem":3,"Tiruchirappalli":4},
}

EVAC_ROUTES = {
    "Chennai":       ["NH-48 → Vellore","ECR → Puducherry","NH-16 → Tiruvallur"],
    "Nagapattinam":  ["SH-66 → Thanjavur","NH-67 → Tiruvarur","NH-32 → Tiruchy"],
    "Cuddalore":     ["NH-45A → Villupuram","SH-49 → Cuddalore North","NH-532 → Chidambaram"],
    "Tiruvarur":     ["NH-67 → Thanjavur","SH-66 → Nagapattinam","ODR → Papanasam"],
    "Kanyakumari":   ["NH-44 → Tirunelveli","NH-66 → Nagercoil","SH-40 → Tenkasi"],
    "Thanjavur":     ["NH-67 → Trichy","NH-226 → Kumbakonam","SH-72 → Papanasam"],
    "Ramanathapuram":["NH-49 → Madurai","NH-87 → Thoothukudi","SH-33 → Rameswaram"],
    "Thoothukudi":   ["NH-7 → Tirunelveli","NH-49 → Ramanathapuram","SH-25 → Kayalpatnam"],
    "Chengalpattu":  ["NH-32 → Chennai","NH-45 → Tindivanam","SH-130 → Mahabalipuram"],
    "Mayiladuthurai":["NH-32 → Nagapattinam","SH-64 → Sirkazhi","NH-226 → Kumbakonam"],
}

HISTORICAL_FLOODS = [
    {"Year":2015,"Deaths":422,"Districts":25,"Rainfall_mm":1218,"Damage_Cr":8481,"Event":"Chennai Mega Floods"},
    {"Year":2018,"Deaths":34, "Districts":12,"Rainfall_mm":640, "Damage_Cr":1200,"Event":"Northeast Monsoon"},
    {"Year":2019,"Deaths":18, "Districts":8, "Rainfall_mm":420, "Damage_Cr":630, "Event":"Cyclone Fani Impact"},
    {"Year":2021,"Deaths":46, "Districts":15,"Rainfall_mm":780, "Damage_Cr":2100,"Event":"Cyclone Nivar Aftermath"},
    {"Year":2022,"Deaths":12, "Districts":6, "Rainfall_mm":390, "Damage_Cr":480, "Event":"Northeast Monsoon"},
    {"Year":2023,"Deaths":29, "Districts":11,"Rainfall_mm":560, "Damage_Cr":950, "Event":"Cyclone Michaung"},
    {"Year":2024,"Deaths":8,  "Districts":4, "Rainfall_mm":310, "Damage_Cr":275, "Event":"Early Monsoon Surge"},
]

RELIEF_CAMPS_DATA = {
    "Chennai-Camp-A":    {"district":"Chennai",      "capacity":500,"occupied":312,"food_days":4,"water_kl":12,"medicine_kits":80, "status":"Active"},
    "Chennai-Camp-B":    {"district":"Chennai",      "capacity":300,"occupied":289,"food_days":2,"water_kl":6, "medicine_kits":30, "status":"Critical"},
    "Nagapattinam-C1":   {"district":"Nagapattinam", "capacity":400,"occupied":180,"food_days":6,"water_kl":18,"medicine_kits":100,"status":"Active"},
    "Nagapattinam-C2":   {"district":"Nagapattinam", "capacity":250,"occupied":241,"food_days":1,"water_kl":3, "medicine_kits":15, "status":"Critical"},
    "Cuddalore-C1":      {"district":"Cuddalore",    "capacity":350,"occupied":210,"food_days":5,"water_kl":14,"medicine_kits":70, "status":"Active"},
    "Thanjavur-C1":      {"district":"Thanjavur",    "capacity":300,"occupied":95, "food_days":8,"water_kl":22,"medicine_kits":90, "status":"Active"},
    "Tiruvarur-C1":      {"district":"Tiruvarur",    "capacity":200,"occupied":188,"food_days":2,"water_kl":4, "medicine_kits":20, "status":"Critical"},
    "Chengalpattu-C1":   {"district":"Chengalpattu", "capacity":400,"occupied":130,"food_days":7,"water_kl":20,"medicine_kits":85, "status":"Active"},
    "Kancheepuram-C1":   {"district":"Kancheepuram", "capacity":250,"occupied":75, "food_days":9,"water_kl":25,"medicine_kits":60, "status":"Standby"},
    "Tiruvallur-C1":     {"district":"Tiruvallur",   "capacity":350,"occupied":290,"food_days":3,"water_kl":8, "medicine_kits":45, "status":"Active"},
}

VEHICLES = {
    "TN-BOAT-001": {"type":"Rescue Boat",  "district":"Chennai",      "driver":"Rajan K",     "status":"Deployed","fuel":65,"last_update":"08:42"},
    "TN-BOAT-002": {"type":"Rescue Boat",  "district":"Nagapattinam", "driver":"Selvam P",    "status":"Deployed","fuel":40,"last_update":"09:15"},
    "TN-AMB-011":  {"type":"Ambulance",    "district":"Chennai",      "driver":"Dr.Priya R",  "status":"En Route","fuel":80,"last_update":"09:22"},
    "TN-AMB-022":  {"type":"Ambulance",    "district":"Cuddalore",    "driver":"Anand S",     "status":"Available","fuel":90,"last_update":"07:30"},
    "TN-TRK-031":  {"type":"Supply Truck", "district":"Thanjavur",    "driver":"Murugan L",   "status":"Deployed","fuel":55,"last_update":"08:55"},
    "TN-TRK-032":  {"type":"Supply Truck", "district":"Tiruvarur",    "driver":"Vijay D",     "status":"Available","fuel":72,"last_update":"09:00"},
    "TN-HLP-001":  {"type":"Helicopter",   "district":"Chennai",      "driver":"Capt.Raj V",  "status":"Deployed","fuel":48,"last_update":"09:30"},
    "TN-HLP-002":  {"type":"Helicopter",   "district":"Madurai",      "driver":"Capt.Meena G","status":"Maintenance","fuel":20,"last_update":"06:00"},
    "TN-JCBS-041": {"type":"JCB/Excavator","district":"Chengalpattu", "driver":"Kannan T",    "status":"Available","fuel":85,"last_update":"08:10"},
    "TN-BOAT-003": {"type":"Rescue Boat",  "district":"Tiruvarur",    "driver":"Senthil M",   "status":"Deployed","fuel":30,"last_update":"09:18"},
}

SUPPLY_CHAIN = {
    "Food Packets":   {"total":50000,"dispatched":32000,"delivered":28500,"unit":"pkt", "reorder_at":5000},
    "Drinking Water": {"total":1200, "dispatched":780,  "delivered":720,  "unit":"kL",  "reorder_at":200},
    "Medicine Kits":  {"total":8000, "dispatched":4200, "delivered":3900, "unit":"kit", "reorder_at":1000},
    "Tarpaulins":     {"total":15000,"dispatched":9800, "delivered":9200, "unit":"nos", "reorder_at":2000},
    "Life Jackets":   {"total":3000, "dispatched":2100, "delivered":2000, "unit":"nos", "reorder_at":500},
    "Blankets":       {"total":20000,"dispatched":12000,"delivered":11500,"unit":"nos", "reorder_at":3000},
    "Generators":     {"total":120,  "dispatched":78,   "delivered":72,   "unit":"nos", "reorder_at":20},
    "Fuel (Diesel)":  {"total":80000,"dispatched":52000,"delivered":49000,"unit":"L",   "reorder_at":10000},
}

RIVER_GAUGES = {
    "Cauvery @ Tiruchy":     {"current":12.4,"danger":14.0,"warning":12.0,"normal":8.0, "district":"Tiruchirappalli","trend":"rising"},
    "Cauvery @ Thanjavur":   {"current":10.8,"danger":13.5,"warning":11.0,"normal":7.5, "district":"Thanjavur",     "trend":"stable"},
    "Vaigai @ Madurai":      {"current":6.2, "danger":10.0,"warning":8.0, "normal":4.0, "district":"Madurai",       "trend":"stable"},
    "Tamirabarani @ TNV":    {"current":8.9, "danger":11.0,"warning":9.0, "normal":5.0, "district":"Tirunelveli",   "trend":"rising"},
    "Palar @ Vellore":       {"current":5.1, "danger":9.0, "warning":7.0, "normal":3.0, "district":"Vellore",       "trend":"falling"},
    "Adyar @ Chennai":       {"current":3.8, "danger":6.0, "warning":4.5, "normal":2.0, "district":"Chennai",       "trend":"rising"},
    "Cooum @ Chennai":       {"current":4.2, "danger":5.5, "warning":4.0, "normal":1.5, "district":"Chennai",       "trend":"rising"},
    "Kollidam @ Nagapattinam":{"current":11.6,"danger":13.0,"warning":11.0,"normal":7.0,"district":"Nagapattinam", "trend":"rising"},
}

COMM_LOG_SEED = [
    {"time":"09:31","from":"Chennai SEOC","to":"Nagapattinam Collector","channel":"Phone","priority":"HIGH",  "message":"Requesting 2 additional NDRF teams. River Kollidam rising. Confirm ETA.","status":"Acknowledged"},
    {"time":"09:28","from":"Tiruvarur Collector","to":"SEOC Control","channel":"Radio", "priority":"HIGH",  "message":"Camp C1 at 94% capacity. Request overflow arrangement immediately.","status":"Pending"},
    {"time":"09:15","from":"SEOC Control","to":"All Districts","channel":"Broadcast","priority":"MEDIUM","message":"Orange alert upgraded to Red for delta districts. All DCs to activate EOCs.","status":"Sent"},
    {"time":"09:05","from":"Thanjavur DC","to":"SEOC Control","channel":"Email", "priority":"LOW",   "message":"Cauvery tributary overflow at Papanasam block. Deploying local response.","status":"Acknowledged"},
    {"time":"08:52","from":"Cuddalore DC","to":"Medical Dept","channel":"Phone", "priority":"HIGH",  "message":"Snake bite cases increasing post-flood. Need anti-venom stock urgently.","status":"Acknowledged"},
    {"time":"08:40","from":"SEOC Control","to":"Chennai Collector","channel":"SMS",   "priority":"MEDIUM","message":"Adyar river at 3.8m. Prepare low-lying area evacuation plans. Report by 10:00.","status":"Sent"},
    {"time":"08:22","from":"Nagapattinam Collector","to":"SEOC Control","channel":"Radio", "priority":"HIGH",  "message":"Fishing community (1,200 persons) stranded at Velankanni. Helicopter requested.","status":"Escalated"},
    {"time":"08:10","from":"SEOC Control","to":"All Districts","channel":"Broadcast","priority":"LOW",   "message":"NDRF battalion 6 arriving Chennai at 11:00. Districts coordinate pickup.","status":"Sent"},
]

STAFF_SHIFTS = {
    "Morning (06:00–14:00)": [
        {"name":"Suresh Kumar",   "role":"Incident Commander", "district":"SEOC HQ",       "contact":"94445-11001","status":"On Duty"},
        {"name":"Priya Rajan",    "role":"Field Coordinator",  "district":"Chennai",        "contact":"94445-11002","status":"On Duty"},
        {"name":"Anbu Selvan",    "role":"Relief Coordinator", "district":"Nagapattinam",   "contact":"94445-11003","status":"On Duty"},
        {"name":"Geetha Devi",    "role":"Medical Officer",    "district":"Cuddalore",      "contact":"94445-11004","status":"On Duty"},
        {"name":"Ramesh Babu",    "role":"Logistics Officer",  "district":"Thanjavur",      "contact":"94445-11005","status":"On Duty"},
    ],
    "Afternoon (14:00–22:00)": [
        {"name":"Kavitha Nair",   "role":"Incident Commander", "district":"SEOC HQ",        "contact":"94445-11006","status":"Standby"},
        {"name":"Mohan Das",      "role":"Field Coordinator",  "district":"Tiruvarur",      "contact":"94445-11007","status":"Standby"},
        {"name":"Saravanan P",    "role":"Relief Coordinator", "district":"Chengalpattu",   "contact":"94445-11008","status":"Standby"},
        {"name":"Lakshmi S",      "role":"Medical Officer",    "district":"Kancheepuram",   "contact":"94445-11009","status":"Standby"},
        {"name":"Vignesh T",      "role":"Logistics Officer",  "district":"Tiruvallur",     "contact":"94445-11010","status":"Standby"},
    ],
    "Night (22:00–06:00)": [
        {"name":"Rajendran M",    "role":"Incident Commander", "district":"SEOC HQ",        "contact":"94445-11011","status":"Off Duty"},
        {"name":"Deepa Krishnan", "role":"Field Coordinator",  "district":"Chennai",        "contact":"94445-11012","status":"Off Duty"},
        {"name":"Balu Murugan",   "role":"Relief Coordinator", "district":"Nagapattinam",   "contact":"94445-11013","status":"Off Duty"},
        {"name":"Saroja V",       "role":"Medical Officer",    "district":"Madurai",        "contact":"94445-11014","status":"Off Duty"},
        {"name":"Karthik R",      "role":"Logistics Officer",  "district":"Salem",          "contact":"94445-11015","status":"Off Duty"},
    ],
}

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="TN SEOC — Disaster Response System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;800&display=swap');

:root {
  --bg:       #050a0f;
  --bg2:      #0a1520;
  --bgc:      #0d1e2e;
  --bgc2:     #071525;
  --bdr:      #1a3a5c;
  --bdrb:     #0e7fc2;
  --blue:     #00b4ff;
  --cyan:     #00ffd5;
  --amber:    #ffb300;
  --red:      #ff3737;
  --green:    #00e676;
  --purple:   #9c27b0;
  --txt:      #e8f4fd;
  --txt2:     #7fb3d3;
  --mono:     #5dc8ff;
  --glow:     0 0 20px rgba(0,180,255,0.15);
  --fd:       'Exo 2', sans-serif;
  --fm:       'Share Tech Mono', monospace;
  --fu:       'Rajdhani', sans-serif;
}
html,body,.stApp{background:var(--bg)!important;color:var(--txt);font-family:var(--fu);}
.stApp::before{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,180,255,0.012) 2px,rgba(0,180,255,0.012) 4px);pointer-events:none;z-index:999;}
h1,h2,h3{font-family:var(--fd);letter-spacing:.05em;}
code,pre{font-family:var(--fm);color:var(--mono);}
.block-container{padding:1rem 2rem!important;max-width:100%!important;}

/* Sidebar */
[data-testid="stSidebar"]{background:var(--bgc2)!important;border-right:1px solid var(--bdr)!important;}
[data-testid="stSidebar"] *{color:var(--txt)!important;}

/* Buttons */
.stButton>button{background:linear-gradient(135deg,#003a6e,#005fa3)!important;color:var(--cyan)!important;border:1px solid var(--bdrb)!important;border-radius:4px!important;font-family:var(--fd)!important;font-weight:700!important;letter-spacing:.1em!important;text-transform:uppercase!important;transition:all .2s!important;box-shadow:0 0 12px rgba(0,180,255,.2)!important;}
.stButton>button:hover{background:linear-gradient(135deg,#005fa3,#0080d4)!important;box-shadow:0 0 20px rgba(0,180,255,.4)!important;transform:translateY(-1px)!important;}

/* Metrics */
[data-testid="stMetric"]{background:var(--bgc)!important;border:1px solid var(--bdr)!important;border-left:3px solid var(--blue)!important;border-radius:6px!important;padding:16px!important;box-shadow:var(--glow)!important;}
[data-testid="stMetricLabel"]{color:var(--txt2)!important;font-family:var(--fm)!important;font-size:.75rem!important;}
[data-testid="stMetricValue"]{color:var(--cyan)!important;font-family:var(--fd)!important;font-weight:800!important;}

/* Tabs */
[data-testid="stTabs"] button{font-family:var(--fd)!important;font-weight:700!important;letter-spacing:.06em!important;text-transform:uppercase!important;color:var(--txt2)!important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:var(--cyan)!important;border-bottom:2px solid var(--cyan)!important;}
[data-baseweb="tab-panel"]{background:transparent!important;border:1px solid var(--bdr)!important;border-top:none!important;border-radius:0 0 8px 8px!important;padding:20px!important;}

/* Inputs */
[data-baseweb="select"]>div,[data-baseweb="input"]>div,[data-baseweb="textarea"]>div{background:var(--bgc)!important;border-color:var(--bdr)!important;color:var(--txt)!important;}
[data-baseweb="slider"] [role="slider"]{background:var(--blue)!important;}
[data-testid="stExpander"]{background:var(--bgc)!important;border:1px solid var(--bdr)!important;border-radius:6px!important;}
hr{border-color:var(--bdr)!important;}
[data-testid="stDataFrame"]{border:1px solid var(--bdr)!important;}

/* KPI strip */
.kpi-strip{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 20px 0;}
.kpi-box{flex:1;min-width:130px;background:var(--bgc);border:1px solid var(--bdr);border-top:3px solid var(--blue);border-radius:6px;padding:14px 16px;text-align:center;}
.kpi-box.red{border-top-color:var(--red);}
.kpi-box.amber{border-top-color:var(--amber);}
.kpi-box.green{border-top-color:var(--green);}
.kpi-box.cyan{border-top-color:var(--cyan);}
.kpi-box.purple{border-top-color:var(--purple);}
.kpi-val{font-family:var(--fd);font-size:1.9rem;font-weight:800;color:var(--txt);line-height:1;}
.kpi-lbl{font-family:var(--fm);font-size:.62rem;color:var(--txt2);text-transform:uppercase;letter-spacing:.12em;margin-top:4px;}

/* Ticker */
.ticker-wrap{background:rgba(255,55,55,.08);border:1px solid rgba(255,55,55,.35);border-radius:4px;padding:8px 16px;font-family:var(--fm);font-size:.73rem;color:var(--red);overflow:hidden;white-space:nowrap;margin:8px 0;animation:pborder 2s infinite;}
@keyframes pborder{0%,100%{border-color:rgba(255,55,55,.35);}50%{border-color:rgba(255,55,55,.85);}}

/* Cards */
.cmd-card{background:var(--bgc);border:1px solid var(--bdr);border-radius:8px;padding:18px;box-shadow:var(--glow);margin-bottom:14px;}
.cmd-hdr{font-family:var(--fm);font-size:.67rem;color:var(--mono);text-transform:uppercase;letter-spacing:.15em;margin-bottom:8px;border-bottom:1px solid var(--bdr);padding-bottom:6px;}

/* Header */
.hdr{background:linear-gradient(135deg,#03090f,#061624 50%,#031020);border:1px solid var(--bdr);border-left:4px solid var(--blue);border-radius:8px;padding:22px 30px;margin-bottom:16px;position:relative;overflow:hidden;}
.hdr::after{content:'SEOC';position:absolute;right:24px;top:50%;transform:translateY(-50%);font-family:var(--fd);font-size:5rem;font-weight:800;color:rgba(0,180,255,.04);letter-spacing:.2em;pointer-events:none;}
.hdr-title{font-family:var(--fd);font-size:1.7rem;font-weight:800;color:var(--txt);letter-spacing:.08em;margin:0;}
.hdr-sub{font-family:var(--fm);font-size:.7rem;color:var(--txt2);margin-top:4px;letter-spacing:.14em;text-transform:uppercase;}
.hdr-status{display:inline-block;background:rgba(0,230,118,.1);border:1px solid rgba(0,230,118,.35);border-radius:3px;padding:2px 10px;font-family:var(--fm);font-size:.63rem;color:var(--green);margin-top:8px;letter-spacing:.12em;text-transform:uppercase;}

/* Log entries */
.log-e{font-family:var(--fm);font-size:.7rem;color:var(--txt2);padding:4px 8px;border-left:2px solid var(--bdr);margin-bottom:4px;}
.log-e.alert{border-left-color:var(--red);color:var(--red);}
.log-e.warn{border-left-color:var(--amber);color:var(--amber);}
.log-e.info{border-left-color:var(--blue);color:var(--cyan);}
.log-e.ok{border-left-color:var(--green);color:var(--green);}
.log-e.purple{border-left-color:var(--purple);color:#ce93d8;}

/* Resource bars */
.res-row{display:flex;align-items:center;gap:10px;margin-bottom:10px;}
.res-name{font-family:var(--fm);font-size:.7rem;color:var(--txt2);min-width:130px;}
.res-bar-bg{flex:1;height:7px;background:var(--bg2);border-radius:4px;overflow:hidden;}
.res-bar-fill{height:100%;border-radius:4px;transition:width .5s;}
.res-val{font-family:var(--fm);font-size:.7rem;color:var(--mono);min-width:40px;text-align:right;}

/* Evac route */
.evac-r{background:var(--bgc);border:1px solid var(--bdr);border-left:3px solid var(--amber);border-radius:4px;padding:9px 13px;font-family:var(--fm);font-size:.73rem;color:var(--amber);margin-bottom:6px;}

/* SMS card */
.sms-card{background:var(--bgc2);border:1px solid var(--bdr);border-radius:8px;padding:14px;font-family:var(--fm);font-size:.78rem;color:var(--txt);white-space:pre-wrap;margin-top:8px;}

/* Camp status */
.camp-crit{background:rgba(255,55,55,.07);border:1px solid rgba(255,55,55,.3);border-left:3px solid var(--red);border-radius:5px;padding:10px 14px;margin-bottom:8px;}
.camp-ok{background:rgba(0,230,118,.05);border:1px solid rgba(0,230,118,.2);border-left:3px solid var(--green);border-radius:5px;padding:10px 14px;margin-bottom:8px;}
.camp-std{background:rgba(0,180,255,.05);border:1px solid rgba(0,180,255,.15);border-left:3px solid var(--blue);border-radius:5px;padding:10px 14px;margin-bottom:8px;}
.camp-stat{font-family:var(--fm);font-size:.7rem;line-height:1.9;}
.camp-name{font-family:var(--fd);font-size:.95rem;font-weight:700;margin-bottom:4px;}

/* Vehicle badge */
.veh-dep{display:inline-block;background:rgba(0,180,255,.12);border:1px solid rgba(0,180,255,.35);border-radius:3px;padding:1px 8px;font-family:var(--fm);font-size:.62rem;color:var(--cyan);}
.veh-avl{display:inline-block;background:rgba(0,230,118,.1);border:1px solid rgba(0,230,118,.3);border-radius:3px;padding:1px 8px;font-family:var(--fm);font-size:.62rem;color:var(--green);}
.veh-mtn{display:inline-block;background:rgba(255,179,0,.1);border:1px solid rgba(255,179,0,.3);border-radius:3px;padding:1px 8px;font-family:var(--fm);font-size:.62rem;color:var(--amber);}
.veh-enr{display:inline-block;background:rgba(156,39,176,.12);border:1px solid rgba(156,39,176,.35);border-radius:3px;padding:1px 8px;font-family:var(--fm);font-size:.62rem;color:#ce93d8;}

/* Comm priority */
.pri-high{color:var(--red);font-family:var(--fm);font-size:.65rem;font-weight:700;}
.pri-med{color:var(--amber);font-family:var(--fm);font-size:.65rem;font-weight:700;}
.pri-low{color:var(--green);font-family:var(--fm);font-size:.65rem;font-weight:700;}

/* Missing person */
.mp-card{background:rgba(255,55,55,.06);border:1px solid rgba(255,55,55,.25);border-radius:6px;padding:12px;margin-bottom:8px;}
.mp-found{background:rgba(0,230,118,.06);border:1px solid rgba(0,230,118,.25);border-radius:6px;padding:12px;margin-bottom:8px;}

/* Gauge river */
.gauge-danger{color:var(--red)!important;}
.gauge-warn{color:var(--amber)!important;}
.gauge-safe{color:var(--green)!important;}

/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--bdr);border-radius:3px;}

/* Chatbot */
.chat-bubble-user{background:rgba(0,180,255,.12);border:1px solid rgba(0,180,255,.25);border-radius:10px 10px 2px 10px;padding:10px 14px;font-family:var(--fu);font-size:.85rem;color:var(--txt);margin:6px 40px 6px 0;text-align:right;}
.chat-bubble-ai{background:rgba(13,30,46,.9);border:1px solid var(--bdr);border-radius:10px 10px 10px 2px;padding:10px 14px;font-family:var(--fu);font-size:.85rem;color:var(--txt);margin:6px 0 6px 40px;}
.chat-label{font-family:var(--fm);font-size:.6rem;color:var(--txt2);text-transform:uppercase;letter-spacing:.1em;margin-bottom:2px;}

@media(max-width:768px){.kpi-val{font-size:1.3rem;}.hdr-title{font-size:1.1rem;}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
for k, v in {
    "citizen_reports": {},
    "broadcast_log": [],
    "alert_count": 0,
    "missing_persons": [
        {"id":"MP-001","name":"Ramu Selvam",  "age":62,"district":"Nagapattinam","last_seen":"Near Vettar River bank","reported_by":"Son – 94445-22001","status":"Missing","time":"07:15"},
        {"id":"MP-002","name":"Kamala Devi",  "age":45,"district":"Tiruvarur",   "last_seen":"Flood relief camp area","reported_by":"Husband – 94445-22002","status":"Missing","time":"08:30"},
        {"id":"MP-003","name":"Arun Kumar",   "age":8, "district":"Chennai",     "last_seen":"Adyar river bank park","reported_by":"Mother – 94445-22003","status":"Missing","time":"06:50"},
        {"id":"MP-004","name":"Selvam Raj",   "age":38,"district":"Cuddalore",   "last_seen":"Fishing boat, did not return","reported_by":"Wife – 94445-22004","status":"Found Safe","time":"05:20"},
        {"id":"MP-005","name":"Meena Kumari", "age":29,"district":"Nagapattinam","last_seen":"Flood-affected Velankanni","reported_by":"Brother – 94445-22005","status":"Missing","time":"09:05"},
    ],
    "rescue_ops": [
        {"id":"RO-001","team":"NDRF Team Alpha","district":"Nagapattinam","persons_rescued":23,"operation":"Boat rescue – Velankanni coast","status":"Active","start":"06:00"},
        {"id":"RO-002","team":"NDRF Team Beta", "district":"Tiruvarur",   "persons_rescued":41,"operation":"Roof-top evacuation – Delta region","status":"Active","start":"07:30"},
        {"id":"RO-003","team":"Fire & Rescue 7","district":"Chennai",     "persons_rescued":12,"operation":"Adyar colony water extraction","status":"Active","start":"08:15"},
        {"id":"RO-004","team":"Coast Guard-3",  "district":"Cuddalore",   "persons_rescued":67,"operation":"Coastal fishing village evacuation","status":"Completed","start":"04:00"},
        {"id":"RO-005","team":"SDRF Team C",    "district":"Thanjavur",   "persons_rescued":18,"operation":"Cauvery overflow village rescue","status":"Active","start":"08:45"},
    ],
    "volunteers": [],
    "comm_log": COMM_LOG_SEED[:],
    "damage_reports": [],
    "chat_history": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# MODEL
# ============================================================
@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except:
        return None

model = load_model()

# ============================================================
# WEATHER HELPERS
# ============================================================
def get_live_weather(city):
    coords = TN_CITIES.get(city)
    url = (f"http://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"
           if coords else f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
    try:
        r = requests.get(url, timeout=5)
        d = r.json()
        if r.status_code == 200:
            return {"City":city,"Temperature":d["main"]["temp"],"Humidity":d["main"]["humidity"],
                    "Rainfall":d.get("rain",{}).get("1h",0),"WindSpeed":d["wind"]["speed"],
                    "Lat":d["coord"]["lat"],"Lon":d["coord"]["lon"]}
    except:
        pass
    return None

def get_forecast(city):
    coords = TN_CITIES.get(city)
    url = (f"http://api.openweathermap.org/data/2.5/forecast?lat={coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"
           if coords else f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric")
    try:
        r = requests.get(url, timeout=5)
        d = r.json()
        if r.status_code == 200:
            return pd.DataFrame([{"Time":i["dt_txt"],"Rainfall":i.get("rain",{}).get("3h",0),
                                   "Temperature":i["main"]["temp"],"WindSpeed":i["wind"]["speed"]}
                                  for i in d["list"]])
    except:
        pass
    return None

def fetch_city_weather(args):
    city, coords, sc, st_, sr, sw, sh = args
    if city == sc:
        return {"City":city,"Temperature":st_,"Rainfall":sr,"WindSpeed":sw,"Humidity":sh,
                "Lat":coords["lat"],"Lon":coords["lon"]}
    return get_live_weather(city)

def get_state_risk_data(sc=None, st_=None, sr=None, sw=None, sh=50):
    if not model:
        return pd.DataFrame()
    args = [(c, d, sc, st_, sr, sw, sh) for c, d in TN_CITIES.items()]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(fetch_city_weather, a): a[0] for a in args}
        for fut in concurrent.futures.as_completed(futures):
            w = fut.result()
            if not w:
                continue
            inp = pd.DataFrame([{"Temperature":w["Temperature"],"Rainfall":w["Rainfall"],"WindSpeed":w["WindSpeed"]}])
            base = model.predict(inp)[0]
            vuln = TN_CITIES.get(w["City"],{}).get("vuln",0.5)
            pop  = TN_CITIES.get(w["City"],{}).get("pop",500000)
            elev = TN_CITIES.get(w["City"],{}).get("elevation",100)
            if   w["Rainfall"]>50 and vuln>0.7: fr,reason = 2,"Critical: High Rainfall + Coastal Low-Lying"
            elif base==2:                         fr,reason = 2,"AI Model: Extreme Weather"
            elif base==1 and vuln>0.6:            fr,reason = 2,"Elevated: Moderate Rain in Flood-Prone Zone"
            else:                                 fr,reason = base,"Standard: Normal Parameters"
            cr = st.session_state.get("citizen_reports",{})
            if w["City"] in cr and any(x in cr[w["City"]] for x in ["Flooded","Critical"]):
                fr,reason = 2,f"Ground Report: {cr[w['City']]}"
            color = ["#00e676","#ffb300","#ff3737"][fr]
            rl    = ["Low","Moderate","High"][fr]
            score = round(min(100, w["Rainfall"]*0.4 + vuln*40 + fr*20), 1)
            arp   = int(pop * vuln * [0.05,0.2,0.6][fr])
            w.update({"Risk Level":rl,"Risk Score":score,"Color":color,"Reason":reason,
                      "Vulnerability":vuln,"Population":pop,"Elevation":elev,"At-Risk Pop":arp,"Risk_Num":fr})
            results.append(w)
    return pd.DataFrame(results)

# ============================================================
# AI CHATBOT RESPONSE (rule-based + context-aware)
# ============================================================
def ai_chatbot_response(query: str, map_df: pd.DataFrame) -> str:
    q = query.lower()
    now_str = datetime.now().strftime("%d %b %Y %H:%M")

    # High risk districts
    if any(x in q for x in ["high risk","highest risk","most dangerous","danger"]):
        if not map_df.empty:
            hr = map_df[map_df["Risk_Num"]==2]["City"].tolist()
            return (f"🔴 **{len(hr)} High-Risk Districts** as of {now_str}:\n\n" +
                    "\n".join([f"• {c}" for c in hr]) +
                    "\n\nImmediate action advised: activate EOC, pre-position NDRF teams, and issue public advisories.")

    if any(x in q for x in ["camp","relief camp","capacity","occupancy"]):
        crit = [k for k,v in RELIEF_CAMPS_DATA.items() if v["status"]=="Critical"]
        total_occ = sum(v["occupied"] for v in RELIEF_CAMPS_DATA.values())
        total_cap = sum(v["capacity"] for v in RELIEF_CAMPS_DATA.values())
        return (f"🏕️ **Relief Camp Status ({now_str})**\n\n"
                f"• Total Camps Active: **{len(RELIEF_CAMPS_DATA)}**\n"
                f"• Overall Occupancy: **{total_occ}/{total_cap}** ({total_occ*100//total_cap}%)\n"
                f"• ⚠️ Critical Camps (>90% full): **{', '.join(crit) if crit else 'None'}**\n\n"
                f"Recommend requesting overflow relief camps from nearest standby districts.")

    if any(x in q for x in ["missing","missing person","rescue","found"]):
        mp = st.session_state["missing_persons"]
        missing_cnt = sum(1 for p in mp if p["status"]=="Missing")
        found_cnt   = sum(1 for p in mp if p["status"]=="Found Safe")
        return (f"🔍 **Missing Persons Summary ({now_str})**\n\n"
                f"• Total Reported: **{len(mp)}**\n"
                f"• Still Missing: **{missing_cnt}** ⚠️\n"
                f"• Found Safe: **{found_cnt}** ✅\n\n"
                f"Active rescue ops: **{sum(1 for r in st.session_state['rescue_ops'] if r['status']=='Active')}** teams deployed.\n"
                f"Total rescued today: **{sum(r['persons_rescued'] for r in st.session_state['rescue_ops'])}** persons.")

    if any(x in q for x in ["supply","food","water","medicine","stock"]):
        low = [k for k,v in SUPPLY_CHAIN.items() if (v["total"]-v["delivered"]) <= v["reorder_at"]]
        return (f"📦 **Supply Chain Status ({now_str})**\n\n"
                f"• Total supply categories tracked: **{len(SUPPLY_CHAIN)}**\n"
                f"• ⚠️ Low Stock Alert: **{', '.join(low) if low else 'None — All stocks adequate'}**\n\n"
                f"Delivery rate: {sum(v['delivered'] for v in SUPPLY_CHAIN.values()):,} units delivered today.\n"
                f"Recommend immediate reorder for critical items.")

    if any(x in q for x in ["vehicle","fleet","boat","ambulance","truck","helicopter"]):
        deployed = sum(1 for v in VEHICLES.values() if v["status"]=="Deployed")
        avail    = sum(1 for v in VEHICLES.values() if v["status"]=="Available")
        maint    = sum(1 for v in VEHICLES.values() if v["status"]=="Maintenance")
        return (f"🚗 **Fleet Status ({now_str})**\n\n"
                f"• Total Vehicles Tracked: **{len(VEHICLES)}**\n"
                f"• Deployed: **{deployed}** | Available: **{avail}** | Maintenance: **{maint}**\n\n"
                f"Low-fuel alerts (< 40%): "
                + ", ".join([k for k,v in VEHICLES.items() if v["fuel"]<40]) +
                "\n\nRecommend refuelling before next deployment cycle.")

    if any(x in q for x in ["river","gauge","level","flood level","cauvery","vaigai"]):
        danger = [k for k,v in RIVER_GAUGES.items() if v["current"] >= v["danger"]]
        warn   = [k for k,v in RIVER_GAUGES.items() if v["warning"] <= v["current"] < v["danger"]]
        return (f"🌊 **River Gauge Status ({now_str})**\n\n"
                f"• 🔴 At/Above Danger Level: **{', '.join(danger) if danger else 'None'}**\n"
                f"• 🟡 At Warning Level: **{', '.join(warn) if warn else 'None'}**\n"
                f"• 🟢 Normal: **{len(RIVER_GAUGES)-len(danger)-len(warn)} gauges**\n\n"
                f"Recommend issuing flood watch for rising-trend rivers.")

    if any(x in q for x in ["volunteer","volunteers","registered"]):
        vols = st.session_state["volunteers"]
        return (f"🙋 **Volunteer Summary ({now_str})**\n\n"
                f"• Total Registered: **{len(vols)}**\n"
                f"• Skills available: Medical, Rescue, Logistics, Communication\n\n"
                f"Use the Volunteer Portal tab to register new volunteers and assign them to districts.")

    if any(x in q for x in ["rainfall","rain","precipitation"]):
        if not map_df.empty:
            top = map_df.nlargest(5,"Rainfall")[["City","Rainfall","Risk Level"]]
            lines = "\n".join([f"• {r['City']}: **{r['Rainfall']:.1f}mm** ({r['Risk Level']})" for _,r in top.iterrows()])
            return f"🌧️ **Top Rainfall Districts ({now_str})**\n\n{lines}\n\nMonitor these districts closely for river overflow."

    if any(x in q for x in ["helpline","contact","number","phone","emergency"]):
        return ("📞 **Emergency Contacts**\n\n"
                "• SEOC Control Room: **1070**\n"
                "• Police Emergency: **100**\n"
                "• Fire & Rescue: **101**\n"
                "• Ambulance: **108**\n"
                "• Coast Guard: **1554**\n"
                "• Disaster Mgmt Dept: **044-28593990**\n\n"
                "All lines are 24×7 operational.")

    if any(x in q for x in ["summary","overview","status","situation"]):
        if not map_df.empty:
            hr = int((map_df["Risk_Num"]==2).sum())
            mr = int((map_df["Risk_Num"]==1).sum())
            lr = int((map_df["Risk_Num"]==0).sum())
            arp = int(map_df["At-Risk Pop"].sum())
            return (f"📋 **Situation Summary — {now_str}**\n\n"
                    f"🔴 High Risk: **{hr} districts**\n"
                    f"🟡 Moderate: **{mr} districts**\n"
                    f"🟢 Safe: **{lr} districts**\n"
                    f"👥 Population at Risk: **{arp:,}**\n\n"
                    f"Relief Camps Active: **{len(RELIEF_CAMPS_DATA)}** | "
                    f"Rescue Ops Active: **{sum(1 for r in st.session_state['rescue_ops'] if r['status']=='Active')}** | "
                    f"Vehicles Deployed: **{sum(1 for v in VEHICLES.values() if v['status']=='Deployed')}**")

    return (f"👋 I am the **SEOC AI Assistant**. I can help you with:\n\n"
            "• `high risk districts` — current threat level\n"
            "• `relief camp status` — occupancy & supplies\n"
            "• `missing persons` — search & rescue summary\n"
            "• `supply chain` — food, water, medicine stock\n"
            "• `vehicle fleet` — deployment & fuel status\n"
            "• `river gauges` — live river level alerts\n"
            "• `situation summary` — overall state overview\n"
            "• `emergency contacts` — helpline numbers\n\n"
            "_Type your query above to get a real-time briefing._")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0;border-bottom:1px solid #1a3a5c;margin-bottom:14px;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:.62rem;color:#5dc8ff;letter-spacing:.18em;text-transform:uppercase;">Command Console</div>
      <div style="font-family:'Exo 2',sans-serif;font-size:1.05rem;font-weight:800;color:#e8f4fd;">TN-SEOC v4.0</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**⚙️ SIMULATION MODE**")
    use_sim = st.checkbox("Enable Manual Override", key="sim_tog")
    sim_city=sim_temp=sim_rain=sim_wind=sim_hum=None
    if use_sim:
        st.warning("⚠️ Manual Override Active")
        sim_city = st.selectbox("Target District", list(TN_CITIES.keys()), key="sc")
        sim_temp = st.slider("Temperature (°C)", 15, 45, 30)
        sim_rain = st.slider("Rainfall (mm)", 0, 300, 120)
        sim_wind = st.slider("Wind Speed (m/s)", 0, 50, 18)
        sim_hum  = st.slider("Humidity (%)", 30, 100, 75)

    st.markdown("---")
    st.markdown("**📢 CITIZEN GROUND REPORT**")
    rep_city   = st.selectbox("Location", list(TN_CITIES.keys()), key="rc")
    rep_status = st.radio("Condition", ["✅ Safe","⚠️ Water Logging","🌊 Flooded","🚨 Critical"], label_visibility="collapsed")
    up_file    = st.file_uploader("📸 Evidence Photo", type=["jpg","png","jpeg"])
    if st.button("📡 BROADCAST", use_container_width=True):
        if up_file:
            st.session_state["citizen_reports"][rep_city] = rep_status
            st.session_state["broadcast_log"].insert(0,("alert",f"[{datetime.now().strftime('%H:%M:%S')}] CITIZEN · {rep_city} · {rep_status}"))
            st.session_state["alert_count"] += 1
            st.success(f"✅ Broadcasted: {rep_city}")
            st.toast(f"🚨 {rep_status} — {rep_city}", icon="📣")
            st.rerun()
        else:
            st.error("Photo required for verification.")

    st.markdown("---")
    st.markdown("**📋 RECENT LOG**")
    for kind, entry in st.session_state["broadcast_log"][:5]:
        st.markdown(f'<div class="log-e {kind}">{entry}</div>', unsafe_allow_html=True)
    if not st.session_state["broadcast_log"]:
        st.markdown('<div class="log-e">// No broadcasts yet</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:.62rem;color:#3a6a8a;text-align:center;line-height:1.9;">SEOC AI DIVISION · BUILD 2025.06<br><span style="color:#5dc8ff;">📞 HELPLINE: 1070</span></div>', unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
now = datetime.now()
st.markdown(f"""
<div class="hdr">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
    <div>
      <p class="hdr-title">🛡️ TAMIL NADU DISASTER RESPONSE SYSTEM</p>
      <p class="hdr-sub">State Emergency Operations Centre (SEOC) · AI-Powered Flood Intelligence Platform</p>
      <span class="hdr-status">● SYSTEM ONLINE — {now.strftime('%d %b %Y %H:%M')} IST</span>
    </div>
    <div style="text-align:right;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:.62rem;color:#3a6a8a;text-transform:uppercase;letter-spacing:.1em;">Monitoring</div>
      <div style="font-family:'Exo 2',sans-serif;font-size:2rem;font-weight:800;color:#00b4ff;">38</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:.62rem;color:#3a6a8a;">DISTRICTS</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

alerts_ticker = ["🔴 NAGAPATTINAM: Rainfall >80mm. NDRF Alert Issued.","🟡 THANJAVUR: River Cauvery at 85% capacity.",
                 "🔴 CHENNAI: Cyclone Depression forming in BoB.","🟢 NILGIRIS: All clear.",
                 "📞 HELPLINE 1070 — 24×7 ACTIVE","🔴 CUDDALORE: Coastal flood watch in effect.",
                 "🟡 TIRUVARUR: Delta region ORANGE alert.","⚠️ MISSING: 4 persons reported — see Rescue tab."]
st.markdown(f'<div class="ticker-wrap">⚡ LIVE  ◈  {"  ◈  ".join(alerts_ticker*2)}</div>', unsafe_allow_html=True)

# ============================================================
# FETCH DATA
# ============================================================
with st.spinner("⟳ Scanning satellite telemetry..."):
    map_data = get_state_risk_data(sim_city, sim_temp, sim_rain, sim_wind, sim_hum or 50)

# ============================================================
# TOP KPIs
# ============================================================
if not map_data.empty:
    hc = int((map_data["Risk_Num"]==2).sum())
    mc = int((map_data["Risk_Num"]==1).sum())
    lc = int((map_data["Risk_Num"]==0).sum())
    arp= int(map_data["At-Risk Pop"].sum())
    total_rescued = sum(r["persons_rescued"] for r in st.session_state["rescue_ops"])
    active_camps  = sum(1 for c in RELIEF_CAMPS_DATA.values() if c["status"]!="Standby")
    st.markdown(f"""
    <div class="kpi-strip">
      <div class="kpi-box red"><div class="kpi-val">{hc}</div><div class="kpi-lbl">🔴 High Risk Districts</div></div>
      <div class="kpi-box amber"><div class="kpi-val">{mc}</div><div class="kpi-lbl">🟡 Moderate Districts</div></div>
      <div class="kpi-box green"><div class="kpi-val">{lc}</div><div class="kpi-lbl">🟢 Safe Districts</div></div>
      <div class="kpi-box cyan"><div class="kpi-val">{arp:,}</div><div class="kpi-lbl">⚠️ Population at Risk</div></div>
      <div class="kpi-box"><div class="kpi-val">{total_rescued}</div><div class="kpi-lbl">🚣 Persons Rescued</div></div>
      <div class="kpi-box amber"><div class="kpi-val">{active_camps}</div><div class="kpi-lbl">🏕️ Active Relief Camps</div></div>
      <div class="kpi-box purple"><div class="kpi-val">{st.session_state['alert_count']}</div><div class="kpi-lbl">📢 Citizen Reports</div></div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TABS  (12 tabs total)
# ============================================================
(tab_map, tab_dd, tab_res, tab_evac, tab_hist,
 tab_bc, tab_camp, tab_mp, tab_fleet,
 tab_supply, tab_comm, tab_ai) = st.tabs([
    "🗺️ Live Map",
    "🔍 District Analysis",
    "📦 Resources",
    "🚗 Evacuation",
    "📊 Historical",
    "📡 Broadcast",
    "🏕️ Relief Camps",
    "🔍 Rescue Ops",
    "🚘 Fleet",
    "📦 Supply Chain",
    "📻 Comms Log",
    "🤖 AI Assistant",
])

# ─────────────────────────────────────────────
# TAB 1 – LIVE MAP
# ─────────────────────────────────────────────
with tab_map:
    mc1, mc2 = st.columns([3,1])
    with mc1:
        a1,a2,a3 = st.columns(3)
        ms = a1.radio("View",("Light","Street","Satellite"),horizontal=True,label_visibility="collapsed")
        fr_f = a2.multiselect("Filter",["High","Moderate","Low"],default=["High","Moderate","Low"],label_visibility="collapsed")
        sp  = a3.checkbox("Size by Population", value=True)
        if not map_data.empty:
            fd2 = map_data[map_data["Risk Level"].isin(fr_f)].copy()
            fd2["dot"] = (fd2["Population"]/fd2["Population"].max()*25+5) if sp else 12
            mbs = {"Light":"carto-positron","Street":"open-street-map","Satellite":"white-bg"}[ms]
            ml  = [{"below":"traces","sourcetype":"raster","source":["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]}] if ms=="Satellite" else []
            fig_m = px.scatter_mapbox(fd2,lat="Lat",lon="Lon",color="Risk Level",size="dot",size_max=30,
                hover_name="City",hover_data={"dot":False,"Lat":False,"Lon":False,"Temperature":":.1f",
                "Rainfall":":.1f","Risk Score":True,"At-Risk Pop":":,","Reason":True},
                color_discrete_map={"Low":"#00e676","Moderate":"#ffb300","High":"#ff3737"},
                mapbox_style=mbs,height=560)
            if ml: fig_m.update_layout(mapbox_layers=ml)
            fig_m.update_layout(margin=dict(r=0,t=0,l=0,b=0),paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(bgcolor="rgba(5,10,15,0.8)",bordercolor="#1a3a5c",borderwidth=1,
                font=dict(color="#e8f4fd",family="Share Tech Mono, monospace",size=11)),
                mapbox=dict(center=dict(lat=11.0,lon=78.6),zoom=6.3))
            st.plotly_chart(fig_m, use_container_width=True)
    with mc2:
        st.markdown('<div class="cmd-hdr">■ RISK TABLE</div>', unsafe_allow_html=True)
        if not map_data.empty:
            tbl = map_data[["City","Risk Level","Risk Score","Rainfall"]].sort_values("Risk Score",ascending=False)
            tbl.columns=["District","Risk","Score","Rain(mm)"]
            tbl["Risk"]=tbl["Risk"].map({"High":"🔴 HIGH","Moderate":"🟡 MOD","Low":"🟢 LOW"})
            st.dataframe(tbl,use_container_width=True,height=520,hide_index=True,
                column_config={"Score":st.column_config.ProgressColumn("Score",min_value=0,max_value=100,format="%.0f")})

# ─────────────────────────────────────────────
# TAB 2 – DISTRICT DEEP DIVE
# ─────────────────────────────────────────────
with tab_dd:
    d1,d2 = st.columns([1,2])
    with d1:
        tgt = st.selectbox("Select District", list(TN_CITIES.keys()), key="ddc")
        go_btn = st.button("⚡ ANALYZE", use_container_width=True)
        if not map_data.empty and tgt in map_data["City"].values:
            row = map_data[map_data["City"]==tgt].iloc[0]
            rc  = {"High":"#ff3737","Moderate":"#ffb300","Low":"#00e676"}.get(row["Risk Level"],"#aaa")
            st.markdown(f"""<div class="cmd-card"><div class="cmd-hdr">■ QUICK STATUS</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:.7rem;color:#7fb3d3;line-height:2.1;">
            <div>DISTRICT <span style="color:#e8f4fd;float:right;">{tgt.upper()}</span></div>
            <div>RISK LEVEL <span style="color:{rc};float:right;font-weight:700;">{row['Risk Level'].upper()}</span></div>
            <div>SCORE <span style="color:#00b4ff;float:right;">{row['Risk Score']:.0f}/100</span></div>
            <div>RAINFALL <span style="color:#e8f4fd;float:right;">{row['Rainfall']:.1f}mm</span></div>
            <div>TEMPERATURE <span style="color:#e8f4fd;float:right;">{row['Temperature']:.1f}°C</span></div>
            <div>VULNERABILITY <span style="color:#e8f4fd;float:right;">{TN_CITIES[tgt]['vuln']*100:.0f}%</span></div>
            <div>ELEVATION <span style="color:#e8f4fd;float:right;">{TN_CITIES[tgt]['elevation']}m</span></div>
            <div>AT-RISK POP <span style="color:#ffb300;float:right;">{row['At-Risk Pop']:,}</span></div>
            </div></div>""", unsafe_allow_html=True)
    with d2:
        if go_btn:
            if use_sim and tgt==sim_city:
                w={"Temperature":sim_temp,"Rainfall":sim_rain,"WindSpeed":sim_wind,"Humidity":sim_hum}
                st.info("🧪 Simulation Active")
            else:
                with st.spinner("Fetching..."):
                    w=get_live_weather(tgt)
            if w and model:
                inp=pd.DataFrame([{"Temperature":w["Temperature"],"Rainfall":w["Rainfall"],"WindSpeed":w["WindSpeed"]}])
                base=model.predict(inp)[0]
                vuln=TN_CITIES.get(tgt,{}).get("vuln",0.5)
                pred=2 if (w["Rainfall"]>50 and vuln>0.7) or base==2 or (base==1 and vuln>0.6) else base
                c1,c2,c3,c4=st.columns(4)
                c1.metric("🌡 Temp",f"{w['Temperature']:.1f}°C")
                c2.metric("🌧 Rain",f"{w['Rainfall']:.1f}mm")
                c3.metric("💨 Wind",f"{w['WindSpeed']:.1f}m/s")
                c4.metric("💧 Humidity",f"{w.get('Humidity',0)}%")
                if pred==2:
                    st.markdown(f"""<div style="background:rgba(255,55,55,.1);border:1px solid #ff3737;border-left:4px solid #ff3737;
                    border-radius:6px;padding:14px;margin:10px 0;">
                    <div style="font-family:'Exo 2',sans-serif;font-size:1.1rem;font-weight:800;color:#ff3737;">🚨 HIGH FLOOD RISK — {tgt.upper()}</div>
                    <div style="font-family:'Share Tech Mono',monospace;font-size:.72rem;color:#ff8a8a;margin-top:5px;">IMMEDIATE ACTION · ACTIVATE NDRF · ISSUE EVACUATION</div></div>""",unsafe_allow_html=True)
                elif pred==1: st.warning(f"⚠️ MODERATE RISK — {tgt}. Stay alert.")
                else: st.success(f"✅ SAFE — {tgt}. Normal parameters.")
                st.markdown("**📅 5-Day Forecast**")
                if use_sim and tgt==sim_city:
                    dates=pd.date_range(start=pd.Timestamp.now(),periods=40,freq="3h")
                    fc=pd.DataFrame({"Time":dates,"Rainfall":[max(0,x) for x in np.random.normal(sim_rain,12,40)],
                        "Temperature":[max(20,x) for x in np.random.normal(sim_temp,1.5,40)],"WindSpeed":[max(0,x) for x in np.random.normal(sim_wind,3,40)]})
                else:
                    with st.spinner(): fc=get_forecast(tgt)
                if fc is not None:
                    fig_fc=make_subplots(rows=2,cols=1,shared_xaxes=True,row_heights=[0.6,0.4],vertical_spacing=0.08)
                    fig_fc.add_trace(go.Bar(x=fc["Time"],y=fc["Rainfall"],name="Rainfall(mm)",marker_color="rgba(0,180,255,.7)",marker_line_width=0),row=1,col=1)
                    fig_fc.add_trace(go.Scatter(x=fc["Time"],y=fc["Temperature"],name="Temp(°C)",line=dict(color="#ffb300",width=2)),row=2,col=1)
                    fig_fc.update_layout(height=300,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.6)",
                        font=dict(color="#7fb3d3",family="Share Tech Mono",size=10),
                        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#e8f4fd")),margin=dict(l=0,r=0,t=8,b=0))
                    fig_fc.update_xaxes(gridcolor="#1a3a5c"); fig_fc.update_yaxes(gridcolor="#1a3a5c")
                    st.plotly_chart(fig_fc,use_container_width=True)
                # PDF report
                rpt=(f"OFFICIAL SITUATION REPORT\n{'='*50}\n"
                     f"District    : {tgt}\nGenerated   : {now.strftime('%d-%b-%Y %H:%M IST')}\n"
                     f"Risk Level  : {'HIGH' if pred==2 else 'MODERATE' if pred==1 else 'LOW'}\n"
                     f"Temperature : {w['Temperature']:.1f}°C\nRainfall    : {w['Rainfall']:.1f}mm\n"
                     f"Wind Speed  : {w['WindSpeed']:.1f}m/s\nVulnerability: {vuln:.2f}\n"
                     f"{'='*50}\nIssued by TN SEOC AI Division\n")
                st.download_button("📄 Download Report",rpt,f"SEOC_{tgt}_{now.strftime('%Y%m%d_%H%M')}.txt","text/plain",use_container_width=True)
            else:
                st.error("⚠️ Model not loaded or weather data unavailable.")

# ─────────────────────────────────────────────
# TAB 3 – RESOURCES
# ─────────────────────────────────────────────
with tab_res:
    r1,r2=st.columns(2)
    clrs={"Boats":"#00b4ff","Relief Camps":"#00ffd5","Helicopters":"#ffb300","NDRF Teams":"#ff3737","Medical Units":"#00e676"}
    totals={r:sum(v.values()) for r,v in RESOURCES.items()}
    mx=max(totals.values())
    with r1:
        st.markdown('<div class="cmd-hdr">■ RESOURCE ALLOCATION BY TYPE</div>',unsafe_allow_html=True)
        html=""
        for res in RESOURCES:
            pct=totals[res]/mx*100
            html+=f'<div class="res-row"><span class="res-name">{res}</span><div class="res-bar-bg"><div class="res-bar-fill" style="width:{pct}%;background:{clrs.get(res,"#00b4ff")};"></div></div><span class="res-val">{totals[res]}</span></div>'
        st.markdown(html,unsafe_allow_html=True)
        fig_p=px.pie(names=list(totals.keys()),values=list(totals.values()),color_discrete_sequence=list(clrs.values()),hole=0.55)
        fig_p.update_traces(textfont=dict(color="#e8f4fd",family="Share Tech Mono",size=10),marker=dict(line=dict(color="#050a0f",width=2)))
        fig_p.update_layout(height=240,paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#7fb3d3"),
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#e8f4fd",family="Share Tech Mono",size=10)),margin=dict(l=0,r=0,t=8,b=0))
        st.plotly_chart(fig_p,use_container_width=True)
    with r2:
        sel=st.selectbox("Resource Type",list(RESOURCES.keys()),key="rt")
        df_r=pd.DataFrame(list(RESOURCES[sel].items()),columns=["District","Units"]).sort_values("Units")
        fig_r=go.Figure(go.Bar(x=df_r["Units"],y=df_r["District"],orientation="h",
            marker=dict(color=clrs.get(sel,"#00b4ff"),line=dict(color="rgba(0,0,0,0)",width=0)),
            text=df_r["Units"],textposition="outside",textfont=dict(color="#e8f4fd",family="Share Tech Mono",size=11)))
        fig_r.update_layout(height=280,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=10),margin=dict(l=0,r=60,t=8,b=0),
            xaxis=dict(gridcolor="#1a3a5c"),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_r,use_container_width=True)
        if not map_data.empty:
            st.markdown('<div class="cmd-hdr">■ RESOURCE GAP — HIGH RISK</div>',unsafe_allow_html=True)
            hr_c=map_data[map_data["Risk_Num"]==2]["City"].tolist()
            dep=list(RESOURCES.get(sel,{}).keys())
            gap=[c for c in hr_c if c not in dep]
            for gc in gap[:5]:
                st.markdown(f'<div style="background:rgba(255,55,55,.07);border:1px solid rgba(255,55,55,.3);border-radius:4px;padding:8px 12px;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;font-size:.7rem;color:#ff8a8a;">⚠️ {gc} — HIGH RISK · No {sel} Deployed</div>',unsafe_allow_html=True)
            if not gap: st.success(f"✅ All high-risk districts have {sel}.")

# ─────────────────────────────────────────────
# TAB 4 – EVACUATION
# ─────────────────────────────────────────────
with tab_evac:
    e1,e2=st.columns([1,2])
    with e1:
        ec=st.selectbox("District",list(EVAC_ROUTES.keys()),key="evc")
        routes=EVAC_ROUTES.get(ec,[])
        v=TN_CITIES.get(ec,{})
        vc={"#ff3737" if v.get("vuln",0)>0.7 else "#ffb300" if v.get("vuln",0)>0.4 else "#00e676": True}
        rc2=list(vc.keys())[0]
        st.markdown(f"""<div class="cmd-card">
        <div class="cmd-hdr">■ DISTRICT PROFILE</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:.7rem;color:#7fb3d3;line-height:2.1;">
        <div>POPULATION <span style="color:#e8f4fd;float:right;">{v.get('pop',0):,}</span></div>
        <div>ELEVATION <span style="color:#e8f4fd;float:right;">{v.get('elevation',0)}m ASL</span></div>
        <div>FLOOD VULNERABILITY <span style="color:{rc2};float:right;">{v.get('vuln',0)*100:.0f}%</span></div>
        </div></div>""",unsafe_allow_html=True)
    with e2:
        st.markdown('<div class="cmd-hdr">■ EVACUATION ROUTES</div>',unsafe_allow_html=True)
        for i,r in enumerate(routes,1):
            st.markdown(f'<div class="evac-r">◈ ROUTE {i}  ·  {r}</div>',unsafe_allow_html=True)
        st.markdown("---")
        if st.button("📱 Generate SMS Advisory",use_container_width=False):
            sms=(f"⚠️ SEOC EMERGENCY ALERT ⚠️\nDistrict: {ec.upper()}\nDate/Time: {now.strftime('%d-%b %H:%M')}\n\n"
                 f"EVACUATION ADVISORY ISSUED\nProceed immediately via:\n"
                 +"\n".join([f"  {i+1}. {r}" for i,r in enumerate(routes)])+
                 f"\n\nAssembly points are open.\nHelpline: 1070 | Police: 100 | Ambulance: 108\n–TN SEOC")
            st.markdown(f'<div class="sms-card">{sms}</div>',unsafe_allow_html=True)
            st.session_state["broadcast_log"].insert(0,("warn",f"[{now.strftime('%H:%M:%S')}] SMS ADVISORY · {ec}"))
            st.download_button("⬇️ Download",sms,f"Advisory_{ec}_{now.strftime('%Y%m%d_%H%M')}.txt","text/plain")
    if not map_data.empty:
        st.markdown("**🗺️ Vulnerability Overview**")
        dv=map_data[["City","Vulnerability","Elevation","Population"]].sort_values("Vulnerability",ascending=False).head(20)
        fig_v=px.bar(dv,x="City",y="Vulnerability",color="Vulnerability",
            color_continuous_scale=[[0,"#00e676"],[0.5,"#ffb300"],[1,"#ff3737"]],hover_data={"Elevation":True,"Population":":,"})
        fig_v.update_layout(height=250,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=9),margin=dict(l=0,r=0,t=8,b=0),
            coloraxis_showscale=False,xaxis=dict(gridcolor="#1a3a5c",tickangle=-35),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_v,use_container_width=True)

# ─────────────────────────────────────────────
# TAB 5 – HISTORICAL
# ─────────────────────────────────────────────
with tab_hist:
    df_h=pd.DataFrame(HISTORICAL_FLOODS)
    h1,h2=st.columns(2)
    with h1:
        fig_d=go.Figure()
        fig_d.add_trace(go.Scatter(x=df_h["Year"],y=df_h["Deaths"],mode="lines+markers",
            line=dict(color="#ff3737",width=2.5),marker=dict(color="#ff3737",size=8,symbol="diamond"),
            fill="tozeroy",fillcolor="rgba(255,55,55,.08)",text=df_h["Event"],
            hovertemplate="<b>%{x}</b><br>Deaths: %{y}<br>%{text}<extra></extra>"))
        fig_d.update_layout(title=dict(text="Flood Fatalities 2015–2024",font=dict(color="#e8f4fd",size=12,family="Exo 2")),
            height=230,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=10),margin=dict(l=0,r=0,t=28,b=0),
            xaxis=dict(gridcolor="#1a3a5c",dtick=1),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_d,use_container_width=True)
    with h2:
        fig_dmg=go.Figure(go.Bar(x=df_h["Year"],y=df_h["Damage_Cr"],
            marker=dict(color="rgba(255,179,0,.7)",line=dict(color="#ffb300",width=1.5)),
            text=[f"₹{v:,}Cr" for v in df_h["Damage_Cr"]],textposition="outside",
            textfont=dict(color="#ffb300",size=9)))
        fig_dmg.update_layout(title=dict(text="Economic Damage ₹ Crore",font=dict(color="#e8f4fd",size=12,family="Exo 2")),
            height=230,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=10),margin=dict(l=0,r=0,t=28,b=38),
            xaxis=dict(gridcolor="#1a3a5c",dtick=1),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_dmg,use_container_width=True)
    h3,h4=st.columns(2)
    with h3:
        fig_sc=px.scatter(df_h,x="Rainfall_mm",y="Districts",size="Deaths",color="Damage_Cr",
            color_continuous_scale=[[0,"#00e676"],[0.5,"#ffb300"],[1,"#ff3737"]],
            hover_data={"Event":True,"Year":True},text="Year",
            labels={"Rainfall_mm":"Rainfall (mm)","Districts":"Affected Districts"})
        fig_sc.update_traces(textposition="top center",textfont=dict(color="#e8f4fd",size=9))
        fig_sc.update_layout(title=dict(text="Rainfall vs Affected Districts",font=dict(color="#e8f4fd",size=12,family="Exo 2")),
            height=250,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=10),margin=dict(l=0,r=0,t=28,b=0),
            coloraxis_showscale=False,xaxis=dict(gridcolor="#1a3a5c"),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_sc,use_container_width=True)
    with h4:
        st.markdown('<div class="cmd-hdr">■ EVENT SUMMARY</div>',unsafe_allow_html=True)
        df_disp=df_h[["Year","Event","Deaths","Districts","Rainfall_mm","Damage_Cr"]].copy()
        df_disp.columns=["Year","Event","Deaths","Districts","Rain(mm)","Damage(₹Cr)"]
        st.dataframe(df_disp,use_container_width=True,height=250,hide_index=True)
    st.markdown("---")
    k1,k2,k3,k4=st.columns(4)
    k1.metric("Total Deaths",int(df_h["Deaths"].sum()),"-14 vs prev decade")
    k2.metric("Districts Affected",int(df_h["Districts"].sum()))
    k3.metric("Max Rainfall","1218mm","2015 Chennai")
    k4.metric("Total Damage",f"₹{int(df_h['Damage_Cr'].sum()):,}Cr")

# ─────────────────────────────────────────────
# TAB 6 – BROADCAST CENTER
# ─────────────────────────────────────────────
with tab_bc:
    bc1,bc2=st.columns([1,2])
    with bc1:
        st.markdown('<div class="cmd-hdr">■ COMPOSE BROADCAST</div>',unsafe_allow_html=True)
        atype=st.selectbox("Alert Type",["🔴 RED ALERT","🟡 ORANGE ALERT","🟢 ALL CLEAR","📢 ADVISORY"])
        tdist=st.multiselect("Target Districts",list(TN_CITIES.keys()),default=["Chennai","Nagapattinam","Cuddalore"])
        cmsg =st.text_area("Message",height=80,placeholder="Leave blank for auto-generation...")
        chan =st.multiselect("Channels",["SMS","Sirens","TV Crawl","App Push","Radio"],default=["SMS","App Push"])
        if st.button("📡 BROADCAST NOW",use_container_width=True):
            if tdist:
                for d in tdist:
                    kind="alert" if "RED" in atype else "warn" if "ORANGE" in atype else "ok"
                    st.session_state["broadcast_log"].insert(0,(kind,f"[{now.strftime('%H:%M:%S')}] {atype} · {d} · {', '.join(chan)}"))
                st.success(f"✅ Sent to {len(tdist)} districts via {len(chan)} channels")
                st.toast(f"{atype} issued for {len(tdist)} districts",icon="📡")
                st.rerun()
    with bc2:
        st.markdown('<div class="cmd-hdr">■ BROADCAST LOG</div>',unsafe_allow_html=True)
        for kind,entry in st.session_state["broadcast_log"][:18]:
            st.markdown(f'<div class="log-e {kind}">{entry}</div>',unsafe_allow_html=True)
        if not st.session_state["broadcast_log"]:
            st.markdown('<div class="log-e">// No broadcasts yet</div>',unsafe_allow_html=True)
        if st.button("🗑️ Clear Log"):
            st.session_state["broadcast_log"]=[]; st.rerun()
    if not map_data.empty:
        st.markdown("---")
        af=map_data.groupby("Risk Level").size().reset_index(name="Count")
        fig_a=px.bar(af,x="Risk Level",y="Count",color="Risk Level",text="Count",
            color_discrete_map={"Low":"#00e676","Moderate":"#ffb300","High":"#ff3737"})
        fig_a.update_traces(textposition="outside",textfont=dict(color="#e8f4fd"))
        fig_a.update_layout(height=220,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=11),showlegend=False,
            margin=dict(l=0,r=0,t=8,b=0),xaxis=dict(gridcolor="#1a3a5c"),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_a,use_container_width=True)

# ─────────────────────────────────────────────
# TAB 7 – RELIEF CAMPS
# ─────────────────────────────────────────────
with tab_camp:
    st.markdown("### 🏕️ Relief Camp Management Dashboard")
    ca1,ca2=st.columns([2,1])
    with ca1:
        st.markdown('<div class="cmd-hdr">■ ALL CAMPS STATUS</div>',unsafe_allow_html=True)
        for camp,d in RELIEF_CAMPS_DATA.items():
            occ_pct=d["occupied"]/d["capacity"]*100
            css="camp-crit" if d["status"]=="Critical" else "camp-std" if d["status"]=="Standby" else "camp-ok"
            badge=f'<span style="color:#ff3737;font-weight:700;">⚠ CRITICAL</span>' if d["status"]=="Critical" else \
                  f'<span style="color:#00e676;font-weight:700;">✓ ACTIVE</span>' if d["status"]=="Active" else \
                  f'<span style="color:#00b4ff;font-weight:700;">◎ STANDBY</span>'
            bar_col="#ff3737" if occ_pct>90 else "#ffb300" if occ_pct>70 else "#00e676"
            st.markdown(f"""
            <div class="{css}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <div class="camp-name" style="color:#e8f4fd;">{camp}</div>{badge}
              </div>
              <div class="camp-stat" style="font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#7fb3d3;">
                <div style="display:flex;gap:20px;flex-wrap:wrap;">
                  <span>OCCUPANCY <b style="color:#e8f4fd;">{d['occupied']}/{d['capacity']}</b> ({occ_pct:.0f}%)</span>
                  <span>FOOD <b style="color:{'#ff3737' if d['food_days']<=2 else '#ffb300' if d['food_days']<=4 else '#00e676'};">{d['food_days']} days</b></span>
                  <span>WATER <b style="color:{'#ff3737' if d['water_kl']<=4 else '#ffb300' if d['water_kl']<=8 else '#00e676'};">{d['water_kl']}kL</b></span>
                  <span>MED KITS <b style="color:{'#ff3737' if d['medicine_kits']<=25 else '#00e676'};">{d['medicine_kits']}</b></span>
                </div>
                <div style="margin-top:6px;background:#071525;border-radius:3px;height:5px;overflow:hidden;">
                  <div style="width:{occ_pct}%;height:100%;background:{bar_col};border-radius:3px;"></div>
                </div>
              </div>
            </div>""",unsafe_allow_html=True)
    with ca2:
        total_occ=sum(v["occupied"] for v in RELIEF_CAMPS_DATA.values())
        total_cap=sum(v["capacity"] for v in RELIEF_CAMPS_DATA.values())
        crit_c=sum(1 for v in RELIEF_CAMPS_DATA.values() if v["status"]=="Critical")
        st.metric("Total Occupancy",f"{total_occ}/{total_cap}",f"{total_occ*100//total_cap}% Full")
        st.metric("Critical Camps",crit_c,"Need Resupply")
        st.metric("Available Capacity",total_cap-total_occ,"Beds Free")
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ ADD NEW CAMP</div>',unsafe_allow_html=True)
        nc_name=st.text_input("Camp Name",placeholder="e.g. Madurai-C2")
        nc_dist=st.selectbox("District",list(TN_CITIES.keys()),key="ncd")
        nc_cap =st.number_input("Capacity",100,2000,300,step=50)
        if st.button("➕ Register Camp",use_container_width=True):
            if nc_name:
                RELIEF_CAMPS_DATA[nc_name]={"district":nc_dist,"capacity":nc_cap,"occupied":0,
                    "food_days":10,"water_kl":30,"medicine_kits":100,"status":"Standby"}
                st.success(f"✅ Camp '{nc_name}' registered!")
                st.rerun()

# ─────────────────────────────────────────────
# TAB 8 – RESCUE OPS & MISSING PERSONS
# ─────────────────────────────────────────────
with tab_mp:
    st.markdown("### 🔍 Rescue Operations & Missing Persons Tracker")
    mp1,mp2=st.columns([1,1])
    with mp1:
        st.markdown('<div class="cmd-hdr">■ MISSING PERSONS REGISTRY</div>',unsafe_allow_html=True)
        for p in st.session_state["missing_persons"]:
            css="mp-found" if p["status"]=="Found Safe" else "mp-card"
            ico="✅" if p["status"]=="Found Safe" else "🔍"
            st.markdown(f"""<div class="{css}">
            <div style="display:flex;justify-content:space-between;">
              <div style="font-family:'Exo 2',sans-serif;font-weight:700;color:#e8f4fd;">{ico} {p['name']}</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#7fb3d3;">{p['id']} · {p['time']}</div>
            </div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#7fb3d3;line-height:1.8;margin-top:4px;">
              <span>Age: {p['age']} · District: {p['district']}</span><br>
              <span>Last Seen: {p['last_seen']}</span><br>
              <span>Contact: {p['reported_by']}</span>
            </div></div>""",unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ REPORT MISSING PERSON</div>',unsafe_allow_html=True)
        with st.form("mp_form"):
            mn =st.text_input("Full Name")
            ma =st.number_input("Age",1,120,30)
            mdi=st.selectbox("District",list(TN_CITIES.keys()),key="mpd")
            mls=st.text_input("Last Seen Location")
            mrb=st.text_input("Reporter Contact (Name & Phone)")
            if st.form_submit_button("📋 Register"):
                if mn:
                    new_id=f"MP-{len(st.session_state['missing_persons'])+1:03d}"
                    st.session_state["missing_persons"].append({"id":new_id,"name":mn,"age":ma,
                        "district":mdi,"last_seen":mls,"reported_by":mrb,"status":"Missing","time":now.strftime("%H:%M")})
                    st.session_state["broadcast_log"].insert(0,("alert",f"[{now.strftime('%H:%M:%S')}] MISSING · {mn} · {mdi}"))
                    st.success(f"✅ Registered {new_id}")
                    st.rerun()
    with mp2:
        st.markdown('<div class="cmd-hdr">■ ACTIVE RESCUE OPERATIONS</div>',unsafe_allow_html=True)
        for op in st.session_state["rescue_ops"]:
            is_active=op["status"]=="Active"
            border_c="#00b4ff" if is_active else "#00e676"
            st.markdown(f"""<div style="background:rgba(13,30,46,.9);border:1px solid {border_c};border-left:3px solid {border_c};
            border-radius:5px;padding:12px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="font-family:'Exo 2',sans-serif;font-weight:700;color:#e8f4fd;">{op['team']}</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:.63rem;color:{'#00b4ff' if is_active else '#00e676'};">
                {'◉ ACTIVE' if is_active else '✓ COMPLETED'}</div>
            </div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#7fb3d3;line-height:1.9;margin-top:5px;">
              <span>ID: {op['id']} · District: {op['district']} · Start: {op['start']}</span><br>
              <span>Mission: {op['operation']}</span><br>
              <span>Persons Rescued: <b style="color:#00ffd5;font-size:.85rem;">{op['persons_rescued']}</b></span>
            </div></div>""",unsafe_allow_html=True)
        st.markdown("---")
        total_res=sum(o["persons_rescued"] for o in st.session_state["rescue_ops"])
        active_ops=sum(1 for o in st.session_state["rescue_ops"] if o["status"]=="Active")
        st.metric("Total Persons Rescued",total_res)
        st.metric("Active Operations",active_ops)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ LOG NEW RESCUE OPERATION</div>',unsafe_allow_html=True)
        with st.form("ro_form"):
            rt=st.text_input("Team Name",placeholder="e.g. NDRF Team Delta")
            rd=st.selectbox("District",list(TN_CITIES.keys()),key="rod")
            rm=st.text_input("Mission Description")
            if st.form_submit_button("➕ Add Operation"):
                if rt:
                    new_roid=f"RO-{len(st.session_state['rescue_ops'])+1:03d}"
                    st.session_state["rescue_ops"].append({"id":new_roid,"team":rt,"district":rd,
                        "persons_rescued":0,"operation":rm,"status":"Active","start":now.strftime("%H:%M")})
                    st.session_state["broadcast_log"].insert(0,("info",f"[{now.strftime('%H:%M:%S')}] RESCUE OP · {rt} · {rd}"))
                    st.success(f"✅ {new_roid} registered"); st.rerun()

# ─────────────────────────────────────────────
# TAB 9 – FLEET TRACKING
# ─────────────────────────────────────────────
with tab_fleet:
    st.markdown("### 🚘 Vehicle & Fleet Tracking")
    ft1,ft2=st.columns([2,1])
    with ft1:
        st.markdown('<div class="cmd-hdr">■ FLEET STATUS BOARD</div>',unsafe_allow_html=True)
        rows=""
        for vid,v in VEHICLES.items():
            sbadge={"Deployed":'<span class="veh-dep">DEPLOYED</span>',"Available":'<span class="veh-avl">AVAILABLE</span>',
                    "Maintenance":'<span class="veh-mtn">MAINTENANCE</span>',"En Route":'<span class="veh-enr">EN ROUTE</span>'}.get(v["status"],'<span class="veh-dep">UNKNOWN</span>')
            fuel_c="#ff3737" if v["fuel"]<35 else "#ffb300" if v["fuel"]<60 else "#00e676"
            rows+=f"""<tr style="border-bottom:1px solid #1a3a5c;">
            <td style="padding:7px 10px;font-family:'Share Tech Mono',monospace;font-size:.7rem;color:#5dc8ff;">{vid}</td>
            <td style="padding:7px 10px;font-family:'Rajdhani',sans-serif;font-weight:600;color:#e8f4fd;">{v['type']}</td>
            <td style="padding:7px 10px;font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#7fb3d3;">{v['district']}</td>
            <td style="padding:7px 10px;font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#7fb3d3;">{v['driver']}</td>
            <td style="padding:7px 10px;">{sbadge}</td>
            <td style="padding:7px 10px;"><div style="display:flex;align-items:center;gap:6px;">
              <div style="width:60px;height:5px;background:#071525;border-radius:3px;overflow:hidden;">
                <div style="width:{v['fuel']}%;height:100%;background:{fuel_c};border-radius:3px;"></div></div>
              <span style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:{fuel_c};">{v['fuel']}%</span>
            </div></td>
            <td style="padding:7px 10px;font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#3a6a8a;">{v['last_update']}</td>
            </tr>"""
        st.markdown(f"""<div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;background:rgba(13,30,46,.8);border-radius:6px;overflow:hidden;">
        <thead><tr style="background:#071525;border-bottom:2px solid #1a3a5c;">
          {"".join(f'<th style="padding:8px 10px;text-align:left;font-family:Share Tech Mono,monospace;font-size:.63rem;color:#5dc8ff;text-transform:uppercase;letter-spacing:.1em;">{h}</th>' for h in ["ID","Type","District","Driver","Status","Fuel","Updated"])}
        </tr></thead><tbody>{rows}</tbody></table></div>""",unsafe_allow_html=True)
    with ft2:
        st.markdown('<div class="cmd-hdr">■ FLEET SUMMARY</div>',unsafe_allow_html=True)
        for status,clr in [("Deployed","#00b4ff"),("Available","#00e676"),("Maintenance","#ffb300"),("En Route","#ce93d8")]:
            cnt=sum(1 for v in VEHICLES.values() if v["status"]==status)
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:8px 12px;border-left:3px solid {clr};background:rgba(13,30,46,.6);border-radius:3px;margin-bottom:6px;font-family:\'Share Tech Mono\',monospace;font-size:.72rem;"><span style="color:#7fb3d3;">{status}</span><span style="color:{clr};font-weight:700;">{cnt}</span></div>',unsafe_allow_html=True)
        low_fuel=[vid for vid,v in VEHICLES.items() if v["fuel"]<35]
        if low_fuel:
            st.markdown("---")
            st.markdown('<div class="cmd-hdr">⚠️ LOW FUEL ALERT</div>',unsafe_allow_html=True)
            for vid in low_fuel:
                st.markdown(f'<div style="background:rgba(255,55,55,.07);border:1px solid rgba(255,55,55,.3);border-radius:4px;padding:7px 11px;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;font-size:.68rem;color:#ff8a8a;">⛽ {vid} · {VEHICLES[vid]["fuel"]}% fuel</div>',unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ VEHICLE TYPE BREAKDOWN</div>',unsafe_allow_html=True)
        vtype_cnt={}
        for v in VEHICLES.values():
            vtype_cnt[v["type"]]=vtype_cnt.get(v["type"],0)+1
        fig_vt=go.Figure(go.Bar(x=list(vtype_cnt.values()),y=list(vtype_cnt.keys()),orientation="h",
            marker_color=["#00b4ff","#00ffd5","#ffb300","#ff3737","#00e676"],
            text=list(vtype_cnt.values()),textposition="outside",textfont=dict(color="#e8f4fd",size=10)))
        fig_vt.update_layout(height=200,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=9),margin=dict(l=0,r=40,t=4,b=0),
            xaxis=dict(gridcolor="#1a3a5c"),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_vt,use_container_width=True)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ VOLUNTEER PORTAL</div>',unsafe_allow_html=True)
        with st.form("vol_form"):
            vname=st.text_input("Volunteer Name")
            vph  =st.text_input("Phone Number")
            vskll=st.multiselect("Skills",["Medical","Rescue","Logistics","Communication","Cooking","Driving"])
            vdist=st.selectbox("Available District",list(TN_CITIES.keys()),key="vd")
            if st.form_submit_button("🙋 Register Volunteer"):
                if vname:
                    st.session_state["volunteers"].append({"name":vname,"phone":vph,"skills":vskll,"district":vdist,"registered":now.strftime("%H:%M")})
                    st.success(f"✅ {vname} registered!")
                    st.rerun()
        if st.session_state["volunteers"]:
            vdf=pd.DataFrame(st.session_state["volunteers"])
            vdf["skills"]=vdf["skills"].apply(lambda x:", ".join(x))
            st.dataframe(vdf,use_container_width=True,height=160,hide_index=True)

# ─────────────────────────────────────────────
# TAB 10 – SUPPLY CHAIN
# ─────────────────────────────────────────────
with tab_supply:
    st.markdown("### 📦 Supply Chain & Inventory Tracker")
    sc1,sc2=st.columns([2,1])
    with sc1:
        st.markdown('<div class="cmd-hdr">■ LIVE SUPPLY STATUS</div>',unsafe_allow_html=True)
        for item,d in SUPPLY_CHAIN.items():
            in_transit=d["dispatched"]-d["delivered"]
            remaining=d["total"]-d["delivered"]
            deliv_pct=d["delivered"]/d["total"]*100
            is_low=(remaining<=d["reorder_at"])
            border="#ff3737" if is_low else "#1a3a5c"
#             st.markdown(f"""
# <div style="background:rgba(13,30,46,.8);border:1px solid {border};border-radius:6px;padding:12px 16px;margin-bottom:8px;">
    
#     <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
      
#       <div style="font-family:'Exo 2',sans-serif;font-weight:700;color:#e8f4fd;">{item}
#         {'<span style="margin-left:8px;background:rgba(255,55,55,.15);border:1px solid #ff3737;border-radius:3px;padding:1px 6px;font-size:.6rem;font-family:\\"Share Tech Mono\\",monospace;color:#ff3737;">⚠ REORDER</span>' if is_low else ''}
#       </div>
      
#       <div style="font-family:'Share Tech Mono',monospace;font-size:.7rem;color:#5dc8ff;">
#         {d['delivered']:,} / {d['total']:,} {d['unit']} delivered
#       </div>

#     </div>

#     <div style="display:flex;gap:16px;margin-bottom:8px;font-family:'Share Tech Mono',monospace;font-size:.67rem;color:#7fb3d3;">
#       <span>Total Stock: <b style="color:#e8f4fd;">{d['total']:,}</b></span>
#       <span>Dispatched: <b style="color:#00b4ff;">{d['dispatched']:,}</b></span>
#       <span>In Transit: <b style="color:#ffb300;">{in_transit:,}</b></span>
#       <span>Remaining: <b style="color:{'#ff3737' if is_low else '#00e676'};">{remaining:,}</b></span>
#     </div>

#     <div style="background:#071525;border-radius:3px;height:6px;overflow:hidden;">
#       <div style="width:{deliv_pct}%;height:100%;background:{'#ff3737' if is_low else '#00e676'};border-radius:3px;"></div>
#     </div>

# </div>
# """, unsafe_allow_html=True)
    with sc2:
        st.markdown('<div class="cmd-hdr">■ SUPPLY SUMMARY</div>',unsafe_allow_html=True)
        total_items=len(SUPPLY_CHAIN)
        low_items=[k for k,v in SUPPLY_CHAIN.items() if (v["total"]-v["delivered"])<=v["reorder_at"]]
        st.metric("Total Categories",total_items)
        st.metric("⚠️ Low Stock Alerts",len(low_items))
        overall_deliv=sum(v["delivered"] for v in SUPPLY_CHAIN.values())
        overall_disp =sum(v["dispatched"] for v in SUPPLY_CHAIN.values())
        st.metric("Total Delivered",f"{overall_deliv:,} units")
        st.metric("In Transit",f"{overall_disp-overall_deliv:,} units")
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ DELIVERY PROGRESS</div>',unsafe_allow_html=True)
        sc_df=pd.DataFrame([(k,v["delivered"]/v["total"]*100) for k,v in SUPPLY_CHAIN.items()],columns=["Item","Delivery%"])
        fig_sc=go.Figure(go.Bar(x=sc_df["Delivery%"],y=sc_df["Item"],orientation="h",
            marker_color=["#ff3737" if x<50 else "#ffb300" if x<75 else "#00e676" for x in sc_df["Delivery%"]],
            text=[f"{x:.0f}%" for x in sc_df["Delivery%"]],textposition="outside",
            textfont=dict(color="#e8f4fd",size=9)))
        fig_sc.update_layout(height=260,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,21,32,.5)",
            font=dict(color="#7fb3d3",family="Share Tech Mono",size=9),margin=dict(l=0,r=50,t=4,b=0),
            xaxis=dict(gridcolor="#1a3a5c",range=[0,115]),yaxis=dict(gridcolor="#1a3a5c"))
        st.plotly_chart(fig_sc,use_container_width=True)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ LOG SUPPLY DISPATCH</div>',unsafe_allow_html=True)
        with st.form("sup_form"):
            si=st.selectbox("Item",list(SUPPLY_CHAIN.keys()),key="sitem")
            sq=st.number_input("Quantity Dispatched",1,100000,500)
            sd=st.selectbox("To District",list(TN_CITIES.keys()),key="sdist")
            if st.form_submit_button("📤 Log Dispatch"):
                SUPPLY_CHAIN[si]["dispatched"]=min(SUPPLY_CHAIN[si]["dispatched"]+sq, SUPPLY_CHAIN[si]["total"])
                st.session_state["broadcast_log"].insert(0,("info",f"[{now.strftime('%H:%M:%S')}] DISPATCH · {sq} {si} → {sd}"))
                st.success(f"✅ {sq} {SUPPLY_CHAIN[si]['unit']} of {si} dispatched to {sd}"); st.rerun()

# ─────────────────────────────────────────────
# TAB 11 – COMMUNICATIONS LOG + RIVER GAUGES + DAMAGE ASSESSMENT
# ─────────────────────────────────────────────
with tab_comm:
    st.markdown("### 📻 Inter-District Communications & River Gauges")
    cc1,cc2=st.columns([3,2])
    with cc1:
        st.markdown('<div class="cmd-hdr">■ INTER-DISTRICT COMMUNICATION LOG</div>',unsafe_allow_html=True)
        pri_filter=st.multiselect("Priority",["HIGH","MEDIUM","LOW"],default=["HIGH","MEDIUM","LOW"],key="pf")
        for msg in st.session_state["comm_log"]:
            if msg["priority"] not in pri_filter:
                continue
            pri_css={"HIGH":"pri-high","MEDIUM":"pri-med","LOW":"pri-low"}.get(msg["priority"],"pri-low")
            stat_c={"Acknowledged":"#00e676","Sent":"#00b4ff","Pending":"#ffb300","Escalated":"#ff3737"}.get(msg["status"],"#aaa")
            st.markdown(f"""<div style="background:rgba(13,30,46,.8);border:1px solid #1a3a5c;border-radius:5px;padding:11px 14px;margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
              <div style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#5dc8ff;">{msg['time']} · {msg['channel']} · <span class="{pri_css}">{msg['priority']}</span></div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:.63rem;color:{stat_c};">● {msg['status']}</div>
            </div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#7fb3d3;">
              <b style="color:#e8f4fd;">{msg['from']}</b> → <b style="color:#e8f4fd;">{msg['to']}</b>
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:.9rem;color:#e8f4fd;margin-top:4px;">{msg['message']}</div>
            </div>""",unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ SEND NEW MESSAGE</div>',unsafe_allow_html=True)
        with st.form("comm_form"):
            c1,c2=st.columns(2)
            mfrom=c1.text_input("From",placeholder="e.g. SEOC Control")
            mto  =c2.text_input("To",placeholder="e.g. Chennai Collector")
            c3,c4=st.columns(2)
            mchan=c3.selectbox("Channel",["Phone","Radio","SMS","Email","Broadcast"])
            mpri =c4.selectbox("Priority",["HIGH","MEDIUM","LOW"])
            mbody=st.text_area("Message",height=70)
            if st.form_submit_button("📤 Send Message"):
                if mfrom and mto and mbody:
                    st.session_state["comm_log"].insert(0,{"time":now.strftime("%H:%M"),"from":mfrom,"to":mto,
                        "channel":mchan,"priority":mpri,"message":mbody,"status":"Sent"})
                    st.session_state["broadcast_log"].insert(0,("info",f"[{now.strftime('%H:%M:%S')}] MSG · {mfrom}→{mto} · {mpri}"))
                    st.success("✅ Message logged."); st.rerun()
    with cc2:
        st.markdown('<div class="cmd-hdr">■ RIVER GAUGE LEVELS</div>',unsafe_allow_html=True)
        for gauge,d in RIVER_GAUGES.items():
            level_pct=(d["current"]-d["normal"])/(d["danger"]-d["normal"])*100 if d["danger"]!=d["normal"] else 0
            level_pct=max(0,min(100,level_pct))
            if d["current"]>=d["danger"]:       gc,gst="var(--red)","DANGER"; gico="🔴"
            elif d["current"]>=d["warning"]:    gc,gst="var(--amber)","WARNING"; gico="🟡"
            else:                                gc,gst="var(--green)","NORMAL";  gico="🟢"
            trend_ico={"rising":"↑","falling":"↓","stable":"→"}.get(d["trend"],"→")
            trend_c={"rising":"#ff3737","falling":"#00e676","stable":"#ffb300"}.get(d["trend"],"#aaa")
            st.markdown(f"""<div style="background:rgba(13,30,46,.8);border:1px solid #1a3a5c;border-left:3px solid {gc};
            border-radius:5px;padding:10px 13px;margin-bottom:7px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#e8f4fd;font-size:.9rem;">{gico} {gauge}</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:.72rem;color:{gc};font-weight:700;">{gst} 
                <span style="color:{trend_c};">{trend_ico} {d['trend'].upper()}</span>
              </div>
            </div>
            <div style="display:flex;justify-content:space-between;font-family:'Share Tech Mono',monospace;font-size:.67rem;color:#7fb3d3;margin:5px 0;">
              <span>CURR <b style="color:{gc};">{d['current']}m</b></span>
              <span>WARN <b style="color:#ffb300;">{d['warning']}m</b></span>
              <span>DANGER <b style="color:#ff3737;">{d['danger']}m</b></span>
            </div>
            <div style="background:#071525;border-radius:3px;height:5px;overflow:hidden;">
              <div style="width:{level_pct}%;height:100%;background:{gc};border-radius:3px;"></div>
            </div></div>""",unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ POST-FLOOD DAMAGE ASSESSMENT</div>',unsafe_allow_html=True)
        with st.form("dmg_form"):
            da1,da2=st.columns(2)
            ddist=da1.selectbox("District",list(TN_CITIES.keys()),key="dd2")
            dblock=da2.text_input("Block/Village",placeholder="e.g. Velankanni Block")
            da3,da4=st.columns(2)
            dhouses=da3.number_input("Houses Damaged",0,10000,0)
            dcrop  =da4.number_input("Crop Area (acres)",0,50000,0)
            da5,da6=st.columns(2)
            droad  =da5.number_input("Roads Damaged (km)",0,500,0)
            ddeaths=da6.number_input("Casualties",0,500,0)
            ddesc  =st.text_area("Observations",height=55,placeholder="Additional damage details...")
            if st.form_submit_button("📋 Submit Assessment"):
                st.session_state["damage_reports"].append({
                    "dist":ddist,"block":dblock,"houses":dhouses,"crop":dcrop,
                    "roads":droad,"deaths":ddeaths,"desc":ddesc,"time":now.strftime("%H:%M")})
                st.session_state["broadcast_log"].insert(0,("warn",f"[{now.strftime('%H:%M:%S')}] DAMAGE REPORT · {ddist}/{dblock}"))
                st.success("✅ Assessment submitted.")
                st.rerun()
        if st.session_state["damage_reports"]:
            st.markdown(f"**{len(st.session_state['damage_reports'])} reports filed:**")
            df_dmg=pd.DataFrame(st.session_state["damage_reports"])
            st.dataframe(df_dmg,use_container_width=True,height=120,hide_index=True)

# ─────────────────────────────────────────────
# TAB 12 – AI ASSISTANT
# ─────────────────────────────────────────────
with tab_ai:
    st.markdown("### 🤖 SEOC AI Field Assistant")
    ai1,ai2=st.columns([2,1])
    with ai1:
        st.markdown("""<div style="background:rgba(13,30,46,.8);border:1px solid #1a3a5c;border-radius:8px;padding:14px;margin-bottom:16px;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:.68rem;color:#5dc8ff;margin-bottom:6px;">■ SEOC AI ASSISTANT v2.0 — FIELD BRIEFING SYSTEM</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:.88rem;color:#7fb3d3;">
        Ask me about: high-risk districts · relief camps · missing persons · supply chain · river levels · vehicle fleet · rescue ops · situation summary · emergency contacts
        </div></div>""",unsafe_allow_html=True)

        # Chat history display
        chat_container=st.container()
        with chat_container:
            for entry in st.session_state["chat_history"]:
                if entry["role"]=="user":
                    st.markdown(f'<div style="text-align:right;"><div class="chat-label" style="text-align:right;">FIELD OPERATOR</div><div class="chat-bubble-user">{entry["content"]}</div></div>',unsafe_allow_html=True)
                else:
                    st.markdown(f'<div><div class="chat-label">SEOC AI</div><div class="chat-bubble-ai">{entry["content"]}</div></div>',unsafe_allow_html=True)

        with st.form("chat_form",clear_on_submit=True):
            user_q=st.text_input("Your query",placeholder="e.g. Which districts are at high risk right now?",label_visibility="collapsed")
            submitted=st.form_submit_button("⚡ Send",use_container_width=True)
            if submitted and user_q.strip():
                ai_resp=ai_chatbot_response(user_q.strip(), map_data)
                st.session_state["chat_history"].append({"role":"user","content":user_q.strip()})
                st.session_state["chat_history"].append({"role":"assistant","content":ai_resp})
                st.rerun()

        if st.session_state["chat_history"]:
            if st.button("🗑️ Clear Chat"):
                st.session_state["chat_history"]=[]; st.rerun()

    with ai2:
        st.markdown('<div class="cmd-hdr">■ QUICK BRIEFINGS</div>',unsafe_allow_html=True)
        shortcuts=[("📋 Situation Summary","situation summary"),("🔴 High Risk Districts","high risk districts"),
                   ("🏕️ Camp Status","relief camp status"),("📦 Supply Alerts","supply chain"),
                   ("🌊 River Levels","river gauge levels"),("🚘 Fleet Status","vehicle fleet"),
                   ("🔍 Missing Persons","missing persons"),("📞 Emergency Contacts","helpline")]
        for label,query in shortcuts:
            if st.button(label,use_container_width=True,key=f"sc_{query}"):
                resp=ai_chatbot_response(query,map_data)
                st.session_state["chat_history"].append({"role":"user","content":label})
                st.session_state["chat_history"].append({"role":"assistant","content":resp})
                st.rerun()
        st.markdown("---")
        st.markdown('<div class="cmd-hdr">■ STAFF ON DUTY</div>',unsafe_allow_html=True)
        current_shift="Morning (06:00–14:00)"
        if 14<=now.hour<22: current_shift="Afternoon (14:00–22:00)"
        elif now.hour>=22 or now.hour<6: current_shift="Night (22:00–06:00)"
        st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:.65rem;color:#00ffd5;margin-bottom:8px;">ACTIVE SHIFT: {current_shift}</div>',unsafe_allow_html=True)
        for staff in STAFF_SHIFTS.get(current_shift,[]):
            st.markdown(f"""<div style="background:rgba(13,30,46,.7);border:1px solid #1a3a5c;border-radius:4px;
            padding:7px 10px;margin-bottom:5px;font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#7fb3d3;">
            <div style="color:#e8f4fd;font-weight:700;font-family:'Rajdhani',sans-serif;">{staff['name']}</div>
            <div>{staff['role']} · {staff['district']}</div>
            <div style="color:#5dc8ff;">{staff['contact']}</div>
            </div>""",unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="margin-top:28px;padding:14px 24px;border-top:1px solid #1a3a5c;
font-family:'Share Tech Mono',monospace;font-size:.62rem;color:#3a6a8a;
display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
  <span>🛡️ TN SEOC · AI DIVISION · BUILD 2025.06 · v4.0</span>
  <span>DATA: OpenWeatherMap API · ML MODEL: Flood Prediction v2 · 38 Districts</span>
  <span>📞 EMERGENCY: 1070 · AMBULANCE: 108 · POLICE: 100 · COAST GUARD: 1554</span>
</div>""",unsafe_allow_html=True)