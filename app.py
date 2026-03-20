import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import os
from streamlit_autorefresh import st_autorefresh

# ================== CONFIG ==================
st.set_page_config(page_title="Smart Predictive Maintenance PRO", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏭 Smart Predictive Maintenance System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>AI + IoT Live Simulation Dashboard</h4>", unsafe_allow_html=True)
st.write("---")

DATA_FILE = "machine_data.csv"

# ================== AUTO REFRESH ==================
refresh_rate = 2000  # 2 seconds
count = st_autorefresh(interval=refresh_rate, key="fizzbuzzcounter")

# ================== INIT DATA ==================
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame({
        "Machine": ["A","B","C"],
        "Temperature": [65,72,85],
        "Vibration": [2.1,3.5,5.8],
        "Usage": [4,6,11],
        "Status": ["Healthy","Warning","Critical"]
    })
    df_init.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

# ================== SIDEBAR ==================
st.sidebar.header("⚙️ Control Panel")
mode = st.sidebar.selectbox("Mode", ["Live IoT Simulation", "Manual Input"])
machine = st.sidebar.selectbox("Select Machine", ["Machine A", "Machine B", "Machine C"])

# ================== FUNCTIONS ==================
def predict(temp, vibration, usage):
    if temp > 80 or vibration > 5 or usage > 10:
        return "Critical"
    elif temp > 70 or vibration > 3:
        return "Warning"
    else:
        return "Healthy"

def recommendation(temp, vibration):
    if temp > 80:
        return "Check cooling system immediately"
    elif vibration > 5:
        return "Inspect motor alignment"
    elif temp > 70:
        return "Improve ventilation"
    elif vibration > 3:
        return "Monitor machine vibration"
    else:
        return "Normal operation"

def health_score(temp, vibration, usage):
    return max(0, round(100 - (temp*0.3 + vibration*10 + usage*2), 2))

# ================== DATA INPUT ==================
col1, col2 = st.columns(2)

if mode == "Live IoT Simulation":
    with col1:
        st.subheader("📡 Live IoT Data")

        temp = random.randint(60, 100)
        vibration = round(random.uniform(1, 6), 2)
        usage = random.randint(1, 12)

        # Smooth metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("🌡 Temperature", f"{temp} °C")
        m2.metric("📳 Vibration", f"{vibration} mm/s")
        m3.metric("⏱ Usage", f"{usage} h")

else:
    with col1:
        st.subheader("📥 Manual Input")
        temp = st.slider("Temperature (°C)", 0, 120, 60)
        vibration = st.slider("Vibration", 0.0, 10.0, 2.0)
        usage = st.slider("Usage Hours", 0, 24, 5)

# ================== PROCESS ==================
status = predict(temp, vibration, usage)
score = health_score(temp, vibration, usage)
rec = recommendation(temp, vibration)

# Anomaly
anomaly = None
if temp > 90 or vibration > 6:
    anomaly = "🚨 Anomaly Detected!"

# Save data
new_data = pd.DataFrame({
    "Machine":[machine],
    "Temperature":[temp],
    "Vibration":[vibration],
    "Usage":[usage],
    "Status":[status]
})
df = pd.concat([df, new_data], ignore_index=True)
df.to_csv(DATA_FILE, index=False)

# ================== OUTPUT ==================
with col2:
    st.subheader("📊 Machine Status")

    if status == "Critical":
        st.error(f"❌ {status}")
    elif status == "Warning":
        st.warning(f"⚠️ {status}")
    else:
        st.success(f"✅ {status}")

    st.metric("💯 Health Score", f"{score}/100")
    st.info(f"🛠 {rec}")

    if anomaly:
        st.error(anomaly)

# ================== DASHBOARD ==================
st.write("---")
st.subheader("📊 System Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Total Records", len(df))
c2.metric("Critical Cases", len(df[df["Status"]=="Critical"]))
c3.metric("Warnings", len(df[df["Status"]=="Warning"]))

# ================== LIVE GRAPH ==================
st.write("---")
st.subheader("📈 Live Sensor Trend")

fig, ax = plt.subplots()
ax.plot(df["Temperature"].tail(20), label="Temperature")
ax.plot(df["Vibration"].tail(20), label="Vibration")
ax.legend()

st.pyplot(fig)

# ================== ALERT HISTORY ==================
st.write("---")
st.subheader("🚨 Critical Alerts")

st.dataframe(df[df["Status"]=="Critical"].tail(10))

# ================== DATA ==================
st.subheader("📁 Historical Data")
st.dataframe(df.tail(10))

# ================== FOOTER ==================
st.write("---")
st.markdown("<center>🚀 Real-Time AI + IoT Monitoring Dashboard</center>", unsafe_allow_html=True)