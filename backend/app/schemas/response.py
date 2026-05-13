from pydantic import BaseModel
from typing import Literal


class Confidence(BaseModel):
    confidence: Literal["high", "medium", "low"]
