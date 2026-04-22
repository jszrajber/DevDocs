from pydantic import BaseModel, field_validator
from typing import Literal


class SafetyCheck(BaseModel):
    is_safe: Literal["true", "false"]


class QuestionRequest(BaseModel):
    question: str

    @field_validator("question")
    def sanitize(cls, v):
        forbidden = ["ingore previous", "forget instructions", "system prompt"]
        for phrase in forbidden:
            if phrase in v.lower():
                raise ValueError("Invalid input")

        return v
