import streamlit as st
import pandas as pd
from datetime import datetime
from agents import WaterTrackerAgent
from database import log_water_intake, get_intake_history
from logger import log_info, log_error

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

if not st.session_state.tracker_started:
    st.title("AI-Powered Water Intake Tracker")
    st.markdown("Track your daily hydration with help of AI assistant. log your water intake and get feedback.")
    user_id = st.text_input("Enter your User ID:")
    if st.button("Start Tracking") and user_id:
        st.session_state.user_id = user_id
        st.session_state.tracker_started = True
        log_info(f"User {user_id} started tracking.")
        st.rerun()
else:
    st.header(f"Welcome, {st.session_state.user_id}!")
    intake_ml = st.number_input("Log Water Intake (ml):", min_value=0, step=100)
    if st.button("Log Intake") and intake_ml > 0:
        try:
            log_water_intake(st.session_state.user_id, intake_ml)
            agent = WaterTrackerAgent()
            feedback = agent.analyze_water_intake(intake_ml)
            st.success(f"Logged {intake_ml} ml. AI Feedback: {feedback}")
            log_info(f"User {st.session_state.user_id} logged {intake_ml} ml.")
        except Exception as e:
            st.error(f"Error logging intake: {e}")
            log_error(f"Error logging intake for user {st.session_state.user_id}: {e}")

    if st.button("View Intake History"):
        try:
            records = get_intake_history(st.session_state.user_id)
            if records:
                df = pd.DataFrame(records, columns=["Intake (ml)","Timestamp"])
                st.table(df)
            else:
                st.info("No intake history found.")
            log_info(f"User {st.session_state.user_id} viewed intake history.")
        except Exception as e:
            st.error(f"Error fetching history: {e}")
            log_error(f"Error fetching history for user {st.session_state.user_id}: {e}")

    if st.button("End Tracking"):
        log_info(f"User {st.session_state.user_id} ended tracking.")
        st.session_state.tracker_started = False
        st.rerun()