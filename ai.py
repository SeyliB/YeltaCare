from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
#Obtention des variables sensibles
GEMINI_API_KEY = os.getenv('API_KEY')

# Configuration de Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

class GeminiAI:
    def __init__(self, model_name="gemini-2.0-pro-exp-02-05"):
        """Initialise le modèle Gemini avec le modèle choisi"""
        self.model_name = model_name

    def generate_text(self, prompt):
        """Génère du texte à partir d'un prompt"""
        response = client.models.generate_content(
            model=self.model_name, contents=prompt
        )
        return response.text 

    def chat_session(self):
        """Crée une session de chat avec mémoire de contexte"""
        return client.models.start_chat(model=self.model_name)