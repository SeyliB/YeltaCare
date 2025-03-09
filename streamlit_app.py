import streamlit as st
import user
import informations

def goto(page):
    st.session_state.page = page
    st.rerun()  # Forcer le rechargement de la page

# Gestion de la navigation
def main():
    # Initialisation de l'état de session pour la navigation
    if "page" not in st.session_state:
        st.session_state.page = "connexion"

    # Afficher l'interface correspondante
    if st.session_state.page == "connexion":
        user.login_interface()
    elif st.session_state.page == "inscription":
        user.register_interface()
    elif st.se:
        informations.

if __name__ == "__main__":
    main()