import streamlit as st
import os
import google.generativeai as ggi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load Gemini API key from secrets
fetch_api_key = st.secrets["gemini_api_key"]

# Configure Gemini API
ggi.configure(api_key=fetch_api_key)

# Initialize Gemini model
model = ggi.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Function to get LLM response
def LLM_Response(question, context=None):
    if context:
        response = chat.send_message(question, context=context, stream=True)
    else:
        response = chat.send_message(question, stream=True)
    return response

# Function to check relevance
def check_relevance(initial_prompt, new_message):
    # Tokenize the initial prompt and new message
    initial_tokens = word_tokenize(initial_prompt.lower())
    new_tokens = word_tokenize(new_message.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    initial_tokens = [token for token in initial_tokens if token not in stop_words]
    new_tokens = [token for token in new_tokens if token not in stop_words]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    initial_tokens = [lemmatizer.lemmatize(token) for token in initial_tokens]
    new_tokens = [lemmatizer.lemmatize(token) for token in new_tokens]

    # Check if any of the new tokens match the initial tokens
    for token in new_tokens:
        if token in initial_tokens:
            return True

    return False

# Streamlit app title
st.title("SUNY IITG CyberSecurity Lab Procedure Generator")

# Initial user input for lab topic
user_quest = st.text_input("Lab topic")
btn = st.button("Generate")

# Store the initial prompt and context
initial_prompt = None
context = None

if btn and user_quest:
    # Store the initial prompt and context
    initial_prompt = user_quest
    context = chat.start_context(initial_prompt)

    # Get the initial response
    result = LLM_Response(user_quest, context)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)

    # Follow-up question input
    follow_up_quest = st.text_input("Follow-up question")
    follow_up_btn = st.button("Ask")

    if follow_up_btn and follow_up_quest:
        # Check if the follow-up question is relevant to the initial prompt
        if not check_relevance(initial_prompt, follow_up_quest):
            st.error("Please ensure your follow-up question is relevant to the initial topic.")
        else:
            # Get the response to the follow-up question using the stored context
            result = LLM_Response(follow_up_quest, context)
            st.subheader("Response : ")
            for word in result:
                st.text(word.text)
