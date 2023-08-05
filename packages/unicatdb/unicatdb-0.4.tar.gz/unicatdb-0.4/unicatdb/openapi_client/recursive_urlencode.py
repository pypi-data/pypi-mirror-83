import urllib.parse
from typing import List, Tuple, Union


def deep_object_urlencode(data: List[Tuple[str, Union[str, dict]]]):
    """URL-encode with Swagger deeoObject style parameters support.

    Inspired by: https://stackoverflow.com/a/4014164
    """

    def q(string):
        return urllib.parse.quote_plus(str(string))

    pairs = []

    for key, value in data:
        if type(value) is dict:
            for dict_key, dict_value in value.items():
                pairs.append("%s[%s]=%s" % (q(key), q(dict_key), q(dict_value)))
        else:
            pairs.append("%s=%s" % (q(key), q(value)))

    return '&'.join(pairs)
