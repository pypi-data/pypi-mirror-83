import argparse
import sys
from course_manager.db import CourseDb
from course_manager.db import DB
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description='Course Manager')
    subparsers = parser.add_subparsers(help='commands', dest='command')
    add_parser = subparsers.add_parser('add', help='Add a course')
    remove_parser = subparsers.add_parser('remove', help='Remove a course')
    update_parser = subparsers.add_parser('update', help='Update a course')
    list_parser = subparsers.add_parser('list', help='List courses')

    add_parser.add_argument('name', help='Name of the course')
    add_parser.add_argument('-c', '--current', help='Set current task')
    add_parser.add_argument('-n', '--next',  help='Set next task')

    remove_parser.add_argument('course_id', help='Remove a course by ID')

    update_parser.add_argument('course_id', help='ID of course to update')
    update_parser.add_argument('--name',
                               help='Name of the updated course')
    update_parser.add_argument('-c', '--current',
                               help='New current task')
    update_parser.add_argument('-n', '--next',
                               help='New next task')

    args = parser.parse_args(argv)
    course_db = CourseDb(DB)
    if args.command == 'add':
        course_db.add_course(name=args.name, current_task=args.current,
                             next_task=args.next)
    elif args.command == 'remove':
        course_db.remove_course(args.course_id)
    elif args.command == 'update':
        course_db.update_course(course_id=args.course_id, name=args.name,
                                current_task=args.current,
                                next_task=args.next)
    elif args.command == 'list':
        course_db.print_table()
    else:
        parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())
