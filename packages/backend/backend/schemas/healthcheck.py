"""
Model for healthcheck endpoint
"""

from pydantic import BaseModel


class HealthcheckResult(BaseModel):
    is_alive: bool
    date: str
