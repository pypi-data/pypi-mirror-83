from typing import Tuple, Type, TypeVar

T = TypeVar('T')


def get_keys(obj: Type[T]) -> Tuple[str]:
    """Helper function to get keys off a dataclass for KeyStore input. Allows
    you to pass the dataclass to this function instead of writing out the keys
    manually which requires updating when the dataclass changes."""

    if type(obj) == dict:
        return tuple(obj.keys())

    try:
        keys = tuple(obj.__annotations__.keys())
    except AttributeError as e:
        raise AttributeError(
            f"Cannot get attributes from class, this method only works with dataclasses: {e}"
        )
    return keys
