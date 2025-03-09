from datetime import datetime, timedelta
import streamlit as st
from streamlit_calendar import calendar


def afficherCalendrierSemaine(data):
    # Définir la semaine actuelle (du lundi au dimanche)
    today = datetime.today()
    # Lundi de la semaine
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)  # Dimanche de la semaine

    calendar_options = {
        "editable": False,  # Désactiver l'édition
        "selectable": False,  # Désactiver la sélection
        "headerToolbar": {  # Supprimer les boutons de navigation
            "left": "",
            "center": "title",
            "right": ""
        },
        "initialView": "timeGridWeek",  # Vue semaine
        "validRange": {  # Bloquer sur une seule semaine, incluant le dimanche
            "start": start_of_week.strftime("%Y-%m-%d"),
            "end": end_of_week.strftime("%Y-%m-%d"),
        },
        "slotMinTime": "06:00:00",  # Début affichage
        "slotMaxTime": "20:00:00",  # Fin affichage
        "height": "600px",  # Fixer la hauteur pour éviter le scroll
        "contentHeight": "auto",  # Ajustement automatique
        "allDaySlot": False,  # Supprimer la ligne "Toute la journée"
        "nowIndicator": False,  # Supprimer l'indicateur d'heure actuelle
        "slotEventOverlap": False,  # Empêche les chevauchements d'événements
        "slotMinHeight": 30,  # Ajuste la hauteur des événements
        "expandRows": True,  # Permet aux lignes de s'étendre dynamiquement
        "firstDay": 1,  # Commence la semaine le lundi
    }

    # Liste des événements
    calendar_events = data
    # Affichage du calendrier
    calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=""" 
        .fc-event-time {
            font-weight: bold;
        }
        .fc-event-title {
            font-size: 1rem;
        }
        .fc-toolbar-title {
            font-size: 1.8rem;
            text-transform: uppercase;
        }
        .fc-view-harness {
            max-height: 600px !important;  /* Fixer la hauteur */
            overflow: hidden !important;  /* Empêcher le scroll */
        }
        """,
        key="calendar",
    )

    # Liste déroulante pour choisir un jour
    jour_choisi = st.selectbox("Sélectionne un jour de la semaine", [
                               "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])

    # Filtrer les événements pour le jour choisi en utilisant get() pour éviter les erreurs
    events_du_jour = [
        event for event in calendar_events if event.get("day") == jour_choisi]

    # Ajouter des boutons sous les événements pour le jour choisi
    if events_du_jour:
        for event in events_du_jour:
            if st.button(f"Voir {event['title']}"):
                st.write(f"Vous avez cliqué sur {event['title']}!")
    else:
        st.write(f"Aucun événement pour {jour_choisi}.")