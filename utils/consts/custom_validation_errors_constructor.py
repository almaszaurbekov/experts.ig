from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.exceptions import APIException, ErrorDetail


def _custom_get_error_details(data, default_code=None):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    if isinstance(data, (list, tuple)):
        ret = [_custom_get_error_details(item, default_code) for item in data]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: _custom_get_error_details(value, default_code)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    if type(data) == int:
        text = data
    else:
        text = force_str(data)
    code = getattr(data, "code", default_code)
    return CustomErrorDetail(
        text, code
    )


# CustomErrorDetail кастомный класс для валидации типа значений
class CustomErrorDetail(ErrorDetail):
    code = None

    # Перезаписанный класс для вывода статуса в int типе
    def __new__(cls, value, code=None, **kwargs):
        if type(value) == int:
            self = value
        else:
            self = super().__new__(cls, value)
        return self


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "invalid"

    # Перезаписанный класс для вывода статуса ввиде словаря
    # и сами значени не списком, как это делает обычный drf.ValidationError
    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _custom_get_error_details(detail, code)
