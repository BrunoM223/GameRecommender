from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid
import statistics
from models.user import User
from models.games import Game
from models.model import Model


@dataclass
class Rating(Model):
    collection: str = field(init=False, default="ratings")
    reviewerID: str
    asin: str
    reviewText: str
    summary: str
    overall: int
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.game = Game.find_by_asin(self.asin)
        self.user = User.find_by_reviewerID(self.reviewerID)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "reviewerID": self.reviewerID,
            "asin": self.asin,
            "reviewText": self.reviewText,
            "summary": self.summary,
            "overall": self.overall
        }

    @classmethod
    def avg_ratings_for_game(cls, asin) -> float:
        all = cls.find_many_by('asin', asin)
        if len(all) > 0:
            overall_only = []
            for rating in all:
                if rating.overall != '':
                    overall_only.append(float(rating.overall))
            avg = statistics.geometric_mean(overall_only)
            return avg
        else:
            return 0


    @classmethod
    def ratings_for_user(cls, reviewerID, asin) -> Optional[Any]:
        ratings = cls.find_many_by('reviewerID', reviewerID)
        if len(ratings) > 0:
            for rating in ratings:
                if rating.asin == asin:
                    return rating
                else:
                    continue
        else:
            return 0

    @classmethod
    def all_ratings_for_user(cls, reviewerID):
        ratings = Rating.find_many_by('reviewerID', reviewerID)
        return ratings

