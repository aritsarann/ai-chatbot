import streamlit as st
import google.generativeai as genai
import requests

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

# Function to search for books with better error handling
def search_books(query):
    api_key = "YOUR_GOOGLE_API_KEY"  # Replace with your actual API key
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        books = response.json().get('items', [])
        
        if not books:
            return []  # No books found
        
        return [
            f"- **{book['volumeInfo']['title']}** by {', '.join(book['volumeInfo'].get('authors', ['Unknown Author']))}"
            for book in books[:5]
        ]
    else:
        st.error("Failed to fetch books. Please try again later.")
        return []


# Capture user input and generate bot response
if user_input := st.chat_input("What knowledge do you seek today?"):
    user_input = user_input.strip()  # Remove whitespace
    if not user_input:
        st.warning("Please enter a valid question.")
    else:
        st.session_state.chat_history.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

    # Use Gemini AI to generate a bot response
    if model:
        try:
            # Search for books based on user input
            books = search_books(user_input)
            
            if books:
                bot_response = (
                    "Ah, dear seeker of knowledge, here are a few titles that may pique your interest:\n" +
                    "\n".join(books) +
                    "\n\nChoose wisely, for every choice shapes your journey through the realms of literature..."
                )
            else:
                bot_response = "Alas, it seems the tomes of knowledge are elusive today. Perhaps you might explore another tale."

            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.error("Please configure the Gemini API Key to generate a response.")