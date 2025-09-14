import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
import json
import datetime

# Example FAQ data - you can load from JSON file if you want
faq_data = {
    "fee": "The college fee details are available on the official website.",
    "admission": "Admissions start in June. Please visit the admission portal.",
    "hostel": "Hostel facilities are available for both boys and girls."
}

# Keywords for better matching
keywords = {
    "fee": ["fee", "fees", "payment", "college fee", "tuition"],
    "admission": ["admission", "apply", "entrance", "registration"],
    "hostel": ["hostel", "accommodation", "stay"]
}

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_text(text, source_lang, target_lang):
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

def get_answer(user_input_en):
    user_input_en = user_input_en.lower()
    for category, kw_list in keywords.items():
        for kw in kw_list:
            if kw in user_input_en:
                return faq_data.get(category)
    return "Sorry, I don't know that. Please contact admin office."

def log_conversation(user, bot):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] USER: {user}\nBOT: {bot}\n\n")

# Streamlit UI
st.set_page_config(page_title="College Multilingual Chatbot", page_icon="🎓")
st.title("🎓 College Multilingual Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    lang = detect_language(user_input)
    user_input_en = translate_text(user_input, source_lang=lang, target_lang="en")
    answer_en = get_answer(user_input_en)
    answer_final = answer_en
    if lang != "en":
        answer_final = translate_text(answer_en, source_lang="en", target_lang=lang)

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": answer_final})
    log_conversation(user_input, answer_final)

    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(answer_final)

# Download logs
try:
    with open("chat_logs.txt", "r", encoding="utf-8") as f:
        logs = f.read()
    st.download_button("📥 Download Chat Logs", logs, file_name="chat_logs.txt")
except FileNotFoundError:
    st.info("No logs yet.")
