"""Handles errors recieved from the Jiachang API."""
import json
import xmltodict


class JcException(Exception):
    """Base error for jcapi."""

    def __init__(self, message):
        self.message = message


class NotFound(JcException):
    """Raised when a 404 response is recieved from the Jiachang API.
    Occurs when the requested controller, etc. could not be found."""


class Unauthorized(JcException):
    """Raised when unauthorized, but no other recognized details are provided.
    Occurs when token is invalid."""


class BadCredentials(Unauthorized):
    """Raised when provided credentials are incorrect."""


class BadToken(Unauthorized):
    """Raised when director bearer token is invalid."""


ERROR_CODES = {"401": Unauthorized, "404": NotFound}

ERROR_DETAILS = {
    "Permission denied Bad credentials": BadCredentials,
}

DIRECTOR_ERRORS = {
    "Unauthorized": Unauthorized,
}

DIRECTOR_ERROR_DETAILS = {"Expired or invalid token": BadToken}


async def __checkResponseFormat(response_text: str):
    """Known Jiachang authentication API error message formats:
    ```json
    {
        "JcErrorResponse": {
            "code": 401,
            "details": "Permission denied Bad credentials",
            "message": "Permission denied",
            "subCode": 0
        }
    }
    ```
    ```json
    {
        "code": 404,
        "details": "Account with id:000000 not found in DB",
        "message": "Account not found",
        "subCode": 0
    }```
    ```xml
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <JcErrorResponse>
        <code>401</code>
        <details></details>
        <message>Permission denied</message>
        <subCode>0</subCode>
    </JcErrorResponse>
    ```
    Known Jiachang director error message formats:
    ```json
    {
        "error": "Unauthorized",
        "details": "Expired or invalid token"
    }
    ```
    """
    if response_text.startswith("<"):
        return "XML"
    return "JSON"


async def checkResponseForError(response_text: str):
    """Checks a string response from the Jiachang API for error codes.

    Parameters:
        `response_text` - JSON or XML response from Jiachang, as a string.
    """
    if await __checkResponseFormat(response_text) == "JSON":
        dictionary = json.loads(response_text)
    elif await __checkResponseFormat(response_text) == "XML":
        dictionary = xmltodict.parse(response_text)
    if "JcErrorResponse" in dictionary:
        if dictionary["JcErrorResponse"]["details"] in ERROR_DETAILS:
            exception = ERROR_DETAILS.get(dictionary["JcErrorResponse"]["details"])
            raise exception(response_text)
        else:
            exception = ERROR_CODES.get(
                str(dictionary["JcErrorResponse"]["code"]), JcException
            )
            raise exception(response_text)
    elif "code" in dictionary:
        if dictionary["details"] in ERROR_DETAILS:
            exception = ERROR_DETAILS.get(dictionary["details"])
            raise exception(response_text)
        else:
            exception = ERROR_CODES.get(str(dictionary["code"]), JcException)
            raise exception(response_text)
    elif "error" in dictionary:
        if dictionary["details"] in DIRECTOR_ERROR_DETAILS:
            exception = DIRECTOR_ERROR_DETAILS.get(dictionary["details"])
            raise exception(response_text)
        else:
            exception = DIRECTOR_ERRORS.get(str(dictionary["error"]), JcException)
            raise exception(response_text)
