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




def homePage(viewerObj: BaseViewer):
    home = f"""
    <div class="px-4 mx-auto max-w-7xl sm:px-6">
    <div class="relative pt-6 pb-16 sm:pb-24">
        <nav class="relative flex items-center justify-between sm:h-10 md:justify-center" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div class="flex items-center justify-between w-full md:w-auto">
                    <a href="#"><span class="sr-only">Company Name</span>
                        <img class="w-auto h-8 sm:h-10" src="https://www.svgrepo.com/show/448244/pack.svg" loading="lazy" width="202" height="40">
                    </a>
                    <div class="flex items-center -mr-2 md:hidden">
                        <button class="inline-flex items-center justify-center p-2 text-gray-400 bg-gray-50 rounded-md hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-50"  type="button" aria-expanded="false">
                            <span class="sr-only">Open main menu</span>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
            <div class="hidden md:flex md:space-x-10 list-none">
                <li>
                    <a href="#" class="text-base font-normal text-gray-500 list-none hover:text-gray-900"
                        target="">Pricing</a>
                </li>
                <li>
                    <a href="#" class="text-base font-normal text-gray-500 list-none hover:text-gray-900"
                        target="">Gallary
                    </a>
                </li>
                <li>
                    <a href="#" class="text-base font-normal text-gray-500 list-none hover:text-gray-900"
                        target="_blank">Blog
                    </a>
                </li>
            </div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="inline-flex rounded-full shadow">   
                    <div href="#"
                        class="inline-flex items-center px-14 py-3 text-base text-gray-900 bg-white border border-transparent rounded-full cursor-pointer font-bold text-2xl hover:bg-gray-50 ">
                        GO
                    </div>
                </div>
            </div>
        </nav>
    </div>
</div>
"""

    viewerObj.queueTurboAction(home, "homePage", viewerObj.turboApp.methods.update)
def loginRegisterPage(viewerObj: BaseViewer):
    loginRegister = f"""
    
    
    
    """

    return


def testPage(viewerObj: BaseViewer):
    testingpage = f"""
    <div id="app" class="w-full max-w-xs">
    
    <button type="button" id="viewlogin"class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">View Login</button>    
    <button type="button" id="hideButton"class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" onclick="hideLogin()">Hide</button>    
    <button type="button" id="showButton"class="text-white bg-blue-600 rounded-full font-medium text-sm px-5 py-2.5 me-2 mb-2 hover:bg-blue-800" onclick="showLogin()">Show Login</button>    
    </div>
    
    <div id="loginContainer" class="rounded-lg w-2/3 bg-blue-700 h-128 p-4 m-4 ">
        <div id="loginForm">
            <h2 class="font-bold text-lg mb-4">Login</h2>
            <input class="rounded-lg w-full p-4 my-2" type="text" placeholder="Username">
            <input class="rounded-lg w-full p-4 my-2" type="password" placeholder="Password">
            <div class="flex justify-center">
            <button class="bg-blue-500 rounded-full text-white p-2 w-1/2 mb-4 my-4">Login</button>
            </div>
            <p class="text-center">Don't have an account? <button onclick="showRegister()" class="text-blue-500">Register</button></p>
        </div>
    </div>
    # <script>
    #     function showLogin() {{
    #         document.getElementById('loginForm').style.display = 'block';
    #         document.getElementById('registerForm').style.display = 'none';
    #     }}
    # </script>
    
    <style>
    .fade-in {{
      animation: fadeIn 1s ease-in-out forwards;
    }}
    @keyframes fadeIn {{
      from {{
        opacity: 0;
      }}
      to {{
        opacity: 1;
      }}
    }}
  </style>
  
    <script>
    const showDivBtn = document.getElementById('viewlogin');
    const showLoginBtn = document.getElementById('showButton');
    const animatedDiv = document.getElementById('loginForm');

    showDivBtn.addEventListener('click', () => {{
      animatedDiv.classList.remove('hidden');
      animatedDiv.classList.add('fade-in');
    }});
  </script>
  
  <script>
    function hideLogin() {{
    document.getElementById('loginContainer').style.display = 'none';
    }}
    
    function showLogin() {{
    document.getElementById('loginContainer').style.display = 'block';
    }}
  </script>
    """

    viewerObj.queueTurboAction(testingpage, "testPage", viewerObj.turboApp.methods.update)


def newVisitorCallback(viewerObj: BaseViewer):
    initial = "<div id=\"homePage\"></div>"
    viewerObj.queueTurboAction(initial, "mainDiv", viewerObj.turboApp.methods.update)
    testPage(viewerObj)
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


extraHeads = """
<style>
@font-face { 
    font-family: Gotham; 
    src: url('JUNEBUG.TTF'); 
    } 
    
    </style>
<script src="https://cdn.tailwindcss.com"></script>"""
bodyBase = """<body class="bg-slate-700"><div id="mainDiv"><div></body>"""

baseApp, turboApp = createApps(formSubmitCallback, newVisitorCallback, WebsiteRelated.appName.value,
                               Routes.webHomePage.value, Routes.webWS.value, ServerSecrets.webFernetKey.value,
                               extraHeads, bodyBase, WebsiteRelated.title.value, False)

print(f"http://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None).serve_forever()
