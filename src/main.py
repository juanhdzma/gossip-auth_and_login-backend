from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

# from fastapi.responses import PlainTextResponse
# import yaml
from src.domain.response.CustomException import (
    InvalidMethodException,
    NotFoundException,
    BadRequestException,
)
from src.domain.response.Response import Response
from src.infrastructure.api.router.AppRouter import app_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow these HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(app_router, prefix="/gossip_api/v1")


# with open("docs/swagger/api.yaml", "r") as file:
#     openapi_yaml_content = yaml.safe_load(file)


# def custom_openapi():
#     return openapi_yaml_content


# app.openapi = custom_openapi


# @app.get("/docs", response_class=PlainTextResponse)
# async def read_openapi():
#     return yaml.dump(openapi_yaml_content)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, err: RequestValidationError):
    return Response.failure(BadRequestException(err.errors()[0]["msg"]))


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return Response.failure(NotFoundException("Ruta no encontrada"))


@app.exception_handler(405)
async def custom_405_handler(_, __):
    return Response.failure(InvalidMethodException("Metodo incorrecto"))
