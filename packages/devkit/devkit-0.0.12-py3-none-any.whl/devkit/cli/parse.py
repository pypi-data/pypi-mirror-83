import argparse
import sys

def parse_args(args):
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # parse web ui commands
    webui_parser = subparsers.add_parser('web', help="Serve devkit webui with built-in web server.")
    webui_parser.add_argument('--debug', action='store_true', default=False, help='Run flask web server in debug mode.')
    webui_parser.add_argument('--host', type=str, default='localhost', help='Define host on which webui is exposed.')
    webui_parser.add_argument('--port', type=int, default=5000, help='Define port on which webui is exposed.')
    webui_parser.set_defaults(command='web')

    # parse args and abort with help if no command is passed
    parsed_args = parser.parse_args(args)

    if getattr(parsed_args, 'command', None) is None:
        parser.print_help()
        sys.exit(1)  

    return parsed_args
