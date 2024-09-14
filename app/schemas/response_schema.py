from fastapi.responses import JSONResponse


def return_response(success: bool = True, data: str = "", status_code: int = 200) -> JSONResponse:
    """builds default response dict."""

    return JSONResponse(
        content={
            "success": success,
            "data": data
        },
        status_code=status_code
    )
