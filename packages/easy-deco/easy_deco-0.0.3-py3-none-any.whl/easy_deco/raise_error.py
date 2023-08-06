from .core import decorator

@decorator
def raise_error(func, args , kwargs):
    """
    ...Documentation here...
    """
    try:
        return func(*args, **kwargs)

    except Exception as e:

        raise eval(e.__class__.__name__)(e)