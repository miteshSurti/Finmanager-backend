from fastapi import FastAPI, Depends

# from server.routes.student import router as StudentRouter
from server.routes.user import router as UserRouter
from server.routes.transaction import router as transactionRouter
from server.routes.query import router as queryRouter
from server.routes.analysis import router as analysisRouter
from server.routes.wallet import router as walletRouter

# auth handlers
from auth.auth_bearer import JWTBearer

app = FastAPI()

# routes
app.include_router(UserRouter, tags=["users"], prefix="/user")
app.include_router(
    transactionRouter,
    tags=["transactions"],
    prefix="/transaction",
    dependencies=[Depends(JWTBearer())],
)
app.include_router(queryRouter, tags=["query"], prefix="/query")
app.include_router(analysisRouter, tags=["analysis"], prefix="/analysis")
app.include_router(walletRouter, tags=["wallet"], prefix="/wallet")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
