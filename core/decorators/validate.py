import inspect
from functools import wraps
from typing import Type

from pydantic import BaseModel


def validate_params(model: Type[BaseModel]):
    """
    Decorator that validates both positional and keyword
    arguments using `pydantic.BaseModel`.

    Args:
        model (Type[BaseModel]): The Pydantic model class used for validation.

    Returns:
        Callable: A decorated function with validated parameters.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # Extract the function's signature to map positional args.
            func_signature = inspect.signature(func)
            param_names = list(func_signature.parameters.keys())

            # Map positional arguments to the corresponding parameter names.
            params = {**dict(zip(param_names, args)), **kwargs}

            # Validate the combined parameters using the Pydantic model.
            validated_data = model(**params).model_dump()

            # Call the original function with validated data.
            return func(**validated_data)

        return wrapper
    return decorator
