import argparse
from . import __version__


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    print(f'py_package: {__version__}')


if __name__ == "__main__":
    main()
