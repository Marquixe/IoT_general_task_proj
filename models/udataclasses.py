
class DataclassMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls)
        for name, val in getattr(cls, '__annotations__', {}).items():
            default = getattr(cls, name, None)
            setattr(obj, name, kwargs.get(name, default))
            
        # call post-init if exists
        post = getattr(obj, '__post_init__', None)
        if callable(post):
            post()

        return obj


class Dataclass(metaclass=DataclassMeta):
    pass



def validator(field_name):
    def deco(func):
        func._validator_for = field_name
        return func
    return deco
