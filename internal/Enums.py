from enum import Enum

class RequiredFiles(Enum):
    webServerRunnable = r"internal\_webserver_worker.py"
    webServerRequired = [
        r"internal\_webserver_worker.py"
    ]