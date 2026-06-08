from typing import Any, Callable

from src.app.core.config import settings


def async_picker(func:Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        if settings.LAUNCHED_IN_CONTAINER:
            return func.delay(*args, **kwargs)  # pyright: ignore[reportFunctionMemberAccess]
        return func(*args, **kwargs)
    return wrapper  # pyright: ignore[reportUnknownVariableType]
