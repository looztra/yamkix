"""Helper to deal with Yamkix configuration of the YAML instance."""

from ruamel.yaml import YAML

from yamkix.config import YamkixConfig

OPINIONATED_MAPPING_VALUE = 2
OPINIONATED_SEQUENCE_VALUE = 4
OPINIONATED_OFFSET_VALUE = 2


def get_opinionated_yaml_writer(
    yamkix_config: YamkixConfig,
) -> YAML:
    """Configure a yaml parser/formatter the `yamkix` way.

    Parameters:
        yamkix_config: a YamkixConfig instance
    Returns:
        a ruamel.yaml YAML instance, configured according to the YamkixConfig you provided and:<br/>
        <ul>
            <li>`mapping = 2` (map indent)</li>
            <li>`sequence = 4` (sequence indent)</li>
            <li>`offset = 2` (sequence dash offset)</li>
        </ul>
    """
    yaml = YAML(typ=yamkix_config.parsing_mode)
    yaml.explicit_start = yamkix_config.explicit_start
    yaml.explicit_end = yamkix_config.explicit_end
    yaml.default_flow_style = yamkix_config.default_flow_style
    yaml.preserve_quotes = yamkix_config.quotes_preserved
    yaml.width = yamkix_config.line_width
    if yamkix_config.dash_inwards:
        yaml.indent(
            mapping=OPINIONATED_MAPPING_VALUE, sequence=OPINIONATED_SEQUENCE_VALUE, offset=OPINIONATED_OFFSET_VALUE
        )
    return yaml
