import streamlit as st
from googletrans import Translator
from langdetect import detect
import json
import datetime

# Load FAQ Data from JSON
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text):
    return translator.translate(text, dest="en").text

def translate_back(text, lang):
    if lang == "en":
        return text
    return translator.translate(text, dest=lang).text

def get_answer(user_input):
    user_input = user_input.lower()
    for key in faq_data:
        if key in user_input:
            return faq_data[key]
    return "Sorry, I don't know that. Please contact admin office."

def log_conversation(user, bot):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] USER: {user}\nBOT: {bot}\n\n")

# Streamlit UI
st.set_page_config(page_title="College Multilingual Chatbot", page_icon="🎓")
st.title("🎓 College Multilingual Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Type your message..."):
    lang = detect_language(user_input)
    query_en = translate_to_english(user_input)
    answer_en = get_answer(query_en)
    final_answer = translate_back(answer_en, lang)

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    log_conversation(user_input, final_answer)

    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(final_answer)

# Download logs
try:
    with open("chat_logs.txt", "r", encoding="utf-8") as f:
        logs = f.read()
    st.download_button("📥 Download Chat Logs", logs, file_name="chat_logs.txt")
except FileNotFoundError:
    st.info("No logs yet.")
