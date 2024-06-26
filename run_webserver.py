from internal.Enums import RequiredFiles
from autoReRun import Runner


toRun = {RequiredFiles.webServerRunnable.value: []}
toCheck = RequiredFiles.webServerRequired.value
interval = 2


Runner(toRun, toCheck, interval).start()
