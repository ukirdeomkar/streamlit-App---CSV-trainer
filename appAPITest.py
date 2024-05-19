import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
# Initialize the model (replace with your actual API key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")


# Define a function to send messages and receive responses with context
def send_message(context, message):
  chat = model.start_chat()
  response = chat.send_message(f"{context}. {message}")
  return response.parts[0].text
# Initialize chat history context window size
context_window_size = 1000

# Streamlit app layout
st.title("Chat with Gemini")

# Input field for user message
user_message = st.text_input("Type your message:")
chat_history = []

# Send message and receive response with context
if user_message:
  # Update chat history
  chat_history.append(user_message)

  # Get context from the chat history window
  context = " ".join(chat_history[-context_window_size:])
  st.write(chat_history[::-1])
  # Send message with context and display response
#   response = send_message(context, user_message)
#   st.write(f"Gemini: {response}")

  # Update chat history with response
#   chat_history.append(response)

# Display chat history (optional)
if chat_history:
  st.write("Chat History:")
  for message in chat_history:
    st.write(f"- {message}")
