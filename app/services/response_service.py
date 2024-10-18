from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse

from schemas.response_scheme import SuccessResponse, ErrorResponse, Message
from exceptions import exceptions_list


class ResponseService:
    @staticmethod
    async def response(response: Any) -> Any:
        try:
            response_result = await response

            return SuccessResponse(
                detail=response_result
            )

        except exceptions_list as error_detail:

            error_response = ErrorResponse(
                detail=Message(
                    message=str(error_detail)
                )
            )

            return JSONResponse(
                content=error_response.model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST
            )
