from app.utils.format import snake_case


class Route:
    @classmethod
    def __url_prefix__(cls):
        return f"/{snake_case(cls.__name__)}"

    @classmethod
    def routes(cls):
        pass
