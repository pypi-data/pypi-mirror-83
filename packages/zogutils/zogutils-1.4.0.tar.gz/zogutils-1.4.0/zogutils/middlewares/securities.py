"""
Security middlewares

Help project to enable security function faster and easy to config via settings
environment parameters.

Configs:
    - SECURITY_CSRF: True or False to enable CSRF
    - BACKEND_CORS_ORIGINS: List of CORS origins to enable CORS with them
    - RATE_LIMIT: to provide rate limiter. MUST BE defined followed config
    RATE_LIMIT_TIME_SPAN and RATE_LIMIT_BLOCK_DURATION
"""
import pydantic
from fastapi import FastAPI
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.rate_limiting.middleware import RateLimitingMiddleware, \
    InMemoryLimitProvider
from starlette.middleware.cors import CORSMiddleware


def init_app(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    init_csrf(app, settings)
    init_cors(app, settings)
    init_rate_limiter(app, settings)


def init_csrf(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    if getattr(settings, "SECURITY_CSRF", None):
        app.add_middleware(
            CSRFMiddleware, allowed_hosts=[getattr(settings, "SERVER_HOST")]
        )


def init_cors(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    if getattr(settings, "BACKEND_CORS_ORIGINS", None):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           getattr(settings, "BACKEND_CORS_ORIGINS")],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def init_rate_limiter(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    if getattr(settings, "RATE_LIMIT", None):
        provider = InMemoryLimitProvider(
            limit=getattr(settings, "RATE_LIMIT"),
            timespan=getattr(settings, "RATE_LIMIT_TIME_SPAN"),
            block_duration=getattr(settings, "RATE_LIMIT_BLOCK_DURATION")
        )
        app.add_middleware(
            RateLimitingMiddleware, provider=provider
        )
