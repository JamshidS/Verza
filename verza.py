import argparse
from commands import (
    init, 
    add,
)

def main():
    parser = argparse.ArgumentParser(description="Verza CLI Tool")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('init', help='Initialize a new Verza repository')

    add_parser = subparsers.add_parser('add', help='Add a new file to the Verza repository')
    add_parser.add_argument('files', nargs='+', help='File(s) to add')

    args = parser.parse_args()

    if args.command == 'init':
        init()
    elif args.command == 'add':
        add(args.files)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()