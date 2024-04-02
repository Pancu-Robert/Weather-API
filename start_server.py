import subprocess

try:
    subprocess.run(["python3", "init_db.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running init_db.py: {e}")

try:
    subprocess.run(["python3", "main.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running main.py: {e}")