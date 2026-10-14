import argparse
import database_processing

parser = argparse.ArgumentParser()
action_group = parser.add_mutually_exclusive_group()
action_group.add_argument("--add", type=str, help="Название задачи")
action_group.add_argument("--list", action="store_true")
action_group.add_argument("--done", type=int, help="id задачи")
action_group.add_argument("--delete", type=int, help="id задачи")

args = parser.parse_args()

if args.add:
    database_processing.add(args.add)

elif args.list:
    database_processing.list()

elif args.done:
    database_processing.done(args.done)

elif args.delete:
    database_processing.delete(args.delete)