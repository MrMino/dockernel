import sys
from .app import run


def main() -> int:
    return run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
