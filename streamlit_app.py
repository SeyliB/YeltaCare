import streamlit as st
import inscription
import connexion
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
        connexion.display()
    elif st.session_state.page == "inscription":
        inscription.display()
    elif st.session_state.page == "informations":
        informations.display()

if __name__ == "__main__":
    main()