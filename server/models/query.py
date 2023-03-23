from pydantic import BaseModel, EmailStr, Field, FilePath
from typing import List, Optional
import datetime


class Query(BaseModel):
    email: EmailStr = Field(...)
    timing: datetime.datetime = Field(...)
    title: str = Field(..., max_length=50)
    description: str = Field(..., max_length=100)
