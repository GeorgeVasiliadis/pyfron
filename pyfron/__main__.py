import argparse
import os.path

from .env import configure_env
from .preparation import populate_image_dir
from .run import run


def main():
    parser = argparse.ArgumentParser(prog="pyfron", description="An OpenDR-based face recognition CLI app")

    parser.add_argument("--env", default="default_env",
                        help="use environment ENV. If it doesn't exist, ENV will be created")

    parser.add_argument("--from-dir", metavar="DIR",
                        help="add images from DIR directory to the predefined test or reference directory. Used "
                             "with populate-* command.")

    parser.add_argument("command", metavar="COMMAND", choices=["run", "populate-test", "populate-reference"])

    args = parser.parse_args()

    config = configure_env(args.env)

    if args.command == "run":
        run(config)

    elif args.command == "populate-test":
        test_dir = args.from_dir or "."

        test_dir = os.path.join(test_dir, "images")
        target_dir = os.path.join(config.TEST_DIR, "images")

        populate_image_dir(test_dir, target_dir)

    elif args.command == "populate-reference":
        ref_dir = args.from_dir or config.LFW_DIR

        ref_dir = os.path.join(ref_dir, "images")
        target_dir = os.path.join(config.REFERENCE_DB_DIR, "images")

        populate_image_dir(ref_dir, target_dir)


if __name__ == "__main__":
    main()
