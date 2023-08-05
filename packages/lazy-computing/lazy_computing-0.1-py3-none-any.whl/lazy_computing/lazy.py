def extract(index, iterable):
    it = iter(iterable)
    while index > 0:
        next(it)
        index -= 1
    return next(it)

def take(limit, iterable):
    it = iter(iterable)
    while limit > 0:
        yield next(it)
        limit -= 1

def remove(number, iterable):
    it = iter(iterable)
    while number > 0:
        next(it)
        number -= 1
    return it


def head(iterable):
    return next(iter(iterable))

def tail(iterable):
    it = iter(iterable)
    next(it)
    return it

def _arithm(start, end=None, step=1):
    if end is None:
        while True:
            yield start
            start += step
    else:
        if step >= 0:
            while start < end:
                yield start
                start += step
        else:
            while start > end:
                yield start
                start += step

def _geom(start, end=None, coef=2):
    if end is None:
        while True:
            yield start
            start *= coef
    else:
        if coef >= 0:
            while start < end:
                yield start
                start *= coef
        else:
            while start > end:
                yield start
                start *= coef

def _is_ellipsis(value):
    return isinstance(value, type(Ellipsis))

def arithm(*args):
    step = 1
    it = iter(args)
    start = next(it)
    value = start
    next_value = next(it)
    if not _is_ellipsis(next_value):
        step = next_value - value
        value = next_value
        next_value = next(it)
        while not _is_ellipsis(next_value):
            if next_value - value != step:
                raise Exception("Step is not constant")
            value = next_value
            next_value = next(it)
    end = next(it, None)
    return _arithm(start, end, step)

def geom(*args):
    coef = 2
    it = iter(args)
    start = next(it)
    value = start
    next_value = next(it)
    print("At begenning", next_value, value)
    if not _is_ellipsis(next_value):
        coef = next_value / value
        value = next_value
        next_value = next(it)
        while not _is_ellipsis(next_value):
            if next_value / value != coef:
                print("Before raise", next_value, value)
                raise Exception("Factor is not constant")
            value = next_value
            next_value = next(it)
    end = next(it, None)
    return _geom(start, end, coef)
    

class Infinity:
    def __iter__(self):
        i = 0
        while True:
            yield i
            i += 1
    def __str__(self):
        return "Infinity"
    def __repr__(self):
        return str(self)

infinity = Infinity()