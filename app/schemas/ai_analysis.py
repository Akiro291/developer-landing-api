from pydantic import BaseModel
from typing import Optional

class AIAnalysis(BaseModel):
    category: str
    sentiment: str
    response: str

