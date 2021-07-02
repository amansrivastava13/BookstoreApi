from pydantic import BaseModel
from models.author import Author
from utils.const import ISBN_DESCRIPTION


class Book(BaseModel):
    isbn: str
    name: str
    author: Author
    year: int
