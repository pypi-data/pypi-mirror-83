from easy_deco.core import decorator

@decorator
def raise_error(func, args , kwargs):
    """
    This decorator help you to wrap any function to catch any error raised in the function body

    ## Snippet code

    ```python
    >>> from easy_deco import raise_error
    >>> @raise_error
    >>> def func():
            "Function body"

    ```
    """
    try:
        return func(*args, **kwargs)

    except Exception as e:

        raise eval(e.__class__.__name__)(e)