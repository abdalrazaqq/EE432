import tkinter as tk
from tkinter import messagebox, ttk
import winsound
import datetime


class Task:
    def __init__(self, description, priority, completed=False, due_date=None):
        self.description = description
        self.priority = priority
        self.completed = completed
        self.due_date = due_date


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, priority, due_date=None):
        if any(task.description == description for task in self.tasks):
            messagebox.showwarning("Duplicate", "Task already exists!")
            return False
        self.tasks.append(Task(description, priority, due_date=due_date))
        self.tasks.sort(key=lambda x: ["High", "Medium", "Low"].index(x.priority))
        return True

    def delete_task(self, description):
        self.tasks = [task for task in self.tasks if task.description != description]
        return True

    def toggle_completion(self, description):
        for task in self.tasks:
            if task.description == description:
                task.completed = not task.completed
                return True
        return False

    def get_sorted_tasks(self):
        return sorted(self.tasks, key=lambda x: ["High", "Medium", "Low"].index(x.priority))


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("800x700")
        self.root.configure(bg="#2C3E50")

        self.manager = TaskManager()

        style = ttk.Style()
        style.configure("TButton", padding=10, font=("Arial", 12), background="#3498DB")
        style.configure("TLabel", foreground="white", background="#2C3E50", font=("Arial", 12))

        # Input Section
        input_frame = ttk.Frame(root)
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Task Description:").grid(row=0, column=0, sticky="w")
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=1, column=0, padx=5, sticky="ew")

        ttk.Label(input_frame, text="Priority:").grid(row=0, column=1, sticky="w")
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                          values=["High", "Medium", "Low"], width=10)
        self.priority_menu.grid(row=1, column=1, padx=5)

        ttk.Label(input_frame, text="Due Date:").grid(row=0, column=2, sticky="w")
        self.due_date_var = tk.StringVar()
        self.due_date_picker = ttk.Combobox(input_frame, textvariable=self.due_date_var,
                                            values=self.generate_due_dates(), width=12)
        self.due_date_picker.grid(row=1, column=2, padx=5)

        self.add_btn = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        self.add_btn.grid(row=1, column=3, padx=5)

        # Task List
        list_frame = ttk.Frame(root)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.task_listbox = tk.Listbox(list_frame, width=80, height=20,
                                       font=("Arial", 12), selectbackground="#3498DB")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        self.task_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.task_listbox.bind("<Double-Button-1>", self.toggle_completion)
        self.task_listbox.bind("<Delete>", self.delete_task)

        self.display_tasks()

    def generate_due_dates(self):
        today = datetime.datetime.today()
        return [(today + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 31)]

    def add_task(self):
        description = self.task_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get() or "No due date"

        if description:
            if self.manager.add_task(description, priority, due_date):
                self.clear_inputs()
                messagebox.showinfo("Success", "Task added successfully!")
                winsound.Beep(1000, 200)
                self.display_tasks()
        else:
            messagebox.showwarning("Error", "Please enter a task description!")

    def clear_inputs(self):
        self.task_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.due_date_var.set("")

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.manager.get_sorted_tasks():
            status = "✔" if task.completed else "✘"
            priority_icon = {"High", "Medium", "Low"}.get(task.priority, "")
            due_date = task.due_date if task.due_date else "No due date"
            self.task_listbox.insert(tk.END,
                                     f"{status} | {task.description} | {priority_icon} {task.priority} | 📅 {due_date}")

    def toggle_completion(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            task_text = self.task_listbox.get(selection[0])
            description = task_text.split("|")[1].strip()
            if self.manager.toggle_completion(description):
                self.display_tasks()

    def delete_task(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            task_text = self.task_listbox.get(selection[0])
            description = task_text.split("|")[1].strip()
            if messagebox.askyesno("Confirm Delete", "Delete this task?"):
                if self.manager.delete_task(description):
                    self.display_tasks()
                    messagebox.showinfo("Success", "Task deleted successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()