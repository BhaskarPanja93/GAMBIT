from pathlib import Path

try: from SecretEnums import * ## change
except: from internal.SecretEnums import * ## change


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
        str(Path(folderLocation, r"run_servers.py"))
    ]
    apiServerRunnable = str(Path(folderLocation, r"internal\_api_worker.py"))
    apiServerRequired = [
        str(Path(folderLocation, r"internal\_api_worker.py")),
        str(Path(folderLocation, r"run_servers.py"))
    ]
    cdnServerRunnable = str(Path(folderLocation, r"internal\_cdn_worker.py"))
    cdnServerRequired = [
        str(Path(folderLocation, r"internal\_cdn_worker.py")),
        str(Path(folderLocation, r"run_servers.py"))
    ]
    connServerRunnable = str(Path(folderLocation, r"internal\_connection_worker.py"))
    connServerRequired = [
        str(Path(folderLocation, r"internal\_connection_worker.py")),
        str(Path(folderLocation, r"run_servers.py"))
    ]


class FormPurposes(Enum):
    submitRegister = "submitRegister"
    submitLogin = "submitLogin"
    startQuiz = "startQueue"
    submitQuizOption = "submitQuizOption"
    renderPostQuizQuestion = "renderPostQuizQuestion"
    renderQuizLobby = "preQuiz"
    renderCategories = "renderCategories"
    renderAuthPage = "renderAuthPage"
    renderMusicPage = "renderMusicPage"
    renderNotesPage = "renderNotesPage"
    renderContentMarketplacePage = "renderContentMarketplacePage"


class Routes(Enum):
    webHomePage = "/better-education"
    webWS = f"{webHomePage}-ws"
    internalConnection = f"{webHomePage}-conn"
    cdnMemoryContent = f"{webHomePage}-cdn-mem"
    cdnLiveContent = f"{webHomePage}-cdn-live"
    cdnFileContent = f"{webHomePage}-cdn-file"


class CoreValues(Enum):
    appName = "Gambit"
    title = "Study Well"


class CDNFileType(Enum):
    font = "font"
    image = "image"
    video = "video"
    css = "css"
    html = "html"
    js = "js"


class Fonts(Enum):
    GothamBlack = f"/{Routes.cdnFileContent.value}?type={CDNFileType.font.value}?name=GothamBlack.ttf"

