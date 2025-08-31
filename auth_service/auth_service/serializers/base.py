# serializers/base.py (or at the top of serializers.py)
from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """
    A base serializer that provides custom error formatting for all inheriting serializers.
    Formats errors as: {"success": false, "msg": "error message"}
    """

    def format_errors(self):
        default_errors = super().errors

        error_list = []
        for field, messages in default_errors.items():
            if field == "non_field_errors":
                error_list.extend(messages)
            else:
                error_list.append(f"{field}: {'; '.join(messages)}")

        return {
            "success": False,
            "msg": error_list[0] if len(error_list) == 1 else error_list,
        }


class BaseModelSerializer(serializers.ModelSerializer):
    """
    A base ModelSerializer with the same custom error formatting.
    """

    def format_errors(self):
        default_errors = super().errors

        error_list = []
        for field, messages in default_errors.items():
            if field == "non_field_errors":
                error_list.extend(messages)
            else:
                error_list.append(f"{field}: {'; '.join(messages)}")

        return {
            "success": False,
            "msg": error_list[0] if len(error_list) == 1 else error_list,
        }
