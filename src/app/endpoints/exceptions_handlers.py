from fastapi import Request
from fastapi.responses import JSONResponse

from app.main import app
from src.app.core.exceptions import CustomExceptionBase, NotFoundException


@app.exception_handler(CustomExceptionBase)
async def custom_exception_handler(request: Request, exc: CustomExceptionBase):
    status_code = 400 if type(exc) is not NotFoundException else 404
    return JSONResponse(
        status_code=status_code,
        content={
            "message": f"Возникла ошибка {type(exc).__name__}: {exc.detail}"
        }
    )
