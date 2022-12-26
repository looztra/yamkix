"""Helper to deal with Yamkix configuration of the YAML instance."""
from ruamel.yaml import YAML

from yamkix.config import YamkixConfig


def get_opinionated_yaml_writer(
    yamkix_config: YamkixConfig,
) -> YAML:
    """Configure a yaml parser/formatter the yamkix way.

    Args:
        yamkix_config: a YamkixConfig instance
    Returns:
        a ruamel.yaml YAML instance
    """
    yaml = YAML(typ=yamkix_config.parsing_mode)
    yaml.explicit_start = yamkix_config.explicit_start
    yaml.explicit_end = yamkix_config.explicit_end
    yaml.default_flow_style = yamkix_config.default_flow_style
    yaml.preserve_quotes = yamkix_config.quotes_preserved
    yaml.width = yamkix_config.line_width
    if yamkix_config.dash_inwards:
        yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml
