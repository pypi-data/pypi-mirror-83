import os
import argparse
import platform
import textwrap

from mist_remote import run_in_mist_server, MissingParameter

HERE = os.path.dirname(__file__)

def msg(message: str, error: bool = False):
    print()
    print(f"[{'!' if error else '*'}] {message}")
    print()

def build_cli() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog='mist-remote',
        description='MIST Remote - Run MIST playbooks in remote MIST server')
    parser.add_argument('PLAYBOOK',
                        help="PLAYBOOK [param1=value1 param2=value2...]",
                        metavar="PLAYBOOK", nargs="+")
    parser.add_argument('-s', '--server',
                        default="http://127.0.0.1:9000",
                        help="setup MIST server")
    parser.add_argument('-q', '--quiet',
                        action="store_true",
                        default=False,
                        help="enables quiet mode")

    return parser


def main():

    #
    # Check python version
    #
    if platform.python_version_tuple() < ("3", "8"):
        print("\n[!] Python 3.8 or above is required\n")
        print("If you don't want to install Python 3.8. "
              "Try with Docker:\n")
        print("   $ docker run --rm cr0hn/mist -h")
        exit(1)

    cli = build_cli()

    parsed_args = cli.parse_args()

    #
    # Parse cli
    #
    playbook: str = ""
    params: dict = {}

    if not parsed_args.PLAYBOOK:
        msg("You can specify a playbook", error=True)
        exit(1)

    playbook = parsed_args.PLAYBOOK[0]

    if len(parsed_args.PLAYBOOK) > 1:
        for _tuple in parsed_args.PLAYBOOK[1:]:
            k, v = _tuple.split("=")

            params[k] = v

    server = parsed_args.server
    quiet = parsed_args.quiet

    try:
        ret = run_in_mist_server(
            server,
            playbook,
            quiet,
            params
        )

        print()
        print("-" * 30, "Console output", "-" * 30)
        print()
        print(ret)
    except MissingParameter as e:
        print()
        print("!" * 95)
        print(str(e))
        # print("\n".join(textwrap.wrap(str(e), 60)))
        print("!" * 95)
    except Exception as e:
        msg(str(e), error=True)

if __name__ == '__main__':
    main()
