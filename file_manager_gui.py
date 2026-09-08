"""
File Manager GUI
A simple, professional desktop file manager built with Tkinter.

Run:
    python file_manager_gui.py
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from pathlib import Path


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("760x480")
        self.root.minsize(640, 420)

        self.current_dir = Path.cwd()

        self._setup_style()
        self._build_layout()
        self.refresh_list()

    # ---------------------------------------------------------------- UI setup
    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", padding=6)
        style.configure("Treeview", rowheight=24)
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Path.TLabel", foreground="#555555")

    def _build_layout(self):
        # Top bar: current directory + change button
        top = ttk.Frame(self.root, padding=(10, 10, 10, 5))
        top.pack(fill="x")

        ttk.Label(top, text="Working folder:", style="Header.TLabel").pack(side="left")
        self.path_label = ttk.Label(top, text=str(self.current_dir), style="Path.TLabel")
        self.path_label.pack(side="left", padx=8)

        ttk.Button(top, text="Change folder", command=self.change_directory).pack(side="right")
        ttk.Button(top, text="Refresh", command=self.refresh_list).pack(side="right", padx=6)

        # Main area: file list (left) + action buttons (right)
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        list_frame = ttk.Frame(main)
        list_frame.pack(side="left", fill="both", expand=True)

        columns = ("name", "type")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("name", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.column("name", width=320)
        self.tree.column("type", width=80, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(main, padding=(15, 0, 0, 0))
        btn_frame.pack(side="right", fill="y")

        actions = [
            ("New file", self.create_file),
            ("Read file", self.read_file),
            ("Update file", self.update_file),
            ("Delete file", self.delete_file),
            ("Rename file", self.rename_file),
            ("New folder", self.create_folder),
            ("Delete folder", self.delete_folder),
        ]
        for label, cmd in actions:
            ttk.Button(btn_frame, text=label, command=cmd, width=18).pack(pady=4, fill="x")

        # Bottom: status/log area
        bottom = ttk.Frame(self.root, padding=(10, 5, 10, 10))
        bottom.pack(fill="x")
        ttk.Label(bottom, text="Log", style="Header.TLabel").pack(anchor="w")

        self.log_box = tk.Text(bottom, height=6, state="disabled", wrap="word",
                                background="#f7f7f7", relief="solid", borderwidth=1)
        self.log_box.pack(fill="x")

    # ---------------------------------------------------------------- helpers
    def log(self, message, level="info"):
        colors = {"info": "#333333", "success": "#1a7f37", "error": "#c62828"}
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        start = self.log_box.index("end-2l")
        end = self.log_box.index("end-1l")
        tag = f"tag_{level}"
        self.log_box.tag_configure(tag, foreground=colors.get(level, "#333333"))
        self.log_box.tag_add(tag, start, end)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        try:
            entries = sorted(self.current_dir.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except OSError as e:
            self.log(f"Could not read folder: {e}", "error")
            return
        for entry in entries:
            kind = "File" if entry.is_file() else "Folder"
            self.tree.insert("", "end", values=(entry.name, kind))

    def selected_name(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0], "values")[0]

    def change_directory(self):
        chosen = filedialog.askdirectory(initialdir=self.current_dir)
        if chosen:
            self.current_dir = Path(chosen)
            self.path_label.configure(text=str(self.current_dir))
            self.refresh_list()
            self.log(f"Switched to {self.current_dir}")

    # ---------------------------------------------------------------- file actions
    def create_file(self):
        name = simpledialog.askstring("New file", "Enter filename:", parent=self.root)
        if not name:
            return
        path = self.current_dir / name
        if path.exists():
            messagebox.showerror("Error", "A file with that name already exists.")
            self.log(f"Create failed: {name} already exists", "error")
            return
        content = self._ask_multiline("File content", "Enter file content:")
        try:
            path.write_text(content or "")
            self.log(f"Created {name}", "success")
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Create failed: {e}", "error")
        self.refresh_list()

    def read_file(self):
        name = self.selected_name() or simpledialog.askstring("Read file", "Enter filename:", parent=self.root)
        if not name:
            return
        path = self.current_dir / name
        if not path.is_file():
            messagebox.showerror("Error", "File does not exist.")
            self.log(f"Read failed: {name} not found", "error")
            return
        try:
            content = path.read_text()
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Read failed: {e}", "error")
            return
        self._show_content_window(name, content)
        self.log(f"Opened {name}")

    def update_file(self):
        name = self.selected_name() or simpledialog.askstring("Update file", "Enter filename:", parent=self.root)
        if not name:
            return
        path = self.current_dir / name
        if not path.is_file():
            messagebox.showerror("Error", "File does not exist.")
            self.log(f"Update failed: {name} not found", "error")
            return
        addition = self._ask_multiline("Update file", "Enter content to append:")
        if addition is None:
            return
        try:
            with open(path, "a") as f:
                f.write(addition)
            self.log(f"Updated {name}", "success")
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Update failed: {e}", "error")

    def delete_file(self):
        name = self.selected_name() or simpledialog.askstring("Delete file", "Enter filename:", parent=self.root)
        if not name:
            return
        path = self.current_dir / name
        if not path.is_file():
            messagebox.showerror("Error", "File does not exist.")
            self.log(f"Delete failed: {name} not found", "error")
            return
        if not messagebox.askyesno("Confirm delete", f"Delete '{name}'? This cannot be undone."):
            return
        try:
            path.unlink()
            self.log(f"Deleted {name}", "success")
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Delete failed: {e}", "error")
        self.refresh_list()

    def rename_file(self):
        old_name = self.selected_name() or simpledialog.askstring("Rename file", "Enter current filename:", parent=self.root)
        if not old_name:
            return
        old_path = self.current_dir / old_name
        if not old_path.exists():
            messagebox.showerror("Error", "File does not exist.")
            self.log(f"Rename failed: {old_name} not found", "error")
            return
        new_name = simpledialog.askstring("Rename file", "Enter new name:", parent=self.root)
        if not new_name:
            return
        new_path = self.current_dir / new_name
        if new_path.exists():
            messagebox.showerror("Error", "A file with that name already exists.")
            self.log(f"Rename failed: {new_name} already exists", "error")
            return
        try:
            old_path.rename(new_path)
            self.log(f"Renamed {old_name} to {new_name}", "success")
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Rename failed: {e}", "error")
        self.refresh_list()

    # ---------------------------------------------------------------- folder actions
    def create_folder(self):
        name = simpledialog.askstring("New folder", "Enter folder name:", parent=self.root)
        if not name:
            return
        path = self.current_dir / name
        if path.exists():
            messagebox.showerror("Error", "A folder with that name already exists.")
            self.log(f"Create folder failed: {name} already exists", "error")
            return
        try:
            path.mkdir()
            self.log(f"Created folder {name}", "success")
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Create folder failed: {e}", "error")
        self.refresh_list()

    def delete_folder(self):
        name = self.selected_name() or simpledialog.askstring("Delete folder", "Enter folder name:", parent=self.root)
        if not name:
            return
        path = self.current_dir / name
        if not path.is_dir():
            messagebox.showerror("Error", "Folder does not exist.")
            self.log(f"Delete folder failed: {name} not found", "error")
            return
        has_contents = any(path.iterdir())
        if has_contents:
            confirm = messagebox.askyesno(
                "Folder not empty",
                f"'{name}' is not empty. Delete it and everything inside?"
            )
        else:
            confirm = messagebox.askyesno("Confirm delete", f"Delete folder '{name}'?")
        if not confirm:
            return
        try:
            if has_contents:
                shutil.rmtree(path)
            else:
                path.rmdir()
            self.log(f"Deleted folder {name}", "success")
        except OSError as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Delete folder failed: {e}", "error")
        self.refresh_list()

    # ---------------------------------------------------------------- small dialogs
    def _ask_multiline(self, title, prompt):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("380x220")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text=prompt, padding=10).pack(anchor="w")
        text = tk.Text(dialog, height=8, wrap="word")
        text.pack(fill="both", expand=True, padx=10)

        result = {"value": None}

        def on_ok():
            result["value"] = text.get("1.0", "end-1c")
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btns = ttk.Frame(dialog, padding=10)
        btns.pack(fill="x")
        ttk.Button(btns, text="Cancel", command=on_cancel).pack(side="right", padx=4)
        ttk.Button(btns, text="OK", command=on_ok).pack(side="right")

        dialog.wait_window()
        return result["value"]

    def _show_content_window(self, filename, content):
        window = tk.Toplevel(self.root)
        window.title(f"Viewing: {filename}")
        window.geometry("420x320")

        text = tk.Text(window, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", content)
        text.configure(state="disabled")

        ttk.Button(window, text="Close", command=window.destroy).pack(pady=(0, 10))


def main():
    root = tk.Tk()
    FileManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()