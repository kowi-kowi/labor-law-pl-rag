import streamlit as st
import requests

st.set_page_config(page_title="Asystent Prawa Pracy PL", page_icon="⚖️")

st.title("Asystent Prawa Pracy (PL)")
st.write("Zadawaj pytania dotyczące Kodeksu pracy.")

question = st.text_input("Wpisz pytanie:")

if st.button("Zapytaj"):
    if question.strip():
        try:
            response = requests.post("http://<YOUR_VM_IP>:8000/ask", json={"question": question})
            answer = response.json().get("answer", "Brak odpowiedzi")
            st.markdown(f"**Odpowiedź:**\n{answer}")
        except Exception as e:
            st.error(f"Błąd połączenia z backend: {e}")