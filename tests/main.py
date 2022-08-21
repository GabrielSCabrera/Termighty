"""
    Main testing utility for large-scale testing of program functionality
"""


def run_obj() -> bool:
    """
    Runs all the tests listed in src/tests/obj/;
    returns True if all tests succeed, False otherwise.
    """


def run_utils() -> bool:
    """
    Runs all the tests listed in src/tests/utils/;
    returns True if all tests succeed, False otherwise.
    """


def run_all() -> bool:
    """
    Runs all the tests listed in the src/tests/ subdirectories;
    returns True if all tests succeed, False otherwise.
    """
    run_obj()
    run_utils()


if __name__ == "__main__":
    run_all()
