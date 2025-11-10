import tkinter as tk
from tkinter import messagebox
import os

# ---- File to save tasks ----
TASKS_FILE = "tasks.txt"

# ---- Main window setup ----
root = tk.Tk()
root.title("To-Do List Manager")
root.geometry("360x450")
root.resizable(False, False)

# ---- Functions ----
def load_tasks():
    """Load tasks from file if available."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                task = line.strip()
                if task:
                    listbox_tasks.insert(tk.END, task)
                    color_task(task, listbox_tasks.size() - 1)

def save_tasks():
    """Save all tasks to file."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        for i in range(listbox_tasks.size()):
            f.write(listbox_tasks.get(i) + "\n")

def color_task(task, index):
    """Apply color depending on completion state."""
    if task.startswith("✔ "):
        listbox_tasks.itemconfig(index, {'fg': 'green'})
    else:
        listbox_tasks.itemconfig(index, {'fg': 'black'})

def add_task():
    """Add a new task."""
    task = entry_task.get().strip()
    if task:
        listbox_tasks.insert(tk.END, task)
        color_task(task, listbox_tasks.size() - 1)
        entry_task.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Enter a task before adding!")

def delete_task():
    """Delete selected task."""
    try:
        index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

def mark_done():
    """Mark selected task as done."""
    try:
        index = listbox_tasks.curselection()[0]
        task = listbox_tasks.get(index)
        if not task.startswith("✔ "):
            task = "✔ " + task
            listbox_tasks.delete(index)
            listbox_tasks.insert(index, task)
            color_task(task, index)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark as done!")

def clear_all():
    """Delete all tasks."""
    if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"):
        listbox_tasks.delete(0, tk.END)
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)

def sort_tasks():
    """Sort tasks alphabetically (done tasks stay at the bottom)."""
    all_tasks = list(listbox_tasks.get(0, tk.END))
    done = [t for t in all_tasks if t.startswith("✔ ")]
    pending = [t for t in all_tasks if not t.startswith("✔ ")]
    pending.sort(key=lambda s: s.lower())
    listbox_tasks.delete(0, tk.END)
    for t in pending + done:
        listbox_tasks.insert(tk.END, t)
        color_task(t, listbox_tasks.size() - 1)
    save_tasks()

# ---- UI Elements ----
frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=10)

listbox_tasks = tk.Listbox(
    frame_tasks,
    height=15,
    width=45,
    selectmode=tk.SINGLE,
    font=("Arial", 10)
)
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame_tasks)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
listbox_tasks.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_tasks.yview)

entry_task = tk.Entry(root, width=30, font=("Arial", 11))
entry_task.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Add", width=9, command=add_task).grid(row=0, column=0, padx=3, pady=2)
tk.Button(button_frame, text="Delete", width=9, command=delete_task).grid(row=0, column=1, padx=3, pady=2)
tk.Button(button_frame, text="Done", width=9, command=mark_done).grid(row=0, column=2, padx=3, pady=2)
tk.Button(button_frame, text="Sort", width=9, command=sort_tasks).grid(row=1, column=0, padx=3, pady=2)
tk.Button(button_frame, text="Clear All", width=9, command=clear_all).grid(row=1, column=2, padx=3, pady=2)

# ---- Load saved tasks ----
load_tasks()

root.mainloop()
