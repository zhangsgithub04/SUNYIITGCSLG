
import streamlit as st
import os
import google.generativeai as ggi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize API Key
fetch_api_key = st.secrets["gemini_api_key"]

# Configure the API Key
ggi.configure(api_key=fetch_api_key)

# Initialize Model
model = ggi.GenerativeModel("gemini-pro")

# Initialize Chat
chat = model.start_chat()

# Function to Get Response from LLM
def LLM_Response(question):
    response = chat.send_message(question, stream=True)
    return response

# Title of the App
st.title("SUNY IITG CyberSecurity Lab Procedure Generator")

# Initialize Session State
if "initial_prompt" not in st.session_state:
    st.session_state.initial_prompt = None
if "initial_keywords" not in st.session_state:
    st.session_state.initial_keywords = None

# Function to Extract Keywords
def extract_keywords(prompt):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(prompt.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    keywords = [lemmatizer.lemmatize(t) for t in tokens]
    return keywords

# Text Input for User Question
user_quest = st.text_input("Lab topic")

# Button to Generate Response
btn = st.button("Generate")

if btn and user_quest:
    if not st.session_state.initial_prompt:
        # Store the initial prompt and extract keywords
        st.session_state.initial_prompt = user_quest
        st.session_state.initial_keywords = extract_keywords(user_quest)
        
        # Get Response from LLM for First Prompt
        result = LLM_Response(user_quest)
        st.subheader("Response:")
        for word in result:
            st.text(word.text)
    else:
        # Extract keywords from subsequent prompts
        subsequent_keywords = extract_keywords(user_quest)
        
        # Evaluate relevance by checking keyword overlap
        relevance_threshold = 0.5
        keyword_overlap = len(set(subsequent_keywords) & set(st.session_state.initial_keywords))
        relevance_score = keyword_overlap / len(st.session_state.initial_keywords)
        
        if relevance_score >= relevance_threshold:
            # Get Response from LLM for Subsequent Prompts
            result = LLM_Response(user_quest)
            st.subheader("Response:")
            for word in result:
                st.text(word.text)
        else:
            st.error("Please stay relevant to the initial topic.")
