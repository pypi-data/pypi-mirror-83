from configurations import Configuration, values


def getlines(path):
    if not path:
        return []
    return list(filter(None, open(path).read().splitlines()))


class MiddlewareMixin:
    MIDDLEWARE_FILE = values.Value(None)
    MIDDLEWARE_FILES = values.ListValue([])

    @classmethod
    def setup(cls):
        super(MiddlewareMixin, cls).setup()
        f_list = cls.MIDDLEWARE_FILES or [cls.MIDDLEWARE_FILE]
        for f in filter(None, f_list):
            for l in getlines(f):
                if l.strip() and l.strip() not in cls.MIDDLEWARE:
                    cls.MIDDLEWARE.append(l.strip())


class MiddlewareConfiguration(MiddlewareMixin, Configuration):
    pass
