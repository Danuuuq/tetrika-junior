def strict(func):

    def wrapper(*args):
        sig  = tuple(func.__annotations__.values())[:-1]
        for arg, type in list(zip(args, sig)):
            if not isinstance(arg, type):
                raise TypeError(f'Аргумент "{arg}" не соответствует типу: {type}')
        return func(*args)
    return wrapper


@strict
def two_int(a: int, b: int) -> int:
    return a + b

@strict
def two_bool(a: bool, b: bool) -> int:
    return a + b

@strict
def two_float(a: float, b: float) -> float:
    return a + b

@strict
def two_str(a: str, b: str) -> str:
    return a + b

@strict
def int_float(a: int, b: float) -> float:
    return a + b


def test_two_int() -> None:
    for a, b, result in [(1, 2, 3), (0, 0, 0), (-5, 10, 5)]:
        assert two_int(a, b) == result

    for a, b in [("1", 2), (1, 2.4), ([], 1), (None, None)]:
        try:
            two_int(a, b)
            assert False, f"Ожидалась ошибка для вызова: sum_two({a}, {b})"
        except TypeError:
            pass

def test_two_bool() -> None:
    for a, b, result in [(True, True, 2), (False, False, 0), (True, False, 1)]:
        assert two_bool(a, b) == result

    for a, b in [("1", 2), (1, 2), ([], 1), (None, None)]:
        try:
            two_bool(a, b)
            assert False, f"Ожидалась ошибка для вызова: two_bool({a}, {b})"
        except TypeError:
            pass

def test_two_float() -> None:
    for a, b, result in [(1.0, 2.0, 3.0), (0.0, 0.0, 0.0), (-5.5, 10.5, 5.0)]:
        assert two_float(a, b) == result

    for a, b in [("1", 2), (1, 2), ([], 1), (None, None)]:
        try:
            two_float(a, b)
            assert False, f"Ожидалась ошибка для вызова: two_float({a}, {b})"
        except TypeError:
            pass

def test_two_str() -> None:
    for a, b, result in [("Hello", "World", "HelloWorld"), ("", "", ""), ("123", "456", "123456")]:
        assert two_str(a, b) == result

    for a, b in [(1, 2), (1.0, 2.0), ([], 1), (None, None)]:
        try:
            two_str(a, b)
            assert False, f"Ожидалась ошибка для вызова: two_str({a}, {b})"
        except TypeError:
            pass

def test_int_float() -> None:
    for a, b, result in [(1, 2.0, 3.0), (0, 0.0, 0.0), (-5, 10.5, 5.5)]:
        assert int_float(a, b) == result

    for a, b in [("1", 2), (1, 2), ([], 1), (None, None)]:
        try:
            int_float(a, b)
            assert False, f"Ожидалась ошибка для вызова: int_float({a}, {b})"
        except TypeError:
            pass

test_two_int()
test_two_bool()
test_two_float()
test_two_str()
test_int_float()