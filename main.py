import streamlit as st
from database import MongoDB
from ai import GeminiAI




#Pour utiliser les fonctions de mongoDB
db = MongoDB()
#Pour utiliser les fonctions de Gemini
gemini = GeminiAI()

# Interface Streamlit
st.title("🤖 YELTA-AI")
st.write("Pose-moi une question !")


# Entrée utilisateur
user_input = st.text_input("💬 Votre question :", "")

# Si on souhaite intégrer la génération de code python via l'API Google
if st.button("Générer du code") and user_input:
    st.write("### 🤖 Code généré :")
    st.code(gemini.generate_text(user_input))


    # Input field
user_input = st.text_input("Enter some data to store in MongoDB:")

if st.button("Save to MongoDB") and user_input:
    db.insert_data({"data": user_input})
    st.success("✅ Data saved successfully!")

# Display data from MongoDB
st.subheader("📜 Stored Data:")

data = db.get_all_data()
for item in data:
    st.write(item["data"])



# Créer un menu déroulant pour les onglets
tab = st.sidebar.selectbox("Choisissez une section", ["Section 1", "Section 2", "Section 3"])

# Afficher le contenu de l'onglet sélectionné
if tab == "Section 1":
    st.write("Contenu de la Section 1")
elif tab == "Section 2":
    st.write("Contenu de la Section 2")
else:
    st.write("Contenu de la Section 3")


import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Exemple de données de points (latitude, longitude)
data = [
    [37.7749, -122.4194],  # San Francisco
    [37.8044, -122.2711],  # Oakland
    [37.8044, -122.4491],  # San Francisco
    [37.6879, -122.4702],  # San Mateo
    [37.7749, -122.4394],  # San Francisco
    [37.8045, -122.4545],  # Oakland
]

# Créer une carte avec un style noir et blanc minimaliste
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12, 
               tiles="CartoDB positron")  # Style noir et blanc minimal

# Ajouter la heatmap
HeatMap(data).add_to(m)

# Afficher la carte dans Streamlit
st_folium(m, width=725)


from streamlit_echarts import st_echarts
liquidfill_option = {
    "series": [{"type": "liquidFill", "data": [0.8, 0.7, 0.6, 0.5]}]
}
st_echarts(liquidfill_option)




import yfinance as yf

# List of ticker symbols for multiple companies
tickers = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"]

# Download historical data for all companies in the list
data = yf.download(tickers, start="2020-01-01", end="2025-01-01")

# Display the data
print(data)
