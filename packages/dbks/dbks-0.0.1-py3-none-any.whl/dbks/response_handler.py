from functools import partial
from requests import Response


class ResponseHandler(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, instance, *args, **kwargs):
        print(f'"{instance.__class__.__name__}.{self.func.__name__}" triggered with')
        if args:
            print("args:", args)
        if kwargs:
            print("kwargs:", kwargs)
        if not args and not kwargs:
            print("no args or kwargs")
        res = self.func(instance, *args, **kwargs)
        if isinstance(res, Response):
            print("Response:")
            print("status_code:", str(res.status_code))
            # print('text:', res.text)
            print("json:", res.json())
            if str(res.status_code)[0] != "2":
                raise SystemError("Non 2XX status code returned!")
        return res

    def __get__(self, instance, owner):
        return partial(self, instance)
