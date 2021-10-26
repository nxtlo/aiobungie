import subprocess
import threading
from backend import app

if __name__ == '__main__':
    try:
        _app_thread = threading.Thread(target=app.main, name="app", daemon=True)
        _app_thread.start()
        with subprocess.Popen(
            ["cd", "frontend", "&&", "yarn", "start"],
            shell=True
        ) as proc:
            _, _ = proc.communicate()
            _app_thread.join()
    except KeyboardInterrupt:
        pass
