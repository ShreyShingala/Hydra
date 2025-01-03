# -*- coding: utf-8 -*-

# lots of imports
from tkinter import ttk
import threading, sys, time, random as rm, tkinter as tk, os, psutil, subprocess, fcntl

root = tk.Tk()
root.withdraw()

hashed = "kill"  # REMEMBER TO CHANGE PASSWORD
windows = []  # list da windows
entries = []  # list da entries

firstTime = True
stop_event = threading.Event()

nameoffile = "watchdog"
nameofotherfile = "hydra.app"
base_dir = os.path.dirname(os.path.abspath(sys.argv[0])).split('/')
base_dir.pop(0)
path = "/"

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
            file.close()

    def file_read(file_path):
        with open(file_path, 'r') as file:
            data = int(file.read())
            file.close()
            return data

    def remove():
        global entries
        for entry in entries:  # Check all passwords
            result = entry.get()
            if result == hashed:
                file_write(text_path, 1)  # Tell watchdog to eliminate itself
                stop_event.set()  # Set stop event
                sys.exit()  # Exit program

        result_label.config(text="Incorrect Password. Try again :)", foreground="red")
        spawner()

    def spawner():
        current_value = file_read(text_path)
        for _ in range(current_value):
            create_window()
            time.sleep(float("0.0" + str(rm.randint(5, 9))))  # Random delay

    def create_window():
        global root, remove_entry, result_label

        # Increment the integer at pipe_path
        tempdata = file_read(text_path)
        file_write(text_path, tempdata + 1)

        # Text in the window
        Line1 = "Lol you actually fell for it"
        Line2 = "This is Hydra, chop one head off and it grows more"
        Line3 = "To kill it put in the password"
        Line4 = "The easy way is to ask me, the hard way is to check my GitHub"
        Line5 = "Good luck!"

        x = tk.Toplevel(root)  # Spawn window

        # Set random background color
        bg = random_color()
        x.configure(bg=bg)

        # Apply custom style to ttk widgets
        style = ttk.Style()
        style.configure("Custom.TLabel", background=bg, foreground=random_color())
        style.configure("Custom.TEntry", fieldbackground=bg, background=bg)
        style.configure("Custom.TButton", background=bg)

        # Add text lines
        ttk.Label(x, text=Line1, anchor="center", style="Custom.TLabel").pack(pady=(5, 5))
        ttk.Label(x, text=Line2, anchor="center", style="Custom.TLabel").pack(pady=(0, 5))
        ttk.Label(x, text=Line3, anchor="center", style="Custom.TLabel").pack(pady=(0, 0))
        ttk.Label(x, text=Line4, anchor="center", style="Custom.TLabel").pack(pady=(0, 0))
        ttk.Label(x, text=Line5, anchor="center", style="Custom.TLabel").pack(pady=(10, 0))

        # Entry for removal
        remove_entry = ttk.Entry(x, style="Custom.TEntry")
        entries.append(remove_entry)
        remove_entry.pack(pady=(20, 0))

        ttk.Button(x, text="Remove", command=remove, style="Custom.TButton").pack(pady=(5, 0))

        # Results Label
        result_label = ttk.Label(x, style="Custom.TLabel")
        result_label.pack()

        # Screen parameters
        screen_width = x.winfo_screenwidth()
        screen_height = x.winfo_screenheight()

        # Additional parameters
        x.title("April Fools")
        x.geometry('600x225-' + str(rm.randint(0, screen_width - 600)) + '+' + str(rm.randint(0, screen_height - 175)))
        x.resizable(False, False)
        x.attributes("-topmost", True)
        x.protocol("WM_DELETE_WINDOW", spawner)
        x.protocol("WM_CLOSE", spawner)
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


def random_color():
    return "#{:06x}".format(rm.randint(0, 0xFFFFFF))


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
