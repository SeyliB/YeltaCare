import streamlit as st
from pymongo import MongoClient
import bcrypt

# Connexion à MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://yelta:Phutsrbpnzg820wH@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.YeltaCare
    return db.Users

# Hacher un mot de passe
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Vérifier un mot de passe
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Créer un nouvel utilisateur
def create_user(username, password):
    users = connect_to_mongodb()
    if users.find_one({"username": username}):
        return False  # L'utilisateur existe déjà
    hashed_password = hash_password(password)
    users.insert_one({"username": username, "password": hashed_password})
    return True

# Authentifier un utilisateur
def authenticate_user(username, password):
    users = connect_to_mongodb()
    user = users.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True
    return False

# Interface Streamlit
def main():
    st.title("🍎 Nutrition Intelligente - Connexion")

    # Menu de navigation
    menu = ["Connexion", "Inscription"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Connexion":
        st.subheader("Connexion")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            if authenticate_user(username, password):
                st.success(f"Bienvenue, {username} !")
                # Rediriger vers l'application principale
                st.write("Vous êtes maintenant connecté.")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

    elif choice == "Inscription":
        st.subheader("Créer un compte")
        new_username = st.text_input("Choisissez un nom d'utilisateur")
        new_password = st.text_input("Choisissez un mot de passe", type="password")
        confirm_password = st.text_input("Confirmez le mot de passe", type="password")
        if st.button("S'inscrire"):
            if new_password == confirm_password:
                if create_user(new_username, new_password):
                    st.success("Compte créé avec succès !")
                    st.info("Connectez-vous pour accéder à l'application.")
                else:
                    st.error("Ce nom d'utilisateur est déjà pris.")
            else:
                st.error("Les mots de passe ne correspondent pas.")

if __name__ == "__main__":
    main()