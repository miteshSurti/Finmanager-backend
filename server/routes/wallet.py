from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.wallet import Wallet, updateWallet

from auth.auth_bearer import JWTBearer

wallet = connection("wallet")


def wallet_helper(wallet) -> dict:
    return {
        "email": wallet["email"],
        "balance": wallet["balance"],
        "debt": wallet["debt"],
        "limit": wallet["limit"],
    }


# Add a new wallet into to the database
async def add_wallet(wallet_data: dict) -> dict:
    try:
        await wallet.insert_one(wallet_data)
        return True
    except:
        return False


#
async def retrieve_wallet(email: str):
    a = await wallet.find_one({"email": email})
    if a:
        return wallet_helper(a)
    else:
        return None


# retrive all wallet
async def retrieve_all():
    a = []
    async for i in wallet.find():
        a.append(wallet_helper(i))
    return a


async def update_wallet(email: str, data: dict):
    if len(data) < 1:
        return False
    w = await wallet.find_one({"email": email})
    if w:
        updated_wallet = await wallet.update_one({"email": email}, {"$set": data})
        if updated_wallet:
            return True
        return False


router = APIRouter()


@router.post("/", response_description="wallet added")
async def addquery(w: Wallet = Body(...)):
    w = jsonable_encoder(w)
    newquery = await add_wallet(w)
    if newquery:
        return ResponseModel(True, "wallet added successfully!")
    else:
        return ErrorResponseModel("Cannot add wallet", 403, "wallet cannot be added!")


@router.get("/{email}", dependencies=[Depends(JWTBearer())])
async def getwallet(email: EmailStr):
    a = await retrieve_wallet(email)
    if a:
        return ResponseModel(a, "wallet data retrieved successfully")
    return ErrorResponseModel("Error", 404, "wallet does not exist")


@router.get("/all/")
async def getAll():
    w = await retrieve_all()
    if w:
        return ResponseModel(wallet, "wallet data retrieved successfully")
    return ErrorResponseModel("Error", 404, "wallet does not exist")


@router.put("/{email}", dependencies=[Depends(JWTBearer())])
async def retrivequery(email: EmailStr, data: updateWallet = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    w = await update_wallet(email, data)
    if w:
        return ResponseModel(w, "wallet data updates successfully")
    return ErrorResponseModel("Error", 403, "wallet does not exist")
