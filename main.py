from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.user import users_router
from core.exceptions import CustomException


# Configure web domain which can access api
origins = [
    "*",
]


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(users_router)


def create_app():
    app_ = FastAPI()
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_listeners(app_=app_)
    init_routers(app_=app_)

    return app_


app = create_app()


@app.get("/")
def hello():
    return "Hello world!"
