import streamlit as st
import requests
import json

# Define the URL of the backend API
API_URL = "http://localhost:8083/api/chat"

gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">simplyChat</div>
"""
st.markdown(gradient_text_html, unsafe_allow_html=True)

model = st.radio(
    "",
    options=["Llama", "GPT-3.5", "Claude-3 Haiku", "Mixtral 8x7B"],
    index=0,
    horizontal=True,
)
st.session_state["model"] = model

# Handle each model's availability
if st.session_state["model"] in ["GPT-3.5", "Claude-3 Haiku", "Mixtral 8x7B"]:
    st.warning(f"🛑 {st.session_state['model']} is still under construction. Please check back later.")
elif st.session_state["model"] == "Llama":
    st.success(f"✅ {st.session_state['model']} is ready to go! Start your chat now.")

with open("ui/sidebar.md", "r") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()

st.sidebar.markdown(sidebar_content)
st.write(styles_content, unsafe_allow_html=True)

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
