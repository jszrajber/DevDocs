from pydantic import BaseModel
from typing import Literal


class Answer(BaseModel):
    answer: str
    confidence: Literal["high", "medium", "low"]
