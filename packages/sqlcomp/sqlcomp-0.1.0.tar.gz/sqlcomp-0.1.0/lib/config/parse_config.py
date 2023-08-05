"""
Handles generating a mapping list of names to shorthand.
"""
from typing import Dict
from ast import literal_eval


def parse_config(config: str) -> Dict:
    """
    Generates a config map of words to shorthand representations.

    :param config: A string of config pairs from a file.
    """
    config = literal_eval(config)
    return config
