from types import MappingProxyType

from hypothesis import strategies

mutable_mappings = strategies.builds(dict)
immutable_mappings = mutable_mappings.map(MappingProxyType)
tuples = strategies.tuples()
