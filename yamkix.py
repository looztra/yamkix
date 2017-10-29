#!/usr/bin/python
"""Load a yaml file and save it formatted according to some rules"""
import argparse
from ruamel.yaml import YAML


def parse_cli():
    """Parse the cli args"""
    my_args = dict()
    parser = argparse.ArgumentParser(
        description='''Format yaml input file.
            By default, explicit_start is `On`, explicit_end is `Off`\
            and array elements are pushed inwards the start of the \
            matching sequence. Comments are preserved thanks to default \
            parsing mode `rt`.
        ''')
    parser.add_argument('-i',
                        '--input',
                        required=True,
                        help='the file to parse')
    parser.add_argument('-t',
                        '--typ',
                        required=False,
                        default='rt',
                        help='the yaml parser mode. Can be `safe` or `rt`')
    parser.add_argument('-o', '--output',
                        required=False,
                        help='the name of the file to generate \
                              (same as input file if not specied)')
    parser.add_argument('-n', '--no-explicit-start',
                        action='store_true',
                        help='by default, explicit start of the yaml doc \
                                is `On`, you can disable it with this option')
    parser.add_argument('-e', '--explicit-end',
                        action='store_true',
                        help='by default, explicit end of the yaml doc \
                                is `Off`, you can enable it with this option')
    parser.add_argument('-q', '--no-quotes-preserved',
                        action='store_true',
                        help='by default, quotes are preserverd \
                                you can disable this with this option')
    parser.add_argument('-f', '--default-flow-style',
                        action='store_true',
                        help='enable the default flow style \
                                `Off` by default. In default flow style \
                                (with typ=`rt`), maps and lists are written \
                                like json')
    parser.add_argument('-d', '--no-dash-inwards',
                        action='store_true',
                        help='by default, dash are pushed inwards \
                                use `--no-dash-inwards` to have the dash \
                                start at the sequence level')

    args = parser.parse_args()

    if args.output is not None:
        my_args['output'] = args.output
    else:
        my_args['output'] = args.input
    if args.typ not in ["safe", "rt"]:
        raise ValueError(
            "'%s' is not a valid value for option --typ. "
            "Allowed values are 'safe' and 'rt'" % args.type)
    my_args['typ'] = args.typ
    my_args['input'] = args.input
    my_args['explicit_start'] = not args.no_explicit_start
    my_args['explicit_end'] = args.explicit_end
    my_args['default_flow_style'] = args.default_flow_style
    my_args['dash_inwards'] = not args.no_dash_inwards
    my_args['quotes_preserved'] = not args.no_quotes_preserved
    print("Processing: file=" + my_args['input'] +
          ", output=" + my_args['output'] +
          ", typ=" + my_args['typ'] +
          ", explicit_start=" + str(my_args['explicit_start']) +
          ", explicit_end=" + str(my_args['explicit_end']) +
          ", default_flow_style=" + str(my_args['default_flow_style']) +
          ", quotes_preserved=" + str(my_args['quotes_preserved']) +
          ", dash_inwards=" + str(my_args['dash_inwards']))
    return my_args


def format_yaml(input_file,
                output_file,
                explicit_start=True,
                explicit_end=False,
                default_flow_style=False,
                dash_inwards=True,
                quotes_preserved=True,
                parsing_mode='rt'):
    """
    Load a file and save it formated :
    :param input_file: the input file
    :param output_file: the output file
    :param explicit_start: write the start of the yaml doc even when there is \
                            only one done in the file
    :param default_flow_style: if False, block style will be used for nested \
                                 arrays/maps
    :param dash_inwards: push dash inwards if True
    :param quotes_preserved: preserve quotes if True
    :param parsing_typ: safe or roundtrip (rt) more
    """
    yaml = YAML(typ=parsing_mode)
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    yaml.default_flow_style = default_flow_style
    yaml.preserve_quotes = quotes_preserved
    if dash_inwards:
        yaml.indent(mapping=2, sequence=4, offset=2)

    with open(input_file, 'rt') as f_input:
        parsed = yaml.load_all(f_input.read())

    with open(output_file, 'wt') as out:
        yaml.dump_all(parsed, out)


def main():
    '''(re)format yaml'''
    parsed_args = parse_cli()
    format_yaml(input_file=parsed_args['input'],
                output_file=parsed_args['output'],
                explicit_start=parsed_args['explicit_start'],
                explicit_end=parsed_args['explicit_end'],
                default_flow_style=parsed_args['default_flow_style'],
                dash_inwards=parsed_args['dash_inwards'],
                quotes_preserved=parsed_args['quotes_preserved'],
                parsing_mode=parsed_args['typ'])


if __name__ == '__main__':
    main()
