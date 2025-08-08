import streamlit as st
from analysis import analyze_mood, get_motivation
import pandas as pd
from datetime import datetime 
import os

DATA_FILE = "data/journal_entries.csv";

st.set_page_config(page_title="Mental Health Journal", layout="centered")
st.title("🧠 Mental Health Journal Analyzer")
st.subheader("Write your thoughts. We'll take care of the insights 💬")
st.sidebar.title("🕓 Journal History")
try:
    df = pd.read_csv(DATA_FILE)
    df = df.sort_values(by="Date", ascending=False)

    with st.sidebar:
        for i, row in df.iterrows():
            with st.expander(f"📝 {row['Date'][:16]}"):
                st.write(row["Entry"])
                st.caption(f"Mood: {row['Mood']} | Score: {row['Score']:.2f}")

except FileNotFoundError:
    st.sidebar.info("No journal entries yet.")

with st.sidebar:
    st.title("📈Mood Over Time")
    st.line_chart(df.set_index("Date")["Score"])

entry = st.text_area("Share your thoughts below",height=200, placeholder="How are you feeling today.....?")
if st.button ("Save Entry"):
    if entry.strip() == "":
        st.error("Please write something...")
    else:
        mood, score = analyze_mood(entry);
        motivation = get_motivation(mood);
    
        if not os.path.exists("data"):
            os.makedirs("data");

        df = pd.DataFrame([[datetime.now(),entry, mood, score]], columns=["Date", "Entry", "Mood", "Score"]);
        df.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False);
        st.success(f"🧭 Mood Detected: {mood} ({score:.2f})")
        st.info(f"✨{motivation}")
