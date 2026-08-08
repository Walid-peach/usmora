from pydantic import BaseModel, Field, field_validator


class ReflectionRequest(BaseModel):
    situation: str = Field(min_length=1, max_length=4000)

    @field_validator("situation")
    @classmethod
    def situation_must_have_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Situation cannot be empty.")
        return cleaned


class ReflectionResponse(BaseModel):
    facts: list[str]
    assumptions: list[str]
    feelings: list[str]
    needs: list[str]
    draft: str
    disclaimer: str
