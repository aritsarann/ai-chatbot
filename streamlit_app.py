import streamlit as st
import google.generativeai as genai

st.title("🌿 Elysian Bookshelf - Librarian Chatbot")
st.subheader("What literary wisdom do you seek today?")

# Capture Gemini API Key
gemini_api_key = "AIzaSyBIcWZ1OAORd7quMfSEw8f875X-SJmamBQ"

# Initialize the Gemini Model
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")
        model = None
else:
    model = None  # Set model to None if API key is not provided

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("What knowledge do you seek today?"):
    user_input = user_input.strip()
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Generate response using Gemini
    if model:
        try:
            bot_response = model.generate(user_input)  # Generate based on the user's input
            bot_text = bot_response['message']  # Extract the response message from Gemini
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
            bot_text = "I'm unable to provide recommendations at this time."
        
        st.session_state.chat_history.append(("assistant", bot_text))
        st.chat_message("assistant").markdown(bot_text)