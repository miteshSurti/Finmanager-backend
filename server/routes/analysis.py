from fastapi import APIRouter, Body, Depends
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from server.database import connection
from server.models._utils import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.analysis import Analysis, updateAnalysis
from auth.auth_bearer import JWTBearer


analysis = connection("analysis")


def analysis_helper(analysis) -> dict:
    return {
        "email": analysis["email"],
        "average": str(analysis["average"]),
        "max": analysis["max"],
        "min": analysis["min"],
        "creditScore": analysis["creditScore"],
    }


# Add a new analysis into to the database
async def add_analysis(analysis_data: dict) -> dict:
    try:
        await analysis.insert_one(analysis_data)
        return True
    except:
        return False


#
async def retrieve_analysis(email: str):
    a = await analysis.find_one({"email": email})
    if a:
        return analysis_helper(a)
    else:
        return None


# retrive all analysis
async def retrieve_all():
    a = []
    async for i in analysis.find():
        a.append(analysis_helper(i))
    return a


async def update_analysis(email: str, data: dict):
    if len(data) < 1:
        return False
    user = await analysis.find_one({"email": email})
    if user:
        updated_user = await analysis.update_one({"email": email}, {"$set": data})
        if updated_user:
            return True
        return False


router = APIRouter()


@router.post(
    "/", response_description="analysis added", dependencies=[Depends(JWTBearer())]
)
async def addquery(analysis: Analysis = Body(...)):
    analysis = jsonable_encoder(analysis)
    newquery = await add_analysis(analysis)
    if newquery:
        return ResponseModel(True, "Analysis added successfully!")
    else:
        return ErrorResponseModel(
            "Cannot add analysis", 403, "Analysis cannot be added!"
        )


@router.get("/{email}", dependencies=[Depends(JWTBearer())])
async def getAnalysis(email: EmailStr):
    a = await retrieve_analysis(email)
    if a:
        return ResponseModel(a, "Analysis data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Analysis does not exist")


@router.get("/all/")
async def getAll():
    analysis = await retrieve_all()
    if analysis:
        return ResponseModel(analysis, "Analysis data retrieved successfully")
    return ErrorResponseModel("Error", 404, "Analysis does not exist")


@router.put("/{email}", dependencies=[Depends(JWTBearer())])
async def retrivequery(email: EmailStr, data: updateAnalysis = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    analysis = await update_analysis(email, data)
    if analysis:
        return ResponseModel(analysis, "Analysis data updates successfully")
    return ErrorResponseModel("Error", 403, "Analysis does not exist")
