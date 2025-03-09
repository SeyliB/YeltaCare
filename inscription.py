import streamlit as st
import streamlit_app as main
import user

# Interface d'inscription
def display():
    st.title("🍎 Inscription")
    st.write("Créez un compte pour accéder à l'application.")

    # Formulaire d'inscription
    new_username = st.text_input("Choisissez un nom d'utilisateur")
    new_password = st.text_input("Choisissez un mot de passe", type="password")
    confirm_password = st.text_input("Confirmez le mot de passe", type="password")
    if st.button("S'inscrire"):
        if new_password == confirm_password:
            if user.create_user(new_username, new_password):
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