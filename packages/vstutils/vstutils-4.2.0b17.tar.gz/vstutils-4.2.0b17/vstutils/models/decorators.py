from ..api import decorators as api_decorators


class register_view_decorator:  # pylint: disable=invalid-name
    __slots__ = ('method_type', 'args', 'kwargs')

    def __init__(self, method_type, *args, **kwargs):
        self.method_type = f'type_{method_type}'
        assert hasattr(self, self.method_type), f'Invalid register type {method_type}.'
        self.args = args
        self.kwargs = kwargs

    def type_action(self, func):
        if func.__doc__ and 'description' not in self.kwargs:
            self.kwargs['description'] = func.__doc__
        return api_decorators.subaction(*self.args, **self.kwargs)(func)

    def type_override_method(self, func):
        return func

    def __call__(self, func):
        result = getattr(self, self.method_type)(func)
        result._append_to_view = True
        return result


class register_view_action(register_view_decorator):  # pylint: disable=invalid-name
    """
    Simple decorator for marking model methods as generated view actions.
    The decorated method becomes a method of generated view and `self` will be view object.
    See supported args in :func:`vstutils.api.decorators.subaction`
    """
    __slots__ = ()  # type: ignore

    def __init__(self, *args, **kwargs):
        super().__init__('action', *args, **kwargs)


class register_view_method(register_view_decorator):  # pylint: disable=invalid-name
    __slots__ = ()  # type: ignore

    def __init__(self, *args, **kwargs):
        super().__init__('override_method', *args, **kwargs)
