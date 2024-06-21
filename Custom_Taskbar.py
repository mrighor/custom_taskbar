import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import webbrowser
import json
import requests
import os

class TaskbarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Taskbar")
        
        # Set the window position to the bottom right corner with a margin
        self.set_window_position()
        
        self.root.configure(bg='#2c3e50')
        self.root.geometry('300x200')  # Set a fixed size for the window
        
        self.buttons_frame = tk.Frame(root, bg='#34495e')
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.config_button = tk.Button(root, text="Config", command=self.open_config, bg='#2980b9', fg='white', font=('Helvetica', 10, 'bold'), relief=tk.FLAT)
        self.config_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Define the path to the buttons.json file
        self.buttons_file = os.path.join(os.path.expanduser("~"), "Documents", "Visual Studio 2010", "buttons.json")
        self.load_buttons()
    
    def set_window_position(self):
        margin_x = 110  # Margin from the right
        margin_y = 100  # Margin from the bottom
        
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = screen_width - width - margin_x
        y = screen_height - height - margin_y
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def open_config(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Config")
        config_window.configure(bg='#2c3e50')
        
        add_button = tk.Button(config_window, text="Add Button", command=self.add_button, bg='#27ae60', fg='white', font=('Helvetica', 10, 'bold'), relief=tk.FLAT)
        add_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        remove_button = tk.Button(config_window, text="Remove Button", command=self.open_remove_window, bg='#c0392b', fg='white', font=('Helvetica', 10, 'bold'), relief=tk.FLAT)
        remove_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    
    def add_button(self):
        name = simpledialog.askstring("Input", "Enter button name:", parent=self.root)
        if not name:
            return
        
        action = simpledialog.askstring("Input", "Enter URL, path to .exe or network path:", parent=self.root)
        if not action:
            return
        
        new_button = {
            "name": name,
            "action": action
        }
        
        self.save_button(new_button)
        self.create_button(new_button)
    
    def open_remove_window(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Button")
        remove_window.configure(bg='#2c3e50')
        
        with open(self.buttons_file, "r") as f:
            buttons = json.load(f)
        
        for button_data in buttons:
            btn = tk.Button(remove_window, text=button_data["name"], command=lambda bd=button_data: self.remove_button(bd, remove_window), bg='#c0392b', fg='white', font=('Helvetica', 10), relief=tk.FLAT)
            btn.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    
    def remove_button(self, button_data, window):
        try:
            with open(self.buttons_file, "r") as f:
                buttons = json.load(f)
            
            buttons = [btn for btn in buttons if btn["name"] != button_data["name"]]
            
            with open(self.buttons_file, "w") as f:
                json.dump(buttons, f)
            
            self.refresh_buttons()
            window.destroy()
        except FileNotFoundError:
            messagebox.showerror("Error", "No buttons to remove", parent=self.root)
    
    def create_button(self, button_data):
        button = tk.Button(self.buttons_frame, text=button_data["name"], command=lambda: self.execute_action(button_data["action"]), bg='#2980b9', fg='white', font=('Helvetica', 10), relief=tk.FLAT)
        button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    
    def execute_action(self, action):
        if action.startswith("http://") or action.startswith("https://"):
            webbrowser.open(action)
        elif action.startswith("\\\\"):
            self.open_file_explorer(action)
        else:
            try:
                subprocess.Popen(action)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {action}: {e}", parent=self.root)
    
    def open_file_explorer(self, path):
        try:
            subprocess.Popen(['explorer', path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open File Explorer at {path}: {e}", parent=self.root)
    
    def save_button(self, button_data):
        try:
            with open(self.buttons_file, "r") as f:
                buttons = json.load(f)
        except FileNotFoundError:
            buttons = []
        
        buttons.append(button_data)
        
        with open(self.buttons_file, "w") as f:
            json.dump(buttons, f)
    
    def load_buttons(self):
        try:
            with open(self.buttons_file, "r") as f:
                buttons = json.load(f)
                for button in buttons:
                    self.create_button(button)
        except FileNotFoundError:
            pass
    
    def refresh_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        self.load_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskbarApp(root)
    root.mainloop()
