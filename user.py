import streamlit as st
import database

collection = database.getCollection("Users")
connected = None

# Hacher un mot de passe
def hash_password(password):
    return True

# Vérifier un mot de passe
def verify_password(password, hashed_password):
    return True

# Créer un nouvel utilisateur
def create_user(username, password):
    global connected
    query = {"username": username, "password": password}
    list = collection.get_data_by_query(query)
    unique = len(list) == 0
    if unique:
        connected = username
        collection.insert_data(query)
    return unique

# Authentifier un utilisateur
def authenticate_user(username, password):
    global connected
    query = {"username": username, "password": password}
    list = collection.get_data_by_query(query)
    found = len(list) == 1
    if found:
        connected = username
    return found