from keyword import iskeyword
from string import ascii_letters

from hypothesis import strategies

from tests.utils import create_unique_object


def is_not_keyword(string: str) -> bool:
    return not iskeyword(string)


identifiers_characters = strategies.sampled_from(ascii_letters + '_')
identifiers = (strategies.text(identifiers_characters,
                               min_size=1)
               .filter(str.isidentifier)
               .filter(is_not_keyword))
positive_integers = strategies.integers(1, 10 ** 5)
unique_objects = strategies.builds(create_unique_object)
