import streamlit as st
import pandas as pd
import os
from gtts import gTTS
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sidebar Logo
st.sidebar.image("https://www.azercell.com/assets/images/services/aicell/webpage_twosided_564x566_aicell.png", use_container_width=True)

# Header with Image
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="https://www.azercell.com/assets/images/services/aicell/webpage_two-sided_564x566_aicell.png" width="80">
        <h1 style="margin-left: 10px; font-size: 38px; font-weight: 800; text-align: center;">Azercell Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Chatbot Styling
st.markdown("""
    <style>
        body {background-color: #f5f5f5;}
        .chat-container {max-width: 700px; margin: auto;}
        .message {padding: 10px; border-radius: 10px; margin-bottom: 10px;}
        .user-message {background-color: #6A0DAD; color: white; text-align: right;}
        .bot-message {background-color: #f0f0f0; color: black;}
    </style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_excel(r'azercell/azercell_app/pages/chatbot.xlsx')

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['rəy_processed'])

# Function to get chatbot answer
def chatbot_answer(user_query):
    user_query_processed = user_query.lower()
    user_query_vec = vectorizer.transform([user_query_processed])
    similarity_scores = cosine_similarity(user_query_vec, X)
    best_match_idx = similarity_scores.argmax()
    return df['ans_processed'].iloc[best_match_idx]

# Session state for user details
if "first_name" not in st.session_state:
    st.session_state.first_name = None
if "last_name" not in st.session_state:
    st.session_state.last_name = None

# Get user details
if not st.session_state.first_name or not st.session_state.last_name:
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("📌 Adınızı daxil edin:")
    with col2:
        last_name = st.text_input("📌 Soyadınızı daxil edin:")

    if first_name and last_name:
        st.session_state.first_name = first_name.strip().capitalize()
        st.session_state.last_name = last_name.strip().capitalize()
        st.success(f"Xoş gəldiniz, {st.session_state.first_name} {st.session_state.last_name}! Sualınızı verə bilərsiniz.")

# Chatbot Interaction
if st.session_state.first_name and st.session_state.last_name:
    user_question = st.text_input("💬 Sualınızı daxil edin:")
    
    if user_question:
        # Get chatbot answer
        answer = chatbot_answer(user_question)
        if 'salam.' in answer:
            answer = answer.replace('salam.', f'Salam, {st.session_state.first_name} {st.session_state.last_name}. ')
        elif 'salam,' in answer:
            answer = answer.replace('salam,', f'Salam, {st.session_state.first_name} {st.session_state.last_name}. ')
        elif 'salam' in answer:
            answer = answer.replace('salam', f'Salam, {st.session_state.first_name} {st.session_state.last_name}. ')

        answer = answer.replace('see more', '')
        # Display text response
        st.markdown(f"<div class='message user-message'><b>{st.session_state.first_name} {st.session_state.last_name}:</b> {user_question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message bot-message'><b>Azercell:</b> {answer}</div>", unsafe_allow_html=True)

        # Convert answer to speech
        tts = gTTS(text=answer, lang='tr')
        tts.save("response.mp3")

        # Play the audio and provide download option
        st.audio("response.mp3", format="audio/mp3")
        st.download_button("🔊 Səsi Yüklə", "response.mp3", file_name="chatbot_response.mp3", mime="audio/mp3")
