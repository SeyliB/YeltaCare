import streamlit as st
import pandas as pd

# Titre de l'application
st.title("🍎 Nutrition Intelligente")

# Section 1 : Introduction
st.write("""
Bienvenue dans votre application de nutrition intelligente !
Entrez vos informations pour obtenir des recommandations personnalisées.
""")

# Section 2 : Collecte des informations utilisateur
st.header("📋 Vos Informations")
age = st.slider("Âge", 1, 100, 25)
weight = st.number_input("Poids (kg)", 30, 200, 70)
height = st.number_input("Taille (cm)", 100, 250, 175)
activity_level = st.selectbox("Niveau d'activité", ["Sédentaire", "Léger", "Modéré", "Actif", "Très actif"])
goal = st.radio("Objectif", ["Perte de poids", "Maintien", "Prise de masse"])

# Section 3 : Calcul des besoins nutritionnels
if st.button("Calculer mes besoins"):
    # Exemple de calcul simple (à adapter avec des formules précises)
    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # Équation de Harris-Benedict
    activity_multiplier = {
        "Sédentaire": 1.2,
        "Léger": 1.375,
        "Modéré": 1.55,
        "Actif": 1.725,
        "Très actif": 1.9
    }
    tdee = bmr * activity_multiplier[activity_level]

    st.subheader("⚡ Vos besoins nutritionnels")
    st.write(f"Calories quotidiennes recommandées : **{tdee:.0f} kcal**")

# Section 4 : Recommandations de repas
st.header("🍽️ Recommandations de repas")
meal_data = pd.read_csv("data/meals.csv")  # Exemple de données de repas
st.write("Voici quelques idées de repas adaptées à vos besoins :")
st.dataframe(meal_data)

# Section 5 : Suivi des repas
st.header("📅 Suivi des repas")
meal = st.text_input("Qu'avez-vous mangé aujourd'hui ?")
if st.button("Ajouter"):
    st.write(f"Vous avez mangé : {meal}")

# Section 6 : Visualisation des données
st.header("📊 Visualisation des données")
st.write("Graphique des calories consommées au fil du temps")
# Exemple de graphique (à adapter avec vos données)
chart_data = pd.DataFrame({"Jour": [1, 2, 3, 4, 5], "Calories": [2000, 2200, 1800, 2500, 2100]})
st.line_chart(chart_data.set_index("Jour"))

# Section 7 : Ressources supplémentaires
st.header("📚 Ressources")
st.write("Consultez ces ressources pour en savoir plus sur la nutrition :")
st.markdown("- [Guide nutritionnel de l'OMS](https://www.who.int/fr)")
st.markdown("- [Calculatrice de calories](https://www.calculator.net/calorie-calculator.html)")