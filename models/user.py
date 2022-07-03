from dataclasses import dataclass, field
from typing import Dict
from models.model import Model
from common.utilities import Utilities
import models.errors as UserError
import uuid


@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    reviewerID: str = field(default=None)
    username: str = field(default=None)
    password: str = field(default=None)
    reviewerName: str = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_reviewerID(cls, reviewerID: str) -> "User":
        try:
            return cls.find_one_by('reviewerID', reviewerID)
        except TypeError:
            raise UserError.UserNotFound("No user with this ID.")

    @classmethod
    def find_by_username(cls, username: str) -> "User":
        try:
            return cls.find_one_by('username', username)
        except TypeError:
            raise UserError.UserNotFound("No user with this username.")

    @classmethod
    def login_valid(cls, username:str, password:str) -> bool:
        user = cls.find_by_username(username=username)
        if not Utilities.hashed_password_check(password, user.password):
            raise UserError.IncorrectPassword("Your password is incorrect.")
        return True

    @classmethod
    def register_user(cls, username: str, password: str) -> bool:
        if not Utilities.username_is_valid(username):
            raise UserError.InvalidUsername("Username isn't in the correct format.")
        try:
            user = cls.find_by_username(username)
            raise UserError.UserAlreadyRegistered("User already registered.")
        except:
            user1 = User(username=username, password=Utilities.hash_password(password), reviewerID=uuid.uuid4().hex)
            user1.save_to_mongo()
        return True

    def json(self) -> Dict:
        return{
            "_id": self._id,
            "username": self.username,
            "password": self.password,
            "reviewerID": self.reviewerID,
            "reviewerName": self.reviewerName,
        }

    @property
    def id(self):
        return self._id



