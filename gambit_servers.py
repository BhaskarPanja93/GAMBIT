from autoReRun import AutoReRun
while True:
    try:
        from internal.Credentials import RequiredFiles, ServerSecrets
        break
    except: input("Credentials.py not found in /internal/")


toRun = {RequiredFiles.webServerRunnable: [ServerSecrets.fernetKey, str(ServerSecrets.webPort), str(ServerSecrets.cdPort)]}
toCheck = RequiredFiles.webServerRequired
interval = 1
AutoReRun(toRun, toCheck, interval)


toRun = {RequiredFiles.cdServerRunnable: [ServerSecrets.fernetKey, str(ServerSecrets.webPort), str(ServerSecrets.cdPort)]}
toCheck = RequiredFiles.cdServerRequired
interval = 1
AutoReRun(toRun, toCheck, interval)
