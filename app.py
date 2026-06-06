import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import subprocess
import sys
import threading
import queue
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def browse_folder(var):
    path = filedialog.askdirectory()
    if path:
        var.set(path)


def folder_row(parent, label, var):
    """A labeled folder-picker row."""
    frame = ttk.Frame(parent)
    frame.pack(fill="x", padx=10, pady=3)
    ttk.Label(frame, text=label, width=14, anchor="w").pack(side="left")
    ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=4)
    ttk.Button(frame, text="Browse…", command=lambda: browse_folder(var)).pack(side="left")


def run_script(args, output_widget, run_btn):
    """Run a script in a background thread, streaming output line by line."""
    run_btn.config(state="disabled")
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)

    q = queue.Queue()

    def worker():
        try:
            proc = subprocess.Popen(
                [sys.executable] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=SCRIPT_DIR,
            )
            for line in proc.stdout:
                q.put(line)
            proc.wait()
        except Exception as e:
            q.put(f"\nError: {e}\n")
        finally:
            q.put(None)  # sentinel

    def poll():
        try:
            while True:
                line = q.get_nowait()
                if line is None:
                    run_btn.config(state="normal")
                    return
                output_widget.insert(tk.END, line)
                output_widget.see(tk.END)
        except queue.Empty:
            pass
        output_widget.after(50, poll)

    threading.Thread(target=worker, daemon=True).start()
    output_widget.after(50, poll)


def make_output(parent):
    out = scrolledtext.ScrolledText(parent, height=18, font=("Courier New", 9), wrap="word")
    out.pack(fill="both", expand=True, padx=10, pady=4)
    return out


def make_run_button(parent, callback):
    bar = ttk.Frame(parent)
    bar.pack(fill="x", padx=10, pady=(0, 8))
    btn = ttk.Button(bar, text="Run", command=callback)
    btn.pack(side="right")
    return btn


# ---------------------------------------------------------------------------
# Tab builders
# ---------------------------------------------------------------------------

def tab_find_duplicates(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Find Duplicates")

    folder_var = tk.StringVar()
    folder_row(tab, "Folder:", folder_var)
    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        run_script(["find-duplicate-files.py", f"--folder={folder_var.get()}"], out, btn)

    btn = make_run_button(tab, on_run)


def tab_find_underscores(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Find Underscores")

    folder_var = tk.StringVar()
    folder_row(tab, "Folder:", folder_var)
    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        run_script(["find-files-with-underscores.py", f"--folder={folder_var.get()}"], out, btn)

    btn = make_run_button(tab, on_run)


def tab_find_not_matching(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Find Not Matching")

    folder_var = tk.StringVar()
    folder_row(tab, "Folder:", folder_var)
    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        run_script(["find-mp3s-not-matching.py", f"--folder={folder_var.get()}"], out, btn)

    btn = make_run_button(tab, on_run)


def tab_find_uppercase(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Find Uppercase Meta")

    folder_var = tk.StringVar()
    folder_row(tab, "Folder:", folder_var)
    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        run_script(["find-uppercase-metadata-mp3s.py", f"--folder={folder_var.get()}"], out, btn)

    btn = make_run_button(tab, on_run)


def tab_fuzzy_find(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Fuzzy Find Files")

    source_var = tk.StringVar()
    target_var = tk.StringVar()
    not_found_only = tk.BooleanVar()
    sort_var = tk.BooleanVar()

    folder_row(tab, "Source:", source_var)
    folder_row(tab, "Target:", target_var)

    opts = ttk.Frame(tab)
    opts.pack(fill="x", padx=10, pady=2)
    ttk.Checkbutton(opts, text="Not-found only", variable=not_found_only).pack(side="left", padx=4)
    ttk.Checkbutton(opts, text="Sort into found/not-found folders", variable=sort_var).pack(side="left", padx=4)

    out = make_output(tab)

    def on_run():
        if not source_var.get() or not target_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select both source and target folders.\n")
            return
        args = [
            "fuzzy-find-files.py",
            f"--source={source_var.get()}",
            f"--target={target_var.get()}",
        ]
        if not_found_only.get():
            args.append("--not-found-only")
        if sort_var.get():
            args.append("--sort")
        run_script(args, out, btn)

    btn = make_run_button(tab, on_run)


def tab_rename_mp3s(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Rename MP3s")

    folder_var = tk.StringVar()
    format_var = tk.StringVar(value="full")
    dry_run_var = tk.BooleanVar(value=True)

    folder_row(tab, "Folder:", folder_var)

    opts = ttk.Frame(tab)
    opts.pack(fill="x", padx=10, pady=2)
    ttk.Label(opts, text="Format:").pack(side="left")
    ttk.Radiobutton(opts, text="Full  (Artist - Album - 01 Title)", variable=format_var, value="full").pack(side="left", padx=6)
    ttk.Radiobutton(opts, text="Simple  (01 Title)", variable=format_var, value="simple").pack(side="left", padx=6)

    dry_frame = ttk.Frame(tab)
    dry_frame.pack(fill="x", padx=10, pady=2)
    ttk.Checkbutton(dry_frame, text="Dry run (preview only, no changes)", variable=dry_run_var).pack(side="left")

    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        args = [
            "rename-mp3s.py",
            f"--folder={folder_var.get()}",
            f"--format={format_var.get()}",
        ]
        if dry_run_var.get():
            args.append("--dry-run")
        run_script(args, out, btn)

    btn = make_run_button(tab, on_run)


def tab_sort_mp3s(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Sort MP3s")

    folder_var = tk.StringVar()
    folder_row(tab, "Folder:", folder_var)
    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        run_script(["sort-mp3s.py", f"--folder={folder_var.get()}"], out, btn)

    btn = make_run_button(tab, on_run)


def tab_sort_by_date(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Sort by Date")

    folder_var = tk.StringVar()
    folder_row(tab, "Folder:", folder_var)
    out = make_output(tab)

    def on_run():
        if not folder_var.get():
            out.delete("1.0", tk.END)
            out.insert(tk.END, "Please select a folder.\n")
            return
        run_script(["sort-by-creation-date.py", f"--folder={folder_var.get()}"], out, btn)

    btn = make_run_button(tab, on_run)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = tk.Tk()
    root.title("MP3 Tools")
    root.minsize(700, 520)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    tab_find_duplicates(notebook)
    tab_find_underscores(notebook)
    tab_find_not_matching(notebook)
    tab_find_uppercase(notebook)
    tab_fuzzy_find(notebook)
    tab_rename_mp3s(notebook)
    tab_sort_mp3s(notebook)
    tab_sort_by_date(notebook)

    root.mainloop()


if __name__ == "__main__":
    main()
