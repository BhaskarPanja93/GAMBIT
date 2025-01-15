from internal.Credentials import RequiredFiles, ServerSecrets
from autoReRun import AutoReRun


toRun = {RequiredFiles.webServerRunnable: [ServerSecrets.fernetKey, str(ServerSecrets.webPort), str(ServerSecrets.cdPort)]}
toCheck = RequiredFiles.webServerRequired
interval = 1
AutoReRun(toRun, toCheck, interval)


# toRun = {RequiredFiles.cdServerRunnable: [ServerSecrets.fernetKey, str(ServerSecrets.webPort), str(ServerSecrets.cdPort)]}
# toCheck = RequiredFiles.cdServerRequired
# interval = 1
# AutoReRun(toRun, toCheck, interval)



