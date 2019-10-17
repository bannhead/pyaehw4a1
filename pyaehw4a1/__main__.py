import argparse
import json

from . import aehw4a1
from .commands import UpdateCommand
from .commands import ReadCommand

def main():
    parser = argparse.ArgumentParser("aehw4a1")
    parser.add_argument("--host", action="store", required=True)
    parser.add_argument("--command", action="store", required=False)

    args = parser.parse_args()

    client = aehw4a1.AehW4a1(args.host)

    if args.command is None:
        command = "status_102_0"
    else:
        command = args.command
    
    if command in ReadCommand.__dict__ or command in UpdateCommand.__dict__:
        parsed = json.loads(client.command(command))
        print("AC",args.host,command,":\n",json.dumps(parsed, indent=4, sort_keys=False))
    else:
        raise Exception("Unknown command: {0}".format(command))

if __name__ == "__main__":
    main()
