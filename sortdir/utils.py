import sys

from colorama import Fore


def print_error(text):
    print(Fore.RED + text + Fore.RESET, file=sys.stderr)
