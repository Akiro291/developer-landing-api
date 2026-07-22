import logging
import uuid
import traceback
from typing import Optional, Dict, Any

from fastapi import HTTPException, Request, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)

def get_error_id() -> str:
    return str(uuid.uuid4())[:8]

def format_error_response(
    error_type: str, 
    message: str, 
    status_code: int, 
    error_id: Optional[str] = None, 
    details: Optional[Dict[Any, Any]] = None
) -> Dict[str, Any]:
    if error_id is None:
        error_id = get_error_id()
    
    response = {
        "error": error_type,
        "message": message,
        "status_code": status_code,
        "error_id": error_id
    }
    
    if details:
        response["details"] = details
    
    return response

def log_exception(exc: Exception, error_id: Optional[str] = None) -> str:
    if error_id is None:
        error_id = get_error_id()
    
    logger.error(f"Exception (ID: {error_id}): {exc}\n{traceback.format_exc()}")
    return error_id

def handle_http_exception(request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            error_type="http_exception",
            message=exc.detail,
            status_code=exc.status_code
        )
    )

def handle_validation_exception(request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    logger.error(f"Validation error: {jsonable_encoder(errors)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error_response(
            error_type="validation_error",
            message="Invalid request data",
            status_code=422,
            details=jsonable_encoder(errors)
        )
    )

def handle_global_exception(request, exc: Exception) -> JSONResponse:
    error_id = get_error_id()
    logger.error(f"Global exception (ID: {error_id}): {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            error_type="internal_error",
            message="Internal server error",
            status_code=500,
            error_id=error_id
        )
    )
