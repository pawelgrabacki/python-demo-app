from datetime import datetime, timezone


def add(a: int, b: int) -> int:
    return a + b


def get_hello(name: str) -> str:
    name = (name or "").strip() or "World"
    return f"Hello, {name}!"


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(get_hello("Jenkins"))
    print(f"Time: {now}")
    print(f"2 + 3 = {add(2, 3)}")


if __name__ == "__main__":
    
    main()