"""
    Tools for parsing of various data, such as values, arguments, etc...
"""
from typing import Any, Union


def parse_kwargs(
    kwargs: dict[str, Any],
    expected: dict[str, Any],
    types: dict[str, Union[type, tuple]] = None,
    required: list[str] = None,
) -> dict[str, Any]:
    """
    Given a set of arbitrary keyword arguments in the form of a dict
    (passed as argument `kwargs`), confirms that these are members of dict
    `expected`.

    If `kwargs` contains a key that is not included in `expected`, an
    exception will be raised.

    If list `required` is not None, then its elements must be present as
    keys in `kwargs`, or an exception is raised.

    If `types` is not None, then the type of each value in kwargs must
    correspond to the type to which it is associated in `types`

                ---------------------------------------

    Successful Example 1:

        arguments:
            kwargs = {'arg1':5, 'arg3':8}
            expected = {'arg1':7, 'arg2':0, 'arg3':1, 'arg4':1}
            required = ['arg1']
            types = {'arg1':int}

        returns:
            processed_kwargs = {'arg1':5, 'arg2':0, 'arg3':8, 'arg4':1}

                ---------------------------------------

    Successful Example 2:

        arguments:
            kwargs = {'arg1':5.2, 'arg3':8}
            expected = {'arg1':7, 'arg2':0, 'arg3':1, 'arg4':1}
            required = ['arg1']
            types = {'arg1':(int,float)}

        returns:
            processed_kwargs = {'arg1':5.2, 'arg2':0, 'arg3':8, 'arg4':1}

                ---------------------------------------

    Unsuccessful Example 1:

        arguments:
            kwargs = {'arg2':5, 'arg3':8}
            expected = {'arg1':7, 'arg2':0, 'arg3':1, 'arg4':1}
            required = ['arg1']

        Raises KeyError

                ---------------------------------------

    Unsuccessful Example 2:

        arguments:
            kwargs = {'arg1':5, 'arg3':8}
            expected = {'arg1':7, 'arg2':0, 'arg3':1, 'arg4':1}
            types = {'arg1':str}

        Raises TypeError
    """
    # If there are missing required keys, raises an Exception
    if required is not None:
        for key in required:
            if key not in kwargs.keys():
                msg = f"Missing expected keyword argument `{key}`."
                raise KeyError(msg)

    # If there are required types that are not fulfilled, raises an Exception
    if types is not None:
        for key, value in types.items():
            if not isinstance(value, (list, tuple)):
                value = (value,)
            if key in kwargs.keys() and type(kwargs[key]) not in value:
                msg = (
                    f"Incorrect type `{type(kwargs[key])}` given for argument "
                    f"`{key}` – expected types are: `{value}`."
                )
                raise TypeError(msg)

    # Preparing default values in the new set of kwargs
    processed_kwargs = {i: j for i, j in expected.items()}
    # Iterating through each key-value pair in `kwargs`
    for key, value in kwargs.items():
        # If the key is not in `expected`, raises an Exception
        if key not in expected.keys():
            msg = f"`{key}` is an unknown keyword argument."
            raise KeyError(msg)
        processed_kwargs[key] = value

    return processed_kwargs
