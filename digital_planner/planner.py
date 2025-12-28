import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date

DATA_FILE = "data.json"

class DigitalPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Planner")
        self.root.geometry("600x500")

        self.data = {
            "tasks": [],
            "courses": [],
            "journal": {}
        }

        self.load_data()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.create_todo_tab()
        self.create_courses_tab()
        self.create_calendar_tab()
        self.create_journal_tab()

    # to-do list tab
    def create_todo_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="To-Do")

        self.task_entry = tk.Entry(tab, width=40)
        self.task_entry.pack(pady=10)

        tk.Button(tab, text="Add Task", command=self.add_task).pack()

        self.task_list = tk.Listbox(tab, width=60, height=15)
        self.task_list.pack(pady=10)

        tk.Button(tab, text="Delete Selected Task", command=self.delete_task).pack()

        self.refresh_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task == "":
            messagebox.showwarning("Warning", "Task cannot be empty.")
            return

        self.data["tasks"].append(task)
        self.task_entry.delete(0, tk.END)
        self.save_data()
        self.refresh_tasks()

    def delete_task(self):
        selected = self.task_list.curselection()
        if len(selected) == 0:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return

        index = selected[0]
        self.data["tasks"].pop(index)
        self.save_data()
        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.data["tasks"]:
            self.task_list.insert(tk.END, task)

    # courses tab
    def create_courses_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Courses")

        self.course_entry = tk.Entry(tab, width=40)
        self.course_entry.pack(pady=10)

        tk.Button(tab, text="Add Course", command=self.add_course).pack()

        self.course_list = tk.Listbox(tab, width=60, height=15)
        self.course_list.pack(pady=10)

        tk.Button(tab, text="Remove Selected Course", command=self.delete_course).pack()

        self.refresh_courses()

    def add_course(self):
        course = self.course_entry.get().strip()
        if course == "":
            messagebox.showwarning("Warning", "Course name cannot be empty.")
            return

        self.data["courses"].append(course)
        self.course_entry.delete(0, tk.END)
        self.save_data()
        self.refresh_courses()

    def delete_course(self):
        selected = self.course_list.curselection()
        if len(selected) == 0:
            messagebox.showwarning("Warning", "Select a course to remove.")
            return

        index = selected[0]
        self.data["courses"].pop(index)
        self.save_data()
        self.refresh_courses()

    def refresh_courses(self):
        self.course_list.delete(0, tk.END)
        for course in self.data["courses"]:
            self.course_list.insert(tk.END, course)

    # calendar tab
    def create_calendar_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Calendar")

        today = date.today().isoformat()
        tk.Label(tab, text=f"Today: {today}", font=("Arial", 14)).pack(pady=10)

        tk.Label(tab, text="Daily Notes / Tasks").pack()
        self.calendar_text = tk.Text(tab, width=60, height=15)
        self.calendar_text.pack(pady=10)

        if today in self.data["journal"]:
            self.calendar_text.insert(tk.END, self.data["journal"][today])

        tk.Button(tab, text="Save Today's Notes", command=self.save_today).pack()

    def save_today(self):
        today = date.today().isoformat()
        self.data["journal"][today] = self.calendar_text.get("1.0", tk.END).strip()
        self.save_data()
        messagebox.showinfo("Saved", "Today's notes saved.")

    # journal tab
    def create_journal_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Journal")

        tk.Label(tab, text="Journal Entry").pack(pady=5)
        self.journal_text = tk.Text(tab, width=60, height=18)
        self.journal_text.pack(pady=10)

        tk.Button(tab, text="Save Entry", command=self.save_journal).pack()

    def save_journal(self):
        today = date.today().isoformat()
        self.data["journal"][today] = self.journal_text.get("1.0", tk.END).strip()
        self.save_data()
        messagebox.showinfo("Saved", "Journal entry saved.")

    # persistence
    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.data = json.load(f)


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalPlanner(root)
    root.mainloop()