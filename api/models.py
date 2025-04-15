from pydantic import BaseModel

class CommandInput(BaseModel):
    text: str