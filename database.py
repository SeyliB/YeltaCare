import pymongo
import os
from dotenv import load_dotenv

# Ce fichier sert a manipuler la database (Ajouter des fonctions si necessaire)

load_dotenv()
# Obtention des variables sensibles
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

collections = {}


class MongoDB:
    def __init__(self, collection_name="Users"):
        """Initialise la connexion à MongoDB et définit la collection par défaut"""
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[collection_name] if collection_name else None

    def insert_data(self, data):
        """Insère un document dans la collection avec gestion des erreurs"""
        if self.collection is None:
            raise ValueError(
                "❌ Aucune collection définie. Utilisez set_collection().")
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except pymongo.errors.PyMongoError as e:
            print(f"❌ Erreur d'insertion MongoDB : {e}")
            return None

    def get_all_data(self):
        """Récupère tous les documents de la collection"""
        return list(self.collection.find())

    def set_collection(self, collection_name):
        """Change la collection utilisée"""
        self.collection = self.db[collection_name]

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

    def get_document(self, query):
        """Récupère un document complet selon un filtre"""
        return self.collection.find_one(query)


def getCollection(tag):
    list = collections.get(tag)
    if list == None:
        return MongoDB(tag)
    else:
        return list
