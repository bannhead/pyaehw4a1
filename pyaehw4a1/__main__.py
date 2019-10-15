import argparse

from . import aehw4a1
from .commands import UpdateCommand

def main():
    parser = argparse.ArgumentParser("aehw4a1")
    parser.add_argument("--host", action="store", required=True)
    parser.add_argument("--command", action="store", required=False)

    args = parser.parse_args()

    client = aehw4a1.AehW4a1(args.host)

    if args.command is not None:
        if args.command in UpdateCommand.__dict__:
            print("AC",args.host,args.command,":",client.command(args.command))
        else:
            raise Exception("Unknown command: {0}".format(args.command))
        #print("AC",args.host,args.command,":",client.command(args.command))
    else:
        result = client.read_all()
        for key in result.keys():
            print("{0}: {1}".format(key, result.get(key)))

if __name__ == "__main__":
    main()
