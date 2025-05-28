import streamlit as st
from app.db import init_db # Add this import

# Call init_db at the start of your application
init_db() # Add this line

def ping():
    return "OK"

st.title("Retrospective App") # Added a title for clarity
st.write(f"Ping Status: {ping()}")

# Add other Streamlit page logic here as the project progresses
# For now, it's fine to just have the ping.
