from itertools import repeat
from typing import (Any,
                    Hashable,
                    Mapping,
                    MutableMapping,
                    Tuple)

from hypothesis import given

from memoir import cached
from tests import strategies
from tests.utils import create_unique_object


@given(strategies.empty.immutable_mappings,
       strategies.unique_objects,
       strategies.positive_integers)
def test_empty_immutable_cache_map(cache: Mapping[Hashable, Any],
                                   argument: Hashable,
                                   attempts_count: int) -> None:
    wrapper = cached.map_(cache)

    result = wrapper(non_transparent_map)
    first_call_result = result(argument)

    assert all(result(argument) is not first_call_result
               for _ in repeat(None,
                               times=attempts_count))
    assert not cache


@given(strategies.empty.mutable_mappings,
       strategies.unique_objects,
       strategies.positive_integers)
def test_empty_mutable_cache_map(cache: MutableMapping[Hashable, Any],
                                 argument: Hashable,
                                 attempts_count: int) -> None:
    wrapper = cached.map_(cache)

    result = wrapper(non_transparent_map)
    first_call_result = result(argument)

    assert all(result(argument) is first_call_result
               for _ in repeat(None,
                               times=attempts_count))
    assert len(cache) == 1
    assert argument in cache
    assert cache[argument] is first_call_result


@given(strategies.identifiers,
       strategies.empty.tuples,
       strategies.identifiers,
       strategies.positive_integers)
def test_property(class_name: str,
                  bases: Tuple[type, ...],
                  property_name: str,
                  attempts_count: int) -> None:
    calls = []

    def getter(self) -> Any:
        object_ = non_transparent_map(self)
        calls.append(object_)
        return object_

    class_ = type(class_name, bases, {property_name: cached.property_(getter)})
    instance = class_()

    result = getattr(instance, property_name)

    assert all(getattr(instance, property_name) is result
               for _ in repeat(None,
                               times=attempts_count))
    assert len(calls) == 1
    assert result in calls


def non_transparent_map(argument: Hashable) -> Any:
    return create_unique_object()
