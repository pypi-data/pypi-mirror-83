from pydantic import BaseModel
from typing import List

from pydantic import main


class Rule(BaseModel):
    name: str
    description: str


class Alert(BaseModel):
    accountId: str
    region: str
    resources: List[str]
    rule: Rule
