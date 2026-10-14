import json

def first_launch():
    try:
        with open("tasks.json", "r")as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None

def add(arg):
    del_id = load_del_id()
    result = first_launch()
    if result is not None:
        data = result
        correct_id = max([x["id"] for x in data] + del_id) + 1
        new_task = {"id": correct_id,
                    "title": arg,
                    "complete": False}
        data.append(new_task)
        save_changes(data)
    else:
        data = []
        new_task = {"id": 1,
                "title": arg,
                "complete": False}
        data.append(new_task)
        save_changes(data)

def save_changes(data):
    with open("tasks.json", "w") as file:
        json.dump(data, file)

def list():
    result = first_launch()
    if result is None:
        print("Нет сохраненных целей!")
    else:
        with open("tasks.json", "r") as file:
            data = json.load(file)
        print(data)

def done(arg):
    data = first_launch()
    if data is not None:
        for i in data:
            if i["id"] == arg:
                i["complete"] = True
                is_id = True
                break
        if not is_id:
            print("Нет цели с таким id")
        else:
            print("Успех!")
            save_changes(data)
    else:
        print("Нет сохраненных целей!")

def delete(arg):
    result = first_launch()
    del_id = load_del_id()
    if result is not None:
        data = result
        is_id = False
        for i in data:
            if i["id"] == arg:
                data.remove(i)
                is_id = True
                break
        if not is_id:
            print("Нет цели с таким id")
        else:
            print("Успех!")
            save_changes_del_id(arg, del_id)
            save_changes(data)
    else:
        print("Нет сохраненных целей!")

def load_del_id():
    try:
        with open("del_id.json", "r") as file:
            del_id = json.load(file)
    except FileNotFoundError:
        del_id = []
    return del_id

def save_changes_del_id(arg, del_id):
    del_id.append(arg)
    with open("del_id.json", "w") as file:
        json.dump()