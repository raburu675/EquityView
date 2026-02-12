from pydantic import BaseModel
from typing import List, Dict

class Query(BaseModel):
    prompt: str
    data: List[Dict]  # This will hold the rows from df.to_dict(orient="records")