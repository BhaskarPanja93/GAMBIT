from internal.Enums import RequiredFiles
from autoReRun import Runner


toRun = {RequiredFiles.webServerRunnable.value: []}
toCheck = RequiredFiles.webServerRequired.value
interval = 1
Runner(toRun, toCheck, interval).start()


# toRun = {RequiredFiles.apiServerRunnable.value: []}
# toCheck = RequiredFiles.apiServerRunnable.value
# interval = 1
# Runner(toRun, toCheck, interval).start()


# toRun = {RequiredFiles.cdnServerRunnable.value: []}
# toCheck = RequiredFiles.cdnServerRequired.value
# interval = 1
# Runner(toRun, toCheck, interval).start()


# toRun = {RequiredFiles.connServerRunnable.value: []}
# toCheck = RequiredFiles.connServerRequired.value
# interval = 1
# Runner(toRun, toCheck, interval).start()



