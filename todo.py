import json
import os

DATA_FILE = "todos.json"


def load_todos():
    """启动时读取 todos.json，文件不存在就返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def save_todos(todos):
    """把待办列表写回 todos.json。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def next_id(todos):
    """找出当前最大编号 +1，作为新加待办的编号。"""
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1


def show_todos(todos):
    if not todos:
        print("（还没有待办哦）")
        return
    print("\n----- 我的待办 -----")
    for t in todos:
        status = "[√]" if t["done"] else "[ ]"
        print(f'{t["id"]}. {status} {t["task"]}')
    print("--------------------\n")


def add_todo(todos):
    task = input("请输入待办内容：").strip()
    if not task:
        print("内容不能为空！")
        return
    todos.append({"id": next_id(todos), "task": task, "done": False})
    save_todos(todos)
    print("已添加！")


def mark_done(todos):
    try:
        tid = int(input("请输入要完成的编号："))
    except ValueError:
        print("请输入数字！")
        return
    for t in todos:
        if t["id"] == tid:
            t["done"] = True
            save_todos(todos)
            print("已标记为完成！")
            return
    print("没找到这个编号")


def delete_todo(todos):
    try:
        tid = int(input("请输入要删除的编号："))
    except ValueError:
        print("请输入数字！")
        return
    for i, t in enumerate(todos):
        if t["id"] == tid:
            del todos[i]
            save_todos(todos)
            print("已删除！")
            return
    print("没找到这个编号")


def main():
    todos = load_todos()
    while True:
        print("\n==== 待办清单 ====")
        print("1. 添加待办")
        print("2. 查看清单")
        print("3. 标记完成")
        print("4. 删除待办")
        print("5. 退出")
        choice = input("请选择：").strip()

        if choice == "1":
            add_todo(todos)
        elif choice == "2":
            show_todos(todos)
        elif choice == "3":
            mark_done(todos)
        elif choice == "4":
            delete_todo(todos)
        elif choice == "5":
            print("再见！待办已保存，下次打开还在。")
            break
        else:
            print("无效选择，请输入 1-5")


if __name__ == "__main__":
    main()
