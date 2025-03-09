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