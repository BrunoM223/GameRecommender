import uuid
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model

@dataclass
class Game(Model):
    collection: str = field(init=False, default="games")
    title: str = field(default=None)
    brand: str = field(default=None)
    asin: str = field(default=None)
    imageURL: str = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return{
            "_id": self._id,
            "title": self.title,
            "brand": self.brand,
            "asin": self.asin,
            "imageURL": self.imageURL
        }

    @classmethod
    def find_by_asin(cls, asin) -> "Game":
        return cls.find_one_by('asin', asin)


