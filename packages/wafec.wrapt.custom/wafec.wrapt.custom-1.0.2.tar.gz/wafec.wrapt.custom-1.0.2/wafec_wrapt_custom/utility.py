

__all__ = [
    'fullname',
    'starts_with'
]


# https://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python
def fullname(o):
    if o is None:
        return None
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    else:
        return module + '.' + o.__class__.__name__


def starts_with(collection, text):
    if text is None or collection is None:
        return False
    for item in collection:
        if text.startswith(item):
            return True
    return False
