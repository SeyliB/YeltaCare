import streamlit as st
import pandas as pd

# Charger les données des fichiers CSV
exercices = pd.read_csv("exercices.csv")
nutritions = pd.read_csv("nutritions.csv")


def display():
    # Titre de la page
    st.title("📅 Horaire Hebdomadaire d'Exercices et de Nutrition")

    # Fusionner les données d'exercices et de nutrition
    horaire = pd.merge(exercices, nutritions, on=[
                       "Jour", "Heure"], how="outer", suffixes=("_exercice", "_nutrition"))

    # Créer un DataFrame pour l'affichage
    jours = ["Lundi", "Mardi", "Mercredi",
             "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    heures = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
              "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]

    # Initialiser un DataFrame vide pour l'horaire
    horaire_df = pd.DataFrame(index=heures, columns=jours)

    # Remplir le DataFrame avec les données
    for _, row in horaire.iterrows():
        jour = row["Jour"]
        heure = row["Heure"]
        exercice = row["Exercice"]
        nutrition = row["Repas"]
        horaire_df.at[heure, jour] = f"{exercice}\n{nutrition}" if pd.notna(
            exercice) and pd.notna(nutrition) else (exercice if pd.notna(exercice) else nutrition)

    # Afficher l'horaire
    st.write("Voici votre horaire hebdomadaire d'exercices et de nutrition :")
    st.dataframe(horaire_df)

    # Appliquer des couleurs pour différencier les exercices et la nutrition
    def color_cells(val):
        if pd.notna(val):
            if "Exercice" in val:
                return "background-color: lightgreen"
            elif "Repas" in val:
                return "background-color: lightblue"
        return ""

    styled_horaire = horaire_df.style.applymap(color_cells)
    st.dataframe(styled_horaire)
