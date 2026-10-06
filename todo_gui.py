import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "todos.json"


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def next_id(todos):
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1


class TodoApp:
    def __init__(self, root):
        self.todos = load_todos()
        self.root = root
        self.root.title("待办清单（窗口版）")
        self.root.geometry("460x560")

        # 待办内容输入框
        self.entry = tk.Entry(root, font=("微软雅黑", 12))
        self.entry.pack(pady=(15, 5), padx=15, fill="x")
        self.entry.insert(0, "待办内容...")
        self.entry.config(fg="gray")
        self.entry.bind("<FocusIn>", self._clear_placeholder)

        # 截止时间输入框
        tk.Label(root, text="截止时间（可选，如 2026-10-10 18:00）：",
                 font=("微软雅黑", 10)).pack(anchor="w", padx=15)
        self.deadline_entry = tk.Entry(root, font=("微软雅黑", 12))
        self.deadline_entry.pack(pady=(0, 8), padx=15, fill="x")

        btn_add = tk.Button(root, text="添加待办", command=self.add_todo,
                            font=("微软雅黑", 11), bg="#4CAF50", fg="white")
        btn_add.pack(pady=2)

        self.listbox = tk.Listbox(root, font=("微软雅黑", 12), height=12)
        self.listbox.pack(padx=15, pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="标记完成", command=self.mark_done,
                  font=("微软雅黑", 11), width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="删除", command=self.delete_todo,
                  font=("微软雅黑", 11), width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="编辑", command=self.edit_todo,
                  font=("微软雅黑", 11), width=10).pack(side="left", padx=5)

        self.refresh_list()

    def _clear_placeholder(self, event):
        if self.entry.get() == "待办内容...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for t in self.todos:
            status = "[√]" if t["done"] else "[ ]"
            deadline = t.get("deadline", "")
            suffix = f'  (截止: {deadline})' if deadline else ''
            self.listbox.insert(tk.END, f'{t["id"]}. {status} {t["task"]}{suffix}')

    def add_todo(self):
        task = self.entry.get().strip()
        if not task or task == "待办内容...":
            messagebox.showwarning("提示", "内容不能为空！")
            return
        deadline = self.deadline_entry.get().strip()
        self.todos.append({"id": next_id(self.todos), "task": task,
                           "done": False, "deadline": deadline})
        save_todos(self.todos)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "待办内容...")
        self.entry.config(fg="gray")
        self.deadline_entry.delete(0, tk.END)
        self.refresh_list()

    def get_selected(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("提示", "请先选择一条待办！")
            return None
        return idx[0]

    def mark_done(self):
        idx = self.get_selected()
        if idx is None:
            return
        self.todos[idx]["done"] = True
        save_todos(self.todos)
        self.refresh_list()

    def edit_todo(self):
        idx = self.get_selected()
        if idx is None:
            return
        todo = self.todos[idx]
        # 弹出编辑窗口
        win = tk.Toplevel(self.root)
        win.title("编辑待办")
        win.geometry("380x180")
        tk.Label(win, text="内容：").pack(anchor="w", padx=15, pady=(15, 0))
        entry = tk.Entry(win, font=("微软雅黑", 12))
        entry.insert(0, todo["task"])
        entry.pack(pady=(0, 5), padx=15, fill="x")
        tk.Label(win, text="截止时间：").pack(anchor="w", padx=15)
        deadline_entry = tk.Entry(win, font=("微软雅黑", 12))
        deadline_entry.insert(0, todo.get("deadline", ""))
        deadline_entry.pack(pady=(0, 8), padx=15, fill="x")

        def save():
            new_task = entry.get().strip()
            if not new_task:
                messagebox.showwarning("提示", "内容不能为空！")
                return
            todo["task"] = new_task
            todo["deadline"] = deadline_entry.get().strip()
            save_todos(self.todos)
            self.refresh_list()
            win.destroy()

        tk.Button(win, text="保存", command=save,
                  font=("微软雅黑", 11), width=10).pack(pady=5)

    def delete_todo(self):
        idx = self.get_selected()
        if idx is None:
            return
        del self.todos[idx]
        save_todos(self.todos)
        self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
