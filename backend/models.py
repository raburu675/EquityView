from sqlmodel import SQLModel, Field
from typing import Optional

# define your output contract
#this serves as our databaseTable and the AIs output schema
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    priority: int #AI Will validate this an an integer
    category: str
    summary: str

