import json

def first_launch():
    try:
        with open("tasks.json", "r")as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        raise

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
        try:
            data = []
            new_task = {"id": correct_id,
                    "title": arg,
                    "complete": False}
            data.append(new_task)
            save_changes(data)
        except ValueError:
            data = []
            new_task = {"id": correct_id,
                    "title": arg,
                    "complete": False}
            data.append(new_task)
            save_changes(data)
    return new_task

def save_changes(data):
    with open("tasks.json", "w") as file:
        json.dump(data, file)

def list():
    border = "-"
    indent = " "
    status_border = 4
    result = first_launch()
    if result is None:
        return f"ID{indent * ((m_len_id + 3) - len(str(i['id'])))}STATUS   TITLE\n{border * 12}\nНет сохраненных целей!"
    else:
        with open("tasks.json", "r") as file:
            data = json.load(file)
        m_len_id = len(str(max(x["id"] for x in data)))
        m_len_title = max(x["title"] for x in data)
        id_border = 4 + m_len_id
        title_border = 4 + m_len_title
        prin = f"ID{indent * m_len_id}STATUS   TITLE\n{border * (id_border + title_border + status_border)}\n"
        for i in data:
            prin +=f"{i['id']}{indent * ((m_len_id + 3) - len(str(i['id'])))}{prin_status(i)}      {i['title']}\n"
        return prin
    
def prin_status(i):
    if i["complete"]:
        return "[x]"
    else:
        return "[ ]"

def done(arg):
    data = first_launch()
    is_id = False
    if data is not None:
        for i in data:
            if i["id"] == arg:
                i["complete"] = True
                is_id = True
                break
        if not is_id:
            return "Нет цели с таким id"
        else:
            save_changes(data)
            return i
    else:
        return "Нет сохраненных целей!"

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
            return "Нет цели с таким id"
        else:
            save_changes_del_id(arg, del_id)
            save_changes(data)
            return i
    else:
        return "Нет сохраненных целей!"

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
        json.dump(del_id, file)