from pydantic import BaseModel


class ProjectIdea(BaseModel):
    title: str
    problem: str
    solution: str
    impact: str