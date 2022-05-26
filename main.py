
import os
import tempfile
import tkinter as tk
from tkinter import filedialog
import zipfile
from elevate import elevate
from pyquery import PyQuery as pq
from pyshortcuts import make_shortcut

window = tk.Tk()
elevate(show_console=False)


def Download(url: str, path: str, action: tk.Label):
    """
    Download the file
    """
    import requests
    import shutil
    print("Downloading")
    resp = requests.get(url)
    action.config(text="Installing...")
    data = resp.content
    tmpdir = tempfile.mkdtemp()
    tmpfile = os.path.join(tmpdir, "octave.zip")
    with open(tmpfile, "wb") as f:
        f.write(data)

    with zipfile.ZipFile(tmpfile, "r") as zip_ref:
        zip_ref.extractall(path)
    action.config(text="Setting up...")
    shutil.rmtree(tmpdir)
    make_shortcut(os.path.join(path, "Octave", "Octave.exe"), "Octave",
                  None, None, None, False, True, True),
    action.config(text="Done!")
    action.after(5000, lambda: window.destroy())


def PickDir(initial: str, dir_set: tk.Entry):
    """
    Pick the directory to use
    """
    chosen_dir = filedialog.askdirectory(initialdir=initial)
    current_text = dir_set.get()
    dir_set.delete(0, len(current_text))
    dir_set.insert(0, chosen_dir)


def Stage1():
    """
    Create the basic setup of the display
    """

    box = tk.Frame(width=500, height=300)
    box.pack()

    label = tk.Label(box, text="Octave", font=("Arial Bold", 50))
    label.pack()

    startbutton = tk.Button(box, text="Start", width=10,
                            height=2, command=Stage2)
    startbutton.pack()


def Stage2():
    """
    Allow the user to pick a directory
    """
    ch = window.winfo_children()
    for child in ch:
        child.destroy()

    box = tk.Frame(width=500, height=300)
    box.pack()

    label = tk.Label(box, text="Octave", font=("Arial Bold", 30))
    label.pack()

    dir_set = tk.Entry(box, width=50)
    #default_dir = r"C:\Program Files (x86)\Octave"
    default_dir = r"C:\Program Files"
    dir_set.insert(0, default_dir)
    dir_set.pack()

    dir_picker = tk.Button(box, text="📁", width=10,
                           command=lambda: PickDir(default_dir, dir_set))
    dir_picker.pack()

    next_button = tk.Button(box, text="Next", width=10,
                            command=lambda: Stage3(dir_set.get()))
    next_button.pack()


def Stage3(path: str):
    """
    Here is where we actually install it
    """
    ch = window.winfo_children()
    for child in ch:
        child.destroy()
    print(path)
    # If the directory does not exist, create it
    if not os.path.exists(path):
        os.makedirs(path)
    d = pq(url="https://github.com/ReCore-sys/Octave/releases")
    link = "https://github.com" + d(".Box-row > div > a").attr("href")
    title_lable = tk.Label(window, text="Octave", font=("Arial Bold", 50))
    title_lable.pack()
    current_action = tk.Label(
        window, text="Downloading...", font=("Arial Bold", 30))
    current_action.pack()
    Download(link, path, current_action)


Stage1()
window.geometry("500x300")
window.title("Octave Installer")
window.mainloop()
