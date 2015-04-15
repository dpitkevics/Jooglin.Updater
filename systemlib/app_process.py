import psutil


def pkill(process_name):
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                proc.kill()
        except psutil.AccessDenied:
            pass