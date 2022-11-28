import asyncio
from functools import wraps
from importlib import import_module


def import_from_string(spec):
    """
    Thanks to https://github.com/encode/django-rest-framework/blob/master/rest_framework/settings.py#L170
    Example:
        import_from_string('django_filters.rest_framework.DjangoFilterBackend')
        engine = conf['ENGINE']
        engine = import_from_string(engine) if isinstance(engine, six.string_types) else engine
    """  # noqa
    try:
        # Nod to tastypie's use of importlib.
        parts = spec.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError, ValueError) as e:
        msg = f"Could not import '{spec}'. {e.__class__.__name__}: {e}."
        raise ImportError(msg) from e


def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if "There is no current event loop in thread" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        raise


def force_sync(fn):
    '''
    turn an async function to sync function
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        return get_event_loop().run_until_complete(res) if asyncio.iscoroutine(res) else res

    return wrapper
