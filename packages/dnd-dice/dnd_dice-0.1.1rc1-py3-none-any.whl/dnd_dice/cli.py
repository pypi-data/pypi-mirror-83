"""Console script for dnd_dice."""
import argparse
import sys

from dnd_dice.dnd_dice import start_dnd_shell


def main():
    """Console script for dnd_dice."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='log file name prefix')
    args = parser.parse_args()
    start_dnd_shell(args.name)
    return 0
