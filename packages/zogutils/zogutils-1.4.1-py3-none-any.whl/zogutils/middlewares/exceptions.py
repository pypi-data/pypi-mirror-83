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
    translator = Translator()
    vi_msg = translator.translate(error_message, src="en", dest="vi").text
    error = ZOGHTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             en_msg=error_message,
                             vi_msg=vi_msg)
    return error.to_response()


class ZOGHTTPException(HTTPException):
    """
    Default ZOG Exception

    Auto translate exception message to supported language via Google. Default
    support English. ZOG exception MUST BE init with error message in English.
    """
    status_code: status
    en_msg: str
    vi_msg: str
    detail: dict = {}

    def __init__(self, en_msg: str = None, vi_msg: str = None,
                 status_code: status = None,
                 headers: Optional[Dict[str, Any]] = None):
        if en_msg:
            self.en_msg = en_msg
        if status_code:
            self.status_code = status_code
        if vi_msg:
            self.vi_msg = vi_msg

        self.add_detail_lang()

        super(ZOGHTTPException, self).__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=headers
        )

    def add_detail_lang(self):
        self.detail["en"] = self.en_msg
        self.detail["vi"] = self.vi_msg

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder({
                "detail": self.detail
            })
        )


class InvalidParam(ZOGHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    en_msg = "Invalid parameter"
