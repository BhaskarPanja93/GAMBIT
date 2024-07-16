from pathlib import Path


from internal.SecretEnums import *


for location in HostDetails.possibleFolderLocation.value:
    if Path(location).is_dir():
        folderLocation = location
        break
else:
    input("Project directory not found in SecretEnum...")


class RequiredFiles(Enum):
    webServerRunnable = str(Path(folderLocation, r"internal\_webserver_worker.py"))
    webServerRequired = [
        str(Path(folderLocation, r"internal\_webserver_worker.py")),
        str(Path(folderLocation, r"run_webserver.py"))
    ]


class FormPurposes(Enum):
    register = "register"
    login = "login"


class Routes(Enum):
    homePageRoute = "/better-education"
    WSRoute = f"{homePageRoute}_ws"


class WebsiteRelated(Enum):
    appName = "Test"
    title = "Study Well"
