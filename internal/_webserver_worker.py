from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from dynamicWebsite import *
updatePackage()
from internal.Enums import *


# def sendRegister(viewerObj: BaseViewer):
#     registerHTML = f"""
#         <form id="songForm" onsubmit="return submit_ws(this)" autocomplete="off">
#             {viewerObj.addCSRF(FormPurposes.register.value)}
#             <label for="songName">Register:</label><br>
#             <input type="text" id="songName" name="songName"><br><br>
#             <button class="text-gray-500 focus:"type="submit">Register</button>
#         </form>"""
#     viewerObj.queueTurboAction(registerHTML, "register", viewerObj.turboApp.methods.update)


def sendLogin(viewerObj: BaseViewer):
    registerHTML = f"""

            <button class="focus:border-blue-500 text-gray-500 text-2xl sm:max-w-md flex-wrap">LOL</button>

        <form id="songForm" onsubmit="return submit_ws(this)" autocomplete="off">
            {viewerObj.addCSRF(FormPurposes.login.value)}
            <label for="songName">Login:</label><br>
            <input type="text" id="songName" name="songName"><br><br>
            <button type="submit">Login</button>
        </form>"""
    viewerObj.queueTurboAction(registerHTML, "login", viewerObj.turboApp.methods.update)


def navBar(viewerObj: BaseViewer):
    navigation_bar = f"""
    
    <nav class="bg-neutral-300">
        <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div class="relative flex items-center justify-between h-16">
                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="flex-shrink-0 flex items-center">
                        <a href="#" class="text-white text-2xl">Gambit</a>
                    </div>
                    <div class="hidden sm:block sm:ml-6">
                        <div class="flex space
                        -x-4">
                            <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Contact</a>
                        </div>
                    </div>  
                </div>
                <div class="hidden sm:block sm:ml-6">
                    <div class="flex space
                    -x-4">
                        <a href="#" class="text-gray-300 hover:bg-blue-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
                        <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg">
    <div class="rounded-md bg-white shadow-xs">
      <!-- Snipped  -->
    </div>
  </div>
    </nav>
    
    
    """

    viewerObj.queueTurboAction(navigation_bar, "navBar", viewerObj.turboApp.methods.update)



def homePage(viewerObj: BaseViewer):

    navBar(viewerObj)
    homePageHTML = f"""
    <nav class="bg-neutral-300">
        <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div class="relative flex items-center justify-between h-16">
                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="flex-shrink-0 flex items-center">
                        <a href="#" class="text-white text-2xl">Gambit</a>
                    </div>
                    <div class="hidden sm:block sm:ml-6">
                        <div class="flex space
                        -x-4">
                            <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Contact</a>
                        </div>
                    </div>  
                </div>
                <div class="hidden sm:block sm:ml-6">
                    <div class="flex space
                    -x-4">
                        <a href="#" class="text-gray-300 hover:bg-blue-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
                        <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg">
    <div class="rounded-md bg-white shadow-xs">
      <!-- Snipped  -->
    </div>
  </div>
    </nav> 
    
    <div class="bg-gray-800">
        <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div class="relative flex items-center justify-between h-16">
                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="hidden sm:block sm:ml-6">
                        <button class="text-white px-3 py-2 rounded-md text-sm font-medium border">Hello</button>
                    </div>
                </div>
            </div>
        </div>
        """
    viewerObj.queueTurboAction(homePageHTML, "homePage", viewerObj.turboApp.methods.update)


def loginPage(viewerObj: BaseViewer):
    login = f"""  
    
    <nav class="bg-neutral-300">
        <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div class="relative flex items-center justify-between h-16">
                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="flex-shrink-0 flex items-center">
                        <a href="#" class="text-white text-2xl">Gambit</a>
                    </div>
                    <div class="hidden sm:block sm:ml-6">
                        <div class="flex space-x-4">
                            <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Contact</a>
                        </div>
                    </div>
                </div>
                <div class="hidden sm:block sm:ml-6">
                    <div class="flex space
                    -x-4">
                        <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
                        <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
                    </div>
                </div>
            </div>
        </div>
    </nav> 
    """

    viewerObj.queueTurboAction(login, "loginPage", viewerObj.turboApp.methods.update)


def registerPage(viewerObj: BaseViewer):
    registration = f"""
    
    
    <nav class="bg-neutral-300">
        <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div class="relative flex items-center justify-between h-16">
                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="flex-shrink-0 flex items-center">
                        <a href="#" class="text-white text-2xl">Study Well</a>
                    </div>
                    <div class="hidden sm:block sm:ml-6">
                        <div class="flex space
                        -x-4">
                            <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
                            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Contact</a>
                        </div>
                    </div>
                </div>
                <div class="hidden sm:block sm:ml-6">
                    <div class="flex space
                    -x-4">
                        <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
                        <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
                    </div>
                </div>
            </div>
        </div>
    </nav> 
    """

    viewerObj.queueTurboAction(registration, "registerPage", viewerObj.turboApp.methods.update)


def testPage(viewerObj: BaseViewer):
    testingpage = f"""
    <div id="app" class="w-full max-w-xs">
        <div id="loginForm">
            <h2 class="font-bold text-lg mb-4">Login</h2>
            <input type="text" placeholder="Username" class="border p-2 w-full mb-4">
            <input type="password" placeholder="Password" class="border p-2 w-full mb-4">
            <button class="bg-blue-500 text-white p-2 w-full mb-4">Login</button>
            <p class="text-center">Don't have an account? <button onclick="showRegister()" class="text-blue-500">Register</button></p>
        </div>
        <div id="registerForm" class="hidden">
            <h2 class="font-bold text-lg mb-4">Register</h2>
            <input type="text" placeholder="Username" class="border p-2 w-full mb-4">
            <input type="email" placeholder="Email" class="border p-2 w-full mb-4">
            <input type="password" placeholder="Password" class="border p-2 w-full mb-4">
            <button class="bg-green-500 text-white p-2 w-full mb-4">Register</button>
            <p class="text-center">Already have an account? <button onclick="showLogin()" class="text-blue-500">Login</button></p>
        </div>
    </div>
    <script>
        function showLogin() {{
            document.getElementById('loginForm').style.display = 'block';
            document.getElementById('registerForm').style.display = 'none';
        }}

        function showRegister() {{
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'block';
        }}

        showLogin();
    </script>
    """

    viewerObj.queueTurboAction(testingpage, "testPage", viewerObj.turboApp.methods.update)



def newVisitorCallback(viewerObj: BaseViewer):
    initial = "<div id=\"testPage\"></div>"
    viewerObj.queueTurboAction(initial, "mainDiv", viewerObj.turboApp.methods.update)
    navBar(viewerObj)
    homePage(viewerObj)
    # sendRegister(viewerObj)
    # sendLogin(viewerObj)


def formSubmitCallback(viewerObj: BaseViewer, form: dict):
    if form is not None:
        purpose = form.pop("PURPOSE")

        if purpose == FormPurposes.register.value:
            print(form)

        elif purpose == FormPurposes.login.value:
            print(form)

    else:
        print("Disconnected: ", viewerObj.viewerID)


extraHeads = """<script src="https://cdn.tailwindcss.com"></script>
    <script src="https://https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.2.1/flowbite.min.js"></script>
            """
bodyBase = """<body class=""><div id="mainDiv"><div></body>"""

baseApp, turboApp = createApps(formSubmitCallback, newVisitorCallback, WebsiteRelated.appName.value,
                               Routes.homePageRoute.value, Routes.WSRoute.value, ServerSecrets.fernetKey.value,
                               extraHeads, bodyBase, WebsiteRelated.title.value, False)

print(f"http://127.0.0.1:{ServerSecrets.portToUse.value}{Routes.homePageRoute.value}")
WSGIServer(('0.0.0.0', ServerSecrets.portToUse.value,), baseApp, log=None).serve_forever()
