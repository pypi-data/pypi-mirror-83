from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from googletrans import Translator


def init_app(app: FastAPI):
    app.add_exception_handler(RequestValidationError, handle_validation_error)


def handle_validation_error(request: Request, exc: RequestValidationError):
    error_message = exc.errors()[0].get("msg")
    error = ZOGHTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             msg=error_message)
    return error.to_response()


class ZOGHTTPException(HTTPException):
    """
    Default ZOG Exception

    Auto translate exception message to supported language via Google. Default
    support English. ZOG exception MUST BE init with error message in English.
    """
    status_code: status
    english_msg: str
    detail: dict = {}
    additional_lang = ["vi"]

    def __init__(self, msg: str = None, status_code: status = None,
                 headers: Optional[Dict[str, Any]] = None):
        if msg:
            self.english_msg = msg
        if status_code:
            self.status_code = status_code

        self.add_detail_lang()

        super(ZOGHTTPException, self).__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=headers
        )

    def add_detail_lang(self):
        self.detail["en"] = self.english_msg
        translator = Translator()
        for lang in self.additional_lang:
            self.detail[lang] = translator.translate(
                self.english_msg, src="en", dest=lang).text

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder({
                "detail": self.detail
            })
        )


class InvalidParam(ZOGHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    english_msg = "Invalid parameter"
