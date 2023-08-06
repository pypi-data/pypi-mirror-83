from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from translation import google


def init_app(app: FastAPI):
    app.add_exception_handler(RequestValidationError, handle_validation_error)


def handle_validation_error(request: Request, exc: RequestValidationError):
    error_message = exc.errors()[0].get("msg")
    error = InvalidParam(msg=error_message)
    return error.to_response()


class ZOGException(HTTPException):
    """
    Default ZOG Exception

    Auto translate exception message to supported language via Google. Default
    support English. ZOG exception MUST BE init with error message in English.
    """
    status_code: status
    detail: dict = []
    supported_lang = ["vi"]

    def __init__(self, msg: str = None,
                 headers: Optional[Dict[str, Any]] = None):
        self.detail["en"] = msg
        self.add_detail_lang(msg)
        super(ZOGException, self).__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=headers
        )

    def add_detail_lang(self, msg: str):
        for lang in self.supported_lang:
            self.detail[lang] = google(msg, dst=lang)

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder({
                "detail": self.detail
            })
        )


class InvalidParam(ZOGException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {
        "en": "Invalid param",
        "vi": "Thiếu thông tin"
    }
