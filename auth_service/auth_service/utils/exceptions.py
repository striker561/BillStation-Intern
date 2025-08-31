from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Get the error
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "status": False,
                "msg": "A server error occurred.",
                "errors": None,
                "data": None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    errors = {}
    messages = []

    if isinstance(response.data, dict):
        for field, msgs in response.data.items():
            if not isinstance(msgs, list):
                msgs = [str(msgs)]
            errors[field] = msgs
            for msg in msgs:
                if field == "non_field_errors":
                    messages.append(msg)
                else:
                    messages.append(f"{field}: {msg}")

    elif isinstance(response.data, list):
        messages = [str(msg) for msg in response.data]
        errors["non_field_errors"] = messages

    else:
        messages = [str(response.data)]
        errors["non_field_errors"] = messages

    # Decide summary message
    if len(messages) == 1:
        summary = messages[0]
    else:
        summary = "Multiple validation errors occurred."

    return Response(
        {
            "status": False,
            "msg": summary,
            "errors": errors,
            "data": None,
        },
        status=response.status_code,
    )
