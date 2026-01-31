from app.main import add, get_hello


def test_add():
    assert add(2, 3) == 5


def test_get_hello_default():
    assert get_hello("") == "Hello, World!"


def test_get_hello_name():
    assert get_hello("Alice") == "Hello, Alice!"