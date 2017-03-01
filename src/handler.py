# encoding: utf-8

import json
import random

_proverbs = None


def load_proverbs():
    global _proverbs

    if _proverbs is None:
        with file('hungarian_proverbs.json', 'r') as fp:
            _proverbs = json.loads(fp.read())

    return _proverbs


def get_random_proverb():
    global _proverbs

    return random.choice(_proverbs)


def lambda_handler(event, context):
    load_proverbs()

    proverb = get_random_proverb()

    return proverb


if __name__ == '__main__':
    print lambda_handler(None, None)
