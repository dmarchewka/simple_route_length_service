import uvicorn
from fastapi import FastAPI


from api.v1 import router

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
