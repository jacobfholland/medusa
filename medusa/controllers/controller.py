

from medusa.utils.merge import merge, merge_values


class Controller:
    """Base controller class to either be inherited by `Model` or used on it's own."""

    # @classmethod
    # @merge_values
    # def create(cls, *args, **kwargs):
    #     # vals = merge(*args, *kwargs)
    #     return kwargs

    @classmethod
    @merge_values
    def get(cls, *args, **kwargs):
        # vals = merge(*args, *kwargs)
        return kwargs

    pass
