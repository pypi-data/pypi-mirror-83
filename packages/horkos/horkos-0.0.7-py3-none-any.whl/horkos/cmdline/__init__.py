import argparse

from horkos.cmdline import check


def _parse(args: list = None) -> dict:
    """Parse the given arguments and return them as a simple dictionary."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand', required=True)
    check_parser = subparsers.add_parser('check', help=check.__doc__)
    check.configure_parser(check_parser)
    return vars(parser.parse_args(args))


def main(args: list = None):
    """Run the horkos command."""
    parsed_args = _parse(args)
    handlers = {
        'check': check.main,
    }
    command = parsed_args.pop('subcommand')
    handlers[command](**parsed_args)
