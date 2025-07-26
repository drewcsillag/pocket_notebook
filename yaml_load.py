"""Handles marshalling from yaml to dict"""
from typing import TextIO, Dict, Any
from collections import defaultdict

import yaml

def parse_preserving_duplicates(src: TextIO) -> Dict:
    """Parse yaml, but handle duplicate keys by having the values be lists instead
    of whatever they would be"""

    # We deliberately define a fresh class inside the function,
    # because add_constructor is a class method and we don't want to
    # mutate pyyaml classes.
    class PreserveDuplicatesLoader(
        yaml.loader.Loader
    ):  # pylint: disable=too-many-ancestors
        """Loader that preserves duplicate key values"""

    def map_constructor(loader: Any, node: Any, deep: Any = False) -> Any:
        """Walk the mapping, recording any duplicate keys."""

        mapping = defaultdict(list)
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            value = loader.construct_object(value_node, deep=deep)

            mapping[key].append(value)

        # print("RESULT MAPPING", mapping)
        return mapping

    PreserveDuplicatesLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, map_constructor
    )  # type: ignore
    return yaml.load(src, PreserveDuplicatesLoader)
