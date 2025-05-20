def strict(func):
    sig  = func.__annotations__.values()

    def wrapper(*args):
        for value in list(zip(args, tuple(sig))):
            if not isinstance(*value):
                raise TypeError
        return func(*args)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
