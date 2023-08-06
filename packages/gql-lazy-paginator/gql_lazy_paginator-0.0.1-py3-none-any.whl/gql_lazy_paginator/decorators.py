from gql_lazy_paginator.core import (
    PaginationHelper,
    PageableInterface
)


__all__ = [
    "IsPageable",
    "PaginateMe",
    "paginate_me",
    "is_pageable",
]


class IsPageable(PaginationHelper):
    """Lazy pager decorator"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        _fn = self.func
        response = _fn(*args, **kwargs)
        return self.filter(response, **kwargs)


class PaginateMe:
    """Lazy results wrapper into PageableInterface"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        func = self.func
        data = func(*args, **kwargs)
        context = args[0] if len(args) else None
        return PageableInterface(
            data,
            context,
            **kwargs
        )


paginate_me = PaginateMe
is_pageable = IsPageable
