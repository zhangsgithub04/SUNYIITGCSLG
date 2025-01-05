import streamlit as st
import os
import google.generativeai as ggi

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
        if initial_prompt.lower() not in follow_up_quest.lower():
            st.error("Please ensure your follow-up question is relevant to the initial topic.")
        else:
            # Get the response to the follow-up question using the stored context
            result = LLM_Response(follow_up_quest, context)
            st.subheader("Response : ")
            for word in result:
                st.text(word.text)
