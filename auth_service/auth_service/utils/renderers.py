from rest_framework import renderers, status


class CustomAPIRenderer(renderers.JSONRenderer):
    """Return a universal acceptable response for all API returned"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]

        # Let our custom exception handler deal with errors
        if response.status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        # Check if data is already in our custom format
        if isinstance(data, dict) and "status" in data:
            return super().render(data, accepted_media_type, renderer_context)

        view = renderer_context.get("view")
        message = getattr(view, "message", None)

        if not message:
            if response.status_code == status.HTTP_201_CREATED:
                message = "Resource created successfully"
            else:
                message = "Operation completed successfully"

        formatted_response = {
            "status": True,
            "msg": message,
            "errors": None,
            "data": data,
        }

        # Update response so middleware / tests see formatted version
        response.data = formatted_response

        return super().render(formatted_response, accepted_media_type, renderer_context)
