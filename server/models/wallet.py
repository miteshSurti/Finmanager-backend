from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class Wallet(BaseModel):
    email: EmailStr = Field(...)
    balance: float = Field(...)
    debt: float = Field(...)
    limit: float = Field(...)


class updateWallet(BaseModel):
    balance: Optional[float]
    debt: Optional[float]
    limit: Optional[float]
