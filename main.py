import argparse

from controller import Controller
def create_parser():
    parser = argparse.ArgumentParser(
        prog="DozeGuard", description="A linux utility to keep your laptop awake."
    )

    parser.add_argument(
        "command",
        choices=['start','stop','status'],
        help="command to execute"
    )

    parser.add_argument(
        "minutes",
        nargs="?",
        type=int,
        help="Duration in minutes(omit for unlimited)"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    controller = Controller()

    if args.command == "start":
        started = controller.start(args.minutes)
        if started:
            print("dozeGuard starated")
        else:
            print("A session is already active.")

    elif args.command == "stop":
        controller.stop()
        print("dozeguard stopped")
    elif args.command == "status":
        if controller.is_active():
            print("Status:Active")
        else:
            print("status:Inactive")

if __name__ ==  "__main__":
    main()




# done
