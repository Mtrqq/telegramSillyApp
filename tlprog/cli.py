import argparse

from tlprog.progress import PredefinedStyle


def cmdline_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser("tlprog")

    parser.add_argument("target")
    parser.add_argument("--label", "-l", default="")
    parser.add_argument("--timeout", "-t", type=float, required=True)
    parser.add_argument("--interval", "-i", type=float, default=0.05)

    parser.add_argument_group("attachments")
    parser.add_argument("--text", default=None)
    parser.add_argument("--file", type=argparse.FileType("rb"), default=None)
    parser.add_argument("--let-me", dest="let_me", default=None)

    parser.add_argument(
        "--style",
        type=lambda x: PredefinedStyle.from_string(x.upper()).value,
        default=PredefinedStyle.CIRCLES.value,
    )

    arguments = parser.parse_args()

    if arguments.let_me is not None:
        if arguments.file is not None or arguments.text is not None:
            parser.error(
                "Unable to use Let Me Google in combination with text/file attachments"
            )

    return arguments
