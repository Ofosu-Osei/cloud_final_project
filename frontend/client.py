import streamlit as st
import requests
import json

# Define the URL of the backend API
API_URL = "http://backend:8083/api/chat"

st.title('Chat with AI')

# Text input for user prompt
user_input = st.text_input("Enter your prompt:", "")

if st.button('Send'):
    if user_input:
        # Prepare the payload as JSON
        payload = json.dumps({"prompt": user_input})

        # Send the POST request to the backend
        response = requests.post(API_URL, data=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            # Display the response from the backend
            result = response.json()
            st.write("Response:", result['response'])
        else:
            st.error("Failed to get response from the server")
    else:
        st.warning("Please enter a prompt.")
