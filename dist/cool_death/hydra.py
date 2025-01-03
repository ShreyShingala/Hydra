# -*- coding: utf-8 -*-

import threading, sys, time, random as rm, tkinter as tk, os, psutil, subprocess, fcntl
from tkinter import ttk

root = tk.Tk()
root.withdraw()

hashed = "kill"  # REMEMBER TO CHANGE PASSWORD
windows = []  # list of windows
entries = []  # list of entries

firstTime = True
stop_event = threading.Event()

nameoffile = "watchdog"
nameofotherfile = "hydra.app"
base_dir = os.path.dirname(os.path.abspath(sys.argv[0])).split('/')
base_dir.pop(0)
path = "/"

died = False

# Create the directory allowing mayhem to begin
for i in range(len(base_dir)):
    if base_dir[i] == nameoffile or base_dir[i] == nameofotherfile:
        break
    else:
        path = os.path.join(path, base_dir[i])

temppath = nameoffile + ".app/Contents/MacOS/" + nameoffile
dogpath = os.path.join(path, temppath)
text_path = os.path.join(path, "hydra_var.txt")

# Functions that will actually run Hydra
def hydrafunc():
    def file_write(file_path, value):
        with open(file_path, 'w') as file:
            file.write(str(value))

    def file_read(file_path):
        with open(file_path, 'r') as file:
            return int(file.read())

    def remove():
        global entries, windows, died
        
        for entry in entries:  # Check all passwords
            result = entry.get()
            if result == hashed:
                file_write(text_path, 1)  # Tell watchdog to eliminate itself
                died = True
                for window in windows:
                    for widget in window.winfo_children():
                        if isinstance(widget, ttk.Label) and widget.cget("text") == "Good luck!":
                            widget.config(text="Congratulations", foreground="green", font=("Helvetica", 16))
                            widget.after(2000, lambda w=widget: w.config(text="You have slain Hydra"))
                            widget.after(4000, lambda w=widget: w.config(text="I told you I knew the password"))
                            widget.after(6000, lambda w=widget: w.config(text="Good luck with the cleanup"))
                        else:
                            widget.destroy()
                    
                    window.protocol("WM_DELETE_WINDOW", window.destroy)
                entries.clear()
                return
        
        if died == False:
            result_label.config(text="Incorrect Password. Try again :)", foreground="red")
            spawner()

    def spawner():
        current_value = file_read(text_path)
        for _ in range(current_value):
            create_window()
            time.sleep(float("0.0" + str(rm.randint(5, 9))))

    def create_window():
        global root, entries, windows, remove_entry, result_label

        tempdata = file_read(text_path)
        file_write(text_path, tempdata + 1)

        # Text in the window
        x = tk.Toplevel(root)  # Spawn window

        Line1 = "Lol you actually fell for it"
        Line2 = "This is Hydra, chop one head off and it grows more"
        Line3 = "To kill it put in the password"
        Line4 = "The easy way is to ask me, the hard way is to check my GitHub"
        Line5 = "Good luck!"
        
        ttk.Label(x, text=Line1, anchor="center").pack(pady=(5, 5))
        ttk.Label(x, text=Line2, anchor="center").pack(pady=(0, 5))
        ttk.Label(x, text=Line3, anchor="center").pack(pady=(0, 0))
        ttk.Label(x, text=Line4, anchor="center").pack(pady=(0, 0))
        ttk.Label(x, text=Line5, anchor="center").pack(pady=(10, 0))

        remove_entry = ttk.Entry(x)
        entries.append(remove_entry)
        remove_entry.pack(pady=(20, 0))

        ttk.Button(x, text="Remove", command=remove).pack(pady=(5, 0))
        
        result_label = ttk.Label(x)
        result_label.pack()

        screen_width = x.winfo_screenwidth()
        screen_height = x.winfo_screenheight()

        x.title("April Fools")
        x.geometry('600x225-' + str(rm.randint(0, screen_width - 600)) + '+' + str(rm.randint(0, screen_height - 175)))
        x.resizable(False, False)
        x.attributes("-topmost", True)
        x.protocol("WM_DELETE_WINDOW", spawner)
        x.protocol("WM_CLOSE", spawner)
        x.deiconify()
        x.bell()

        windows.append(x)

    spawner()

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
