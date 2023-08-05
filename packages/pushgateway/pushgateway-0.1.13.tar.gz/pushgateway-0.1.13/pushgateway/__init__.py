import argparse
from pushgateway.gateway import run
from pushgateway.config import default_config_file
from pushgateway.unit import register, deregister, printlog
import logging


PACKAGENAME = 'pushgateway'
ENTRY_POINT = "pushgateway"
DESCRIPTION = "A push gateway sending webthing properties updates to a openhab server"


def main():
    logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--command', metavar='command', required=True, type=str, help='the command. Supported commands are: listen (run the service), register (register and starts the service as a systemd unit, deregister (deregisters the systemd unit), log (prints the log)')
    parser.add_argument('--filename', metavar='filename', required=False, type=str,  help='the config filename')
    args = parser.parse_args()

    if args.filename is None:
        filename = default_config_file()
    else:
        filename = args.filename

    if args.command == 'listen':
        if filename is None:
            print("--filename has to be set")
        else:
            print("running " + PACKAGENAME + " with config " + filename)
            run(filename)
    elif args.command == 'register':
        if filename is None:
            print("--filename has to be set")
        else:
            print("register " + PACKAGENAME + " with config " + filename)
            register(PACKAGENAME, ENTRY_POINT, filename)
    elif args.command == 'deregister':
        deregister(PACKAGENAME)
    elif args.command == 'log':
        printlog(PACKAGENAME)
    else:
        print("usage " + ENTRY_POINT + " --help")


if __name__ == '__main__':
    main()

