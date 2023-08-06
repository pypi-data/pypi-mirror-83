import pydantic
from fastapi import FastAPI

from . import securities, monitoring, logger, exceptions


def init_app(app: FastAPI, settings: pydantic.BaseSettings):
    logger.init_app()
    monitoring.init_app(app, settings)
    securities.init_app(app, settings)
    exceptions.init_app(app)
