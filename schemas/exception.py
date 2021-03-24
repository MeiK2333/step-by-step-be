from fastapi import HTTPException, responses, Request

from starlette.responses import JSONResponse


class SBSException(Exception):
    def __init__(self, errmsg: str, errcode: int = 200):
        self.errmsg = errmsg
        self.errcode = errcode


async def exception_handler(request: Request, exc: SBSException):
    return JSONResponse(status_code=exc.errcode, content={"errmsg": exc.errmsg})
