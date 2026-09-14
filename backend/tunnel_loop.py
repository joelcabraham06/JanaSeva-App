import subprocess
import time

while True:
    try:
        p = subprocess.Popen([
            "ssh",
            "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3",
            "-o", "StrictHostKeyChecking=no",
            "-R", "80:127.0.0.1:8000",
            "nokey@localhost.run"
        ])
        p.wait()
    except Exception as e:
        pass
    time.sleep(2)
