from typing import Dict
import pymongo


class Database:
    URI = "mongodb+srv://administrator:administrator@tbp.jcdgz.mongodb.net/test?retryWrites=true&w=majority"

    client = pymongo.MongoClient(URI)
    DATABASE = client['TBP']

    @staticmethod
    def insert(collection: str, data: Dict) -> None:
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].replace_one(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def get_random(collection: str, k: int) -> Dict:
        return Database.DATABASE[collection].aggregate([{'$sample': {'size': k}}])

    @staticmethod
    def find_text(collection: str, text: str) -> Dict:
        return Database.DATABASE[collection].find({'$text': {"$search": text}}).limit(10)


