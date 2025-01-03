import streamlit as st
import requests
import json
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "ca14625f-5c6c-4641-b161-9506eee5df4f"
FLOW_ID = "6e8bbe2c-690a-43a9-8c5f-66e018ef874d"
# APPLICATION_TOKEN = "AstraCS:zcxlfxzmCQnZrvuxwMLjmZou:d7d24d6a5aee1b03adf60f642bf2d11332fabaa94ecd40657e122df155b1e008"
APPLICATION_TOKEN = os.getenv('APPLICATION_TOKEN')
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# Tweaks Dictionary
TWEAKS = {
    "ChatInput-DWQpc": {},
    "Prompt-XxSEq": {},
    "ChatOutput-mlcoa": {},
    "GoogleGenerativeAIModel-DX1hx": {}
}

# Function to interact with Langflow API
def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }

    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit Main Application
def main():
    st.title("Social Media Performance Analysis")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # # Option to clear chat history
    # if st.button("Clear Chat"):
    #     st.session_state.messages = []

    # User input prompt
    prompt = st.chat_input("Say Something...")
    if prompt:
        # Append user message to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Show a loading spinner while fetching the response
        with st.spinner("Fetching response..."):
            # Get response from Langflow API
            response = run_flow(
                message=prompt,
                endpoint=ENDPOINT or FLOW_ID,
                output_type="chat",
                input_type="chat",
                tweaks=TWEAKS,
                application_token=APPLICATION_TOKEN
            )
            
            # Extract the message from the nested response
            print("Vishal ", response)
            response_content = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "Error: No response from the API")

            # Append assistant's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": response_content})

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if __name__ == "__main__":
    main()
