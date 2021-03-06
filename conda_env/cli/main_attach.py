from argparse import RawDescriptionHelpFormatter
from ..utils.notebooks import current_env, Notebook
from conda.cli import common
from ..env import from_environment


description = """
Embeds information describing your conda environment
into the notebook metadata
"""

example = """
examples:
    conda env attach -n root notebook.ipynb
    conda env attach -r user/environment notebook.ipynb
"""


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'attach',
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
        help=description,
        epilog=example,
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-n', '--name',
        action='store',
        help='local environment definition',
        default=None
    )
    group.add_argument(
        '-r', '--remote',
        action='store',
        help='remote environment definition',
        default=None
    )
    p.add_argument(
        '--force',
        action='store_true',
        default=False,
        help='Replace existing environment definition'
    )
    p.add_argument(
        'notebook',
        help='notebook file',
        action='store',
        default=None
    )
    common.add_parser_json(p)
    p.set_defaults(func=execute)


def execute(args, parser):
    if args.name is not None:
        prefix = common.get_prefix(args)
        content = from_environment(args.name, prefix).to_dict()
    else:
        content = {'remote': args.remote}

    print("Environment {} will be attach into {}".format(args.name, args.notebook))
    nb = Notebook(args.notebook)
    if nb.inject(content, args.force):
        print("Done.")
    else:
        print("The environment couldn't be attached due:")
        print(nb.msg)
