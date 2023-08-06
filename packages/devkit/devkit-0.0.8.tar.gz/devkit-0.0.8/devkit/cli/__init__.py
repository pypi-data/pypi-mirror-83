from devkit.core import module
from devkit.cli.parse import parse_args

def serve_webui(args):
    from devkit.web import server
    
    if args.debug == True:
        server.run(host=args.host, port=args.port, debug=True)
    else:
        print('>> Web UI production mode not available for now (add --debug)')


def main():
    args = parse_args()
    
    if args.command == 'web':
        serve_webui(args)
