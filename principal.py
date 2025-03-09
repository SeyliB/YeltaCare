import streamlit as st
import user
from database import MongoDB

db = MongoDB()


def display():
    st.write("PRINCIPAL!")
    db.set_collection("Informations")
    data = db.get_document({"username": user.connected})
    st.write(data)  # Output: ["lecture", "natation", "musique"]
    db.set_collection("Informations")
    st.write(db.get_all_data())  # Affiche tous les documents de la collection
