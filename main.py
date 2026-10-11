import json
import argparse
data = []
is_data = True
try:
    with open("tasks.json", "r")as file:
        data = json.load(file)
except FileNotFoundError:
    is_data = None

parser = argparse.ArgumentParser()
action_group = parser.add_mutually_exclusive_group()
action_group.add_argument("--add", type=str, help="Название задачи")
action_group.add_argument("--list", action="store_true")
action_group.add_argument("--done", type=int, help="id задачи")
action_group.add_argument("--delete", type=int, help="id задачи")

args = parser.parse_args()

if args.add:
    if is_data is not None:   
        new_task = {"id": len(data)+1,
                    "title": args.add,
                    "complete": False}
        data.append(new_task)
    else:
        new_task = {"id": 1,
                "title": args.add,
                "complete": False}
        data.append(new_task)

    with open("tasks.json", "w") as file:
        json.dump(data, file)

elif args.list:
    with open("tasks.json", "r") as file:
        data = json.load(file)
    print(data)

elif args.done:
    with open("tasks.json", "r") as file:
        data = json.load(file)
    is_id = False
    for i in data:
        if i["id"] == args.done:
            i["complete"] = True
            is_id = True
            break
    if not is_id:
        print("Нет цели с таким id")
    else:
        print("Успех!")
        with open("tasks.json", "w") as file:
            json.dump(data, file)
elif args.delete:
    with open("tasks.json", "r") as file:
        data = json.load(file)
    is_id = False
    for i in data:
        if i["id"] == args.delete:
            data.remove(i)
            is_id = True
            break
    if not is_id:
        print("Нет цели с таким id")
    else:
        print("Успех!")
        with open("tasks.json", "w") as file:
            json.dump(data, file)