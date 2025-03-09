import streamlit as st
import time
from database import MongoDB

import streamlit_app as main

db = MongoDB()
id = None

# Hacher un mot de passe
def hash_password(password):
    return True

# Vérifier un mot de passe
def verify_password(password, hashed_password):
    return True

# Créer un nouvel utilisateur
def create_user(username, password):
    query = {"username": username, "password": password}
    list = db.get_data_by_query(query)
    unique = len(list) == 0
    if unique:
        db.insert_data(query)
    return unique

# Authentifier un utilisateur
def authenticate_user(username, password):
    query = {"username": username, "password": password}
    list = db.get_data_by_query(query)
    found = len(list) == 1
    if found:
        id = username
    return found

# Interface de connexion
def login_interface():
    st.title("🍎 Connexion")
    st.write("Bienvenue ! Connectez-vous pour accéder à l'application.")

    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if authenticate_user(username, password):
            st.success(f"Bienvenue, {username} !")
            # Rediriger vers l'application principale
            st.write("Vous êtes maintenant connecté.")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

    # Bouton pour aller à l'interface d'inscription
    if st.button("Pas encore de compte ? Inscrivez-vous ici"):
        main.goto("inscription")

# Interface d'inscription
def register_interface():
    st.title("🍎 Inscription")
    st.write("Créez un compte pour accéder à l'application.")

    # Formulaire d'inscription
    new_username = st.text_input("Choisissez un nom d'utilisateur")
    new_password = st.text_input("Choisissez un mot de passe", type="password")
    confirm_password = st.text_input("Confirmez le mot de passe", type="password")
    if st.button("S'inscrire"):
        if new_password == confirm_password:
            if create_user(new_username, new_password):
                st.success("Compte créé avec succès !")
                st.info("Connectez-vous pour accéder à l'application.")
                main.goto("informations")
            else:
                st.error("Ce nom d'utilisateur est déjà pris.")
        else:
            st.error("Les mots de passe ne correspondent pas.")

    # Bouton pour revenir à l'interface de connexion
    if st.button("Déjà un compte ? Connectez-vous ici"):
        main.goto("connexion")