from typing import Optional
from pydantic import BaseModel, EmailStr, Field, FilePath
import datetime


class Transaction(BaseModel):
    email: EmailStr = Field(...)
    description: str = Field(...)
    receipt: FilePath = Field(...)
    timing: datetime.datetime = Field(...)
    amount: int = Field(...)
    isComplete: bool = Field(...)


class updateTransaction(BaseModel):
    description: Optional[str]
    receipt: Optional[FilePath]
    timing: Optional[datetime.datetime]
    amount: Optional[int]
    isComplete: Optional[bool]
