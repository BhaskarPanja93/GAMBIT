from internal.Credentials import RequiredFiles, ServerSecrets
from autoReRun import AutoReRun


toRun = {RequiredFiles.webServerRunnable: [ServerSecrets.webFernetKey, str(ServerSecrets.webPort)]}
toCheck = RequiredFiles.webServerRequired
interval = 1
AutoReRun(toRun, toCheck, interval)



