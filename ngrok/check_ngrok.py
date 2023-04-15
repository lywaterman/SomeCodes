import os
import argparse
import subprocess
import sys
import signal

main_pids= None

def get_process_id(name):
    global main_pids
    result = []
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                cmdline = f.read().decode('utf-8')
                if name in cmdline:
                    result.append(int(pid))
    print(result)
    main_pids = result
    return result

def get_env_var(name, var_name):
    for pid in get_process_id(name):
        with open(f"/proc/{pid}/environ", "rb") as f:
            env_str = f.read().decode("utf-8")
            env_list = env_str.split('\0')
            for env in env_list:
                key, _, value = env.partition('=')
                if key == var_name:
                    return value
    return None

process_name = "main"
var_name = "NGROK_URL"          
var_value = get_env_var(process_name, var_name)
if var_value:
    print(f"{var_name}={var_value}")

parser = argparse.ArgumentParser(description="My program")
parser.add_argument("url", help="the url to update")

args = parser.parse_args()

print(args.url, var_value)
if (args.url == var_value):
    print("no need change")
else:
    print("need change")
    print(var_name, args.url)
    if (main_pids is not None) and len(main_pids) > 0:
        print(main_pids[0])
        os.kill(main_pids[0], signal.SIGKILL)
    env_vars = os.environ.copy()
    env_vars[var_name] = args.url 
    process = subprocess.Popen(["nohup /root/main >/dev/null 2>&1 &"], env=env_vars, shell=True)
    print(process)
