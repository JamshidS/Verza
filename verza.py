import argparse
from commands import (
    init, 
    add,
    commit,
)

def main():
    parser = argparse.ArgumentParser(description="Verza CLI Tool")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('init', help='Initialize a new Verza repository')

    add_parser = subparsers.add_parser('add', help='Add a new file to the Verza repository')
    add_parser.add_argument('files', nargs='+', help='File(s) to add')

    commit_parser = subparsers.add_parser("commit", help="Commit staged changes")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")

    args = parser.parse_args()

    if args.command == 'init':
        init.run()
    elif args.command == 'add':
        add.run(args.files)
    elif args.command == 'commit':
        commit.run(args.message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()