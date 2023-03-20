from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Analysis(BaseModel):
    email: EmailStr = Field(...)
    average: float = Field(default=0)
    max: float = Field(default=0.0)
    min: float = Field(default=0.0)
    creditScore: float = Field(default=100.0)


class updateAnalysis(BaseModel):
    average: Optional[float]
    max: Optional[float]
    min: Optional[float]
    creditScore: Optional[float] = Field(..., le=100.0)
