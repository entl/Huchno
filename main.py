from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from api.auth import auth_router
from api.user import users_router
from core.exceptions import CustomException
from core.fastapi.middlewares.auth_middleware import AuthenticationMiddleware, AuthBackend

# Configure web domain which can access api
origins = [
    "*",
]


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
    ]
    return middleware


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(users_router)
    app_.include_router(auth_router)


def create_app():
    app_ = FastAPI(middleware=make_middleware())
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
