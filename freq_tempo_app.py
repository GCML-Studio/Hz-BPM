import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Percussive Freq Pro v2", layout="centered")

def generate_click_audio(freq, duration=0.03, sample_rate=44100):
    """Generates a sharp click sound as a numpy array."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Square wave for that dry, sharp percussion you had in the original
    wave = np.sign(np.sin(2 * np.pi * freq * t))
    # Apply a quick fade-out envelope to prevent clicking at the end
    envelope = np.exp(-100 * t)
    audio = (wave * envelope * 0.7).astype(np.float32)
    return audio

st.title("🥁 Percussive Freq Pro v2")

# --- UI Layout ---
col1, col2 = st.columns(2)

with col1:
    freq = st.number_input("Enter Frequency (Hz):", value=2.0, step=0.1)
    beats_per_bar = st.number_input("Beats per Bar:", value=4, step=1)

with col2:
    subdiv = st.selectbox(
        "Frequency Represents:", 
        ["Minims (1/2)", "Crotchets (1/4)", "Quavers (1/8)", "Semiquavers (1/16)"],
        index=1
    )

# --- Calculation Logic ---
raw_bpm = freq * 60
base_interval = 1.0 / freq

if subdiv == "Minims (1/2)":
    bpm = raw_bpm * 2
    interval = base_interval / 2
elif subdiv == "Quavers (1/8)":
    bpm = raw_bpm / 2
    interval = base_interval * 2
elif subdiv == "Semiquavers (1/16)":
    bpm = raw_bpm / 4
    interval = base_interval * 4
else: # Crotchets (1/4)
    bpm = raw_bpm
    interval = base_interval

st.divider()
st.metric("Derived Tempo", f"{round(bpm, 2)} BPM")
st.write(f"**Bars per Minute:** {round(bpm/beats_per_bar, 2)}")

# --- Audio Section ---
st.info("Note: Web-based metronomes can have slight latency compared to desktop apps.")

if st.button("Generate Audio Samples"):
    accent = generate_click_audio(1300)
    normal = generate_click_audio(2600)
    
    st.write("Accent Click (Beat 1)")
    st.audio(accent, sample_rate=44100)
    st.write("Normal Click")
    st.audio(normal, sample_rate=44100)