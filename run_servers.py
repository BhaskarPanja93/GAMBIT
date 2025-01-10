from internal.Enums import RequiredFiles
from autoReRun import AutoReRun


toRun = {RequiredFiles.webServerRunnable.value: []}
toCheck = RequiredFiles.webServerRequired.value
interval = 1
AutoReRun(toRun, toCheck, interval)



