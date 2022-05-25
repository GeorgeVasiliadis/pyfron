import argparse
import os.path

from .env import configure_env
from .preparation import populate_image_dir
from .recognizers import print_available_recognizers
from .run import run


def main():
    parser = argparse.ArgumentParser(prog="pyfron", description="An OpenDR-based face recognition CLI app")

    parser.add_argument("--env", default="default_env",
                        help="use environment ENV. If it doesn't exist, ENV will be created")

    parser.add_argument("--model", default="", help="specifies which model will be used")

    parser.add_argument("--list-models", action="store_true", help="prints all the registered models")

    parser.add_argument("--from-dir", metavar="DIR",
                        help="add images from DIR directory to the predefined test or reference directory. Used "
                             "with populate-* commands")

    parser.add_argument("command", metavar="COMMAND", nargs='?', choices=["run", "populate-test", "populate-reference"])

    args = parser.parse_args()

    config = configure_env(args.env)

    if args.command == "run":
        run(config, args.model)

    elif args.command in ["populate-test", "populate-reference"]:
        from_dir = args.from_dir or "."

        if args.command == "populate-test":
            target_dir = os.path.join(config.TEST_DIR)
        elif args.command == "populate-reference":
            target_dir = os.path.join(config.REFERENCE_DB_DIR, "images")
        else:
            raise ValueError("Bad COMMAND choice")

        populate_image_dir(from_dir, target_dir)

    if args.list_models:
        print_available_recognizers()


if __name__ == "__main__":
    main()
