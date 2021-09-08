from collections import OrderedDict
from typing import Dict

import yaml
import codecs


def _adjust_ordereddict_to_yaml():
    def represent_odict(dumper, instance):
        return dumper.represent_mapping("tag:yaml.org,2002:map", instance.items())

    yaml.Dumper.ignore_aliases = lambda *args: True
    yaml.add_representer(OrderedDict, represent_odict)

    def construct_odict(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor("tag:yaml.org,2002:map", construct_odict)


def output_yaml(tree: Dict[str, any], filepath: str):
    _adjust_ordereddict_to_yaml()
    with codecs.open(filepath, "w", "utf-8") as f:
        yaml.dump(tree, f, encoding="utf-8", allow_unicode=True, default_flow_style=False)
