import argparse
from . import danfossclient
from .commands import UpdateCommand

def main():
    parser = argparse.ArgumentParser("pydanfossair")
    parser.add_argument("--host", action="store", required=True)
    parser.add_argument("--command", action="store", required=False)

    args = parser.parse_args()

    client = danfossclient.DanfossClient(args.host)

    if args.command is not None:
        if args.command == "boost_on":
            print("Activate boost: {0}".format(client.command(UpdateCommand.boost_activate)))

        if args.command == "boost_off":
            print("Activate boost: {0}".format(client.command(UpdateCommand.boost_deactivate)))
 
        if args.command == "bypass_on":
            print("Activate bypass: {0}".format(client.command(UpdateCommand.bypass_activate)))

        if args.command == "bypass_off":
            print("Activate bypass: {0}".format(client.command(UpdateCommand.bypass_deactivate)))

        if args.command == "automatic_bypass_off":
            print("Automtic bypass: {0}".format(client.command(UpdateCommand.automatic_bypass_deactivate)))

        if args.command == "automatic_bypass_on":
            print("Automtic bypass: {0}".format(client.command(UpdateCommand.automatic_bypass_activate)))
                   
    else:
        result = client.read_all()

        for key in result.keys():
            print("{0}: {1}".format(key, result.get(key)))

if __name__ == "__main__":
    main()
