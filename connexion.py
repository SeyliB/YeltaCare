import streamlit as st
import time
import streamlit_app as main
import user

# Interface de connexion
def display():
    st.title("🍎 Connexion")
    st.write("Bienvenue ! Connectez-vous pour accéder à l'application.")

    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if user.authenticate_user(username, password):
            st.success(f"Bienvenue, {username} !")
            # Rediriger vers l'application principale
            st.write("Vous êtes maintenant connecté.")
            time.sleep(2)
            main.goto("principal")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

    # Bouton pour aller à l'interface d'inscription
    if st.button("Pas encore de compte ? Inscrivez-vous ici"):
        main.goto("inscription")