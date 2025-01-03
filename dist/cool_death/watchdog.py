import os, time, subprocess, psutil, fcntl, signal, sys

nameoffile = "hydra"
nameofotherfile = "watchdog.app"
selfname = "watchdog"

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
hydrapath = os.path.join(path, temppath)
textpath = os.path.join(path, "hydra_var.txt")

# Function to find or start the Hydra process
def find_or_start_process(process_name, firsttime, hydrapath):
    process = None
    if firsttime:
        for p in psutil.process_iter(['name']):
            if p.info['name'] == process_name:
                process = psutil.Process(p.pid)
                break
    if process is None:
        process = subprocess.Popen([hydrapath], stdin=subprocess.DEVNULL, preexec_fn=os.setsid)
    return process

# Check if the script is already running
def check_if_already_running():
    lock_file_path = "/tmp/watchdog.lock"
    global lock_file
    lock_file = open(lock_file_path, 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit(1)

# Terminate Hydra and Watchdog processes
def terminate_process():
    current_pid = os.getpid()
    for p in psutil.process_iter(['pid', 'name']):
        if p.info['name'] == nameoffile or p.info['name'] == selfname:
            if p.info['pid'] != current_pid:
                os.kill(p.info['pid'], signal.SIGTERM)

if __name__ == "__main__":
    check_if_already_running()

    firsttime = True
    process_name = "hydra"
    process = find_or_start_process(process_name, firsttime, hydrapath)

    while True:
        with open(textpath, "r") as file:
            data = int(file.read())
            file.close()
        if data == 1:
            sys.exit()

        if isinstance(process, subprocess.Popen):
            if process.poll() is not None:
                process = find_or_start_process(process_name, firsttime, hydrapath)
        elif isinstance(process, psutil.Process):
            if not process.is_running():
                process = find_or_start_process(process_name, firsttime, hydrapath)

        time.sleep(0.2)
