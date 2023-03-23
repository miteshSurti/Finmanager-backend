from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.transaction import Transaction, updateTransaction

from auth.auth_bearer import JWTBearer

transactions = connection("transactions")


def transaction_helper(transaction) -> dict:
    return {
        "_id": str(transaction["_id"]),
        "email": transaction["email"],
        "description": transaction["description"],
        "timing": str(transaction["timing"]),
        "amount": transaction["amount"],
        "isComplete": transaction["isComplete"],
    }


async def retrieve_transactions(email: str):
    t = []
    async for transaction in transactions.find({"email": email}):
        t.append(transaction_helper(transaction))
    return t


# Add a new transaction into to the database
async def add_transaction(transaction_data: dict):
    try:
        await transactions.insert_one(transaction_data)
        return True
    except:
        return False


# Update a transaction with a matching ID
async def update_transaction(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    transaction = await transactions.find_one({"_id": ObjectId(id)})
    if transaction:
        updated_transaction = await transactions.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_transaction:
            return True
        return False


async def delete_transaction(id: str):
    delete = await transactions.delete_one({"_id", ObjectId(id)})
    if delete:
        return True
    return False


router = APIRouter()


@router.post("/", response_description="transaction added")
async def addTransaction(transaction: Transaction = Body(...)):
    transaction = jsonable_encoder(transaction)
    newTransaction = await add_transaction(transaction)
    return ResponseModel(newTransaction, "Transaction added successfully!")


@router.get("/{email}")
async def retriveTransactions(email: EmailStr):
    transactions = await retrieve_transactions(email)
    if transactions:
        return ResponseModel(transactions, "Transaction data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Transaction does not exist")


@router.put("/{id}")
async def updatetransaction(id: str, transaction: updateTransaction = Body(...)):
    req = {k: v for k, v in transaction.dict().items() if v is not None}
    updated_Transaction = await update_transaction(id, req)

    if updated_Transaction:
        return ResponseModel(
            "transaction with email: {} name update is successful".format(id),
            "transaction updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Transaction data.",
    )


@router.delete("/{id}")
async def deleteTransaction(id: str):
    transaction = transactions.find_one({"_id": ObjectId(id)})
    if transaction:
        await transactions.delete_one({"_id": ObjectId(id)})
        return True
    return False
