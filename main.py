import argparse
import database_processing
import json 
parser = argparse.ArgumentParser()
action_group = parser.add_mutually_exclusive_group()
action_group.add_argument("--add", type=str, help="Название задачи")
action_group.add_argument("--list", action="store_true")
action_group.add_argument("--done", type=int, help="id задачи")
action_group.add_argument("--delete", type=int, help="id задачи")

args = parser.parse_args()


if args.add:
    if not args.add.strip():
        print("Название не должно быть пустым")
    try:
        print(database_processing.add(args.add))
    except json.JSONDecodeError:
        print("Ошибка: Файл поврежден")

elif args.list:
    try:
        print(database_processing.list())
    except json.JSONDecodeError:
        print("Ошибка: Файл поврежден")

elif args.done or args.done == 0:
    if args.done <=0:
        print("ID не может быть меньше 1")
    else:
        try:
            print(database_processing.done(args.done))
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден")


elif args.delete or args.delete ==0:
    if args.delete <=0:
        print("ID не может быть меньше 1")
    else:
        try:
            print(database_processing.delete(args.delete))
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден")