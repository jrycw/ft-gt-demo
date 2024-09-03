from functools import partial, wraps

from fasthtml.common import Div, NotStr


def gt2fasthtml(func=None, **div_kwargs):
    """
    https://pybit.es/articles/decorator-optional-argument/
    """
    if func is None:
        return partial(gt2fasthtml, **div_kwargs)

    @wraps(func)
    def wrapper(*args, **kwargs):
        gtbl = func(*args, **kwargs)
        gtbl_html = gtbl.as_raw_html()
        return Div(NotStr(gtbl_html), **div_kwargs)

    return wrapper
