import streamlit as st
import google.generativeai as genai

st.title("📚 Elysian Bookshelf - Librarian Chatbot")
st.subheader("What literary wisdom do you seek today?")

# Capture Gemini API Key
gemini_api_key = "AIzaSyBIcWZ1OAORd7quMfSEw8f875X-SJmamBQ"

# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
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

# Function to recommend books based on themes or genres
def recommend_books(theme):
    # Static book recommendations based on common themes
    book_recommendations = {
        "mystery": [
            "- **The Girl with the Dragon Tattoo** by Stieg Larsson",
            "- **Gone Girl** by Gillian Flynn",
            "- **The Da Vinci Code** by Dan Brown",
            "- **Big Little Lies** by Liane Moriarty",
            "- **In the Woods** by Tana French"
        ],
        "fantasy": [
            "- **The Hobbit** by J.R.R. Tolkien",
            "- **A Game of Thrones** by George R.R. Martin",
            "- **Mistborn** by Brandon Sanderson",
            "- **The Name of the Wind** by Patrick Rothfuss",
            "- **The Night Circus** by Erin Morgenstern"
        ],
        "science fiction": [
            "- **Dune** by Frank Herbert",
            "- **Neuromancer** by William Gibson",
            "- **Ender's Game** by Orson Scott Card",
            "- **The Left Hand of Darkness** by Ursula K. Le Guin",
            "- **Snow Crash** by Neal Stephenson"
        ],
        "romance": [
            "- **Pride and Prejudice** by Jane Austen",
            "- **The Notebook** by Nicholas Sparks",
            "- **Me Before You** by Jojo Moyes",
            "- **Outlander** by Diana Gabaldon",
            "- **The Hating Game** by Sally Thorne"
        ]
    }
    
    return book_recommendations.get(theme.lower(), [])

# Capture user input and generate book recommendations or a chatbot response
if user_input := st.chat_input("Which captivating tale shall we explore? Specify your genre or theme."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Use the recommend_books function to suggest titles based on user input
    if model:
        try:
            # Generate a response using Gemini AI
            ai_response = model.generate_content(user_input)
            ai_response_text = ai_response.text if ai_response else "Alas, the winds of fate are not in your favor today..."

            # Fetch book recommendations
            books = recommend_books(user_input)

            if books:
                book_recommendations = "\n".join(books)
                bot_response = (
                    f"dear seeker of knowledge, here are a few titles that may pique your interest:\n" +
                    book_recommendations +
                    "\n\nAdditionally, I have some thoughts for you:\n" +
                    ai_response_text +
                    "\n\nChoose wisely, for every choice shapes your journey through the realms of literature..."
                )
            else:
                bot_response = (
                    f"Dear seeker of knowledge, perhaps these are the treasures your weary heart has long sought.\n\n" +
                    ai_response_text+
                    "\n\nAs you explore these tales, remember: each narrative mirrors your fleeting pursuits. Choose wisely, for your journey in fiction shapes the essence of your existence."
                )

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.error("Please configure the Gemini API Key to generate a response.")
