import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from api.v1 import router
from core.excpetions import RouteException

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app: FastAPI = FastAPI()
app.include_router(router)


@app.exception_handler(ValueError)
async def unicorn_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"message": exc.args},
    )


@app.exception_handler(RouteException)
async def unicorn_exception_handler(request: Request, exc: RouteException):
    return JSONResponse(
        status_code=422,
        content={"message": exc.args},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
