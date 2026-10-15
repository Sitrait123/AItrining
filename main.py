import sys
import argparse
import database_processing
import json 
parser = argparse.ArgumentParser()
action_group = parser.add_mutually_exclusive_group()
action_group.add_argument("--add", type=str, help="Название задачи")
action_group.add_argument("--list", action="store_true")
action_group.add_argument("--done", type=int, help="id задачи")
action_group.add_argument("--delete", type=int, help="id задачи")

if len(sys.argv) == 1:
    parser.print_help()

args = parser.parse_args()


if args.add:
    if not args.add.strip():
        print("Название не должно быть пустым")
    else:
        try:
            print(database_processing.add(args.add))
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден")

elif args.list:
    try:
        result_list = database_processing.list()
        if not result_list:
            print(f"ID     STATUS   TITLE\n____________________\nНет сохраненных целей!")
        else:
            print(result_list)
    except json.JSONDecodeError:
        print("Ошибка: Файл поврежден")

elif args.done or args.done == 0:
    if args.done <=0:
        print("ID не может быть меньше 1")
    else:
        try:
            result_done = database_processing.done(args.done)
            if result_done == 0:
                print("Нет цели с таким id")
            elif result_done is None:
                print("Нет сохраненных целей!")
            else:
                print(result_done)
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден")


elif args.delete or args.delete ==0:
    if args.delete <=0:
        print("ID не может быть меньше 1")
    else:
        try:
            result_delete = database_processing.delete(args.delete)
            if result_delete == 0:
                print("Нет сохраненных целей!")
            elif result_delete is None:
                print("Нет сохраненных целей!")
            else:
                print(result_delete)
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден")