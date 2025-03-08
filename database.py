import pymongo
import os
from dotenv import load_dotenv

#Ce fichier sert a manipuler la database (Ajouter des fonctions si necessaire)

load_dotenv()
#Obtention des variables sensibles
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

class MongoDB:
    def __init__(self):
        """Initialise la connexion à MongoDB"""
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def insert_data(self, data):
        """Insère un document dans la collection"""
        result = self.collection.insert_one(data)
        return result.inserted_id

    def get_all_data(self):
        """Récupère tous les documents de la collection"""
        return list(self.collection.find())

    def get_data_by_query(self, query):
        """Récupère des documents selon un filtre"""
        return list(self.collection.find(query))

    def update_data(self, query, new_values):
        """Met à jour un document"""
        result = self.collection.update_one(query, {"$set": new_values})
        return result.modified_count

    def delete_data(self, query):
        """Supprime un document"""
        result = self.collection.delete_one(query)
        return result.deleted_count

    def close_connection(self):
        """Ferme la connexion à MongoDB"""
        self.client.close()
