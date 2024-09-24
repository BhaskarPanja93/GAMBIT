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


# def loginPage(viewerObj: BaseViewer):
#     login = f"""
#
#     <nav class="bg-neutral-300">
#         <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
#             <div class="relative flex items-center justify-between h-16">
#                 <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
#                     <div class="flex-shrink-0 flex items-center">
#                         <a href="#" class="text-white text-2xl">Gambit</a>
#                     </div>
#                     <div class="hidden sm:block sm:ml-6">
#                         <div class="flex space-x-4">
#                             <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
#                             <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
#                             <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Contact</a>
#                         </div>
#                     </div>
#                 </div>
#                 <div class="hidden sm:block sm:ml-6">
#                     <div class="flex space
#                     -x-4">
#                         <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
#                         <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </nav>
#     """
#     viewerObj.queueTurboAction(login, "loginPage", viewerObj.turboApp.methods.update)
# def registerPage(viewerObj: BaseViewer):
#     registration = f"""
#
#     <nav class="bg-neutral-300">
#         <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
#             <div class="relative flex items-center justify-between h-16">
#                 <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
#                     <div class="flex-shrink-0 flex items-center">
#                         <a href="#" class="text-white text-2xl">Study Well</a>
#                     </div>
#                     <div class="hidden sm:block sm:ml-6">
#                         <div class="flex space
#                         -x-4">
#                             <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
#                             <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
#                             <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Contact</a>
#                         </div>
#                     </div>
#                 </div>
#                 <div class="hidden sm:block sm:ml-6">
#                     <div class="flex space
#                     -x-4">
#                         <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
#                         <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </nav>
#     """
#     viewerObj.queueTurboAction(registration, "registerPage", viewerObj.turboApp.methods.update)


def homePage(viewerObj: BaseViewer):
    home = f"""
<div class="px-12 w-full sm:px-12">
    <div class="relative pt-6 pb-16 sm:pb-24">
        <nav class="relative flex items-center justify-between sm:h-10 md:justify-center" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto">
                    <a href="#">
                        <span class="sr-only">Gambit - All in One Education</span>
                        <img class="w-auto h-14 sm:h-18" src="https://www.svgrepo.com/show/448244/pack.svg" loading="lazy" width="202" height="80">
                    </a>
                    <div class="flex items-center -mr-2 md:hidden">
                        <button class="inline-flex items-center justify-center p-2 text-blue-700 bg-yellow-700 rounded-lg hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-50"  type="button" aria-expanded="false">
                        </button>
                    </div>
                </div>
            </div>
            <div class="hidden md:flex md:space-x-10 list-none">
                <p class="text-3xl text-white font-bold">THE ALL IN ONE PLATFORM </p>
            </div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="py-4 inline-flex rounded-full shadow">   
                    <button class="font-custom inline-flex items-center px-14 py-3 text-2xl text-black bg-yellow-300 border border-transparent rounded-3xl cursor-pointer hover:bg-gray-100 font-bold">
                        REGISTER
                    </button>
                </div>
            </div>
        </nav>

        <div id="imageBackground" class=" py-12 relative image-container w-full">
        <!-- Image -->
        <img src="static/images/background-image.jpg" alt="Home screen image" class="rounded-3xl w-full h-5/6 object-cover">
        <button class="absolute top-1/3 left-1/2 transform -translate-x-1/2 bg-blue-700 text-white font-bold text-4xl rounded-full p-12">START LEARNING</button>
        <p class="flex justify-center absolute top-2/3 left-1/2 transform -translate-x-1/2 translate-y-1 text-white font-bold text-7xl w-full">
            All Your Education Needs In One</p>

        </div>
    </div>
</div>

"""

    viewerObj.queueTurboAction(home, "homePage", viewerObj.turboApp.methods.update)


def loginRegisterPage(viewerObj: BaseViewer):
    homePage(viewerObj)

    loginRegister = f"""

        <div class="flex items-center justify-stretch min-h-screen grid grid-cols-2 gap-8 px-6 py-6 place-content-stretch h-64">
            <div id="loginDiv" class="rounded-lg bg-blue-700 flex items-center justify-center h-96">
                <button id="loginButton" class="rounded-lg bg-blue-700 flex items-center justify-center h-96 w-full">
                    <p class="text-white font-bold text-4xl">Login</p>
                </button>

                <div id="loginFormContainer" class="hidden rounded-lg bg-blue-700 flex items-center justify-center h-96">
                    <form onsubmit="return submitLogin(this)">
                        <input type="text" class="py-3 px-5 block w-full border-gray-200 rounded-full text-xl focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none" name="username" placeholder="Username" >
                        <br>
                        <input class="py-3 px-5 block w-full border-gray-200 rounded-full text-xl focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none" type="password" name="password" placeholder="Password" >
                        <br>
                        <button type="submit" class="bg-white text-blue-700 font-bold p-6 rounded">Submit</button>
                    </form>
                </div>
            </div>

            <div id="registerDiv" class="rounded-lg bg-yellow-700 flex items-center justify-center h-96">
                <button id="registerButton" class="rounded-lg bg-yellow-700 flex items-center justify-center h-96 w-full">
                    <p class="text-white font-bold text-4xl">Register</p>
                </button> 


                <div id="registerFormContainer" class="hidden rounded-lg bg-yellow-700 flex items-center justify-center h-96">
                    <form onsubmit="return submitRegister(this)">
                        <input type="text" class="py-3 px-4 px-5 block w-full border-gray-200 rounded-full text-l focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none mb-4" name="username" placeholder="Username" >

                        <input type="text" class="py-3 px-5 block w-full border-gray-200 rounded-full text-l focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none mb-4" name="email" placeholder="Email" >

                        <input class="py-3 px-5 block w-full border-gray-200 rounded-full text-l focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none mb-4" type="password" name="password" placeholder="Password" >


                        <input class="py-3 px-5 block w-full border-gray-200 rounded-full text-l focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none mb-4" type="password" name="confirm_password" placeholder="Confirm Password" >

                        <button type="submit" class="bg-white text-blue-700 font-bold p-6 rounded">Submit</button>
                    </form>
                </div> 
            </div> 
        </div>


    <script>
            document.getElementById('loginButton').addEventListener('click', function() {{
            document.getElementById('loginFormContainer').classList.remove('hidden');
            document.getElementById('loginButton').classList.add('hidden');
        }});   



            document.getElementById('registerButton').addEventListener('click', function() {{
            document.getElementById('registerFormContainer').classList.remove('hidden');
            document.getElementById('registerButton').classList.add('hidden');
        }});    
    </script>

    """

    viewerObj.queueTurboAction(loginRegister, "loginRegisterPage", viewerObj.turboApp.methods.update)

    loginInputForm = f"""



    """

    # viewerObj.queueTurboAction(loginInputForm, "loginRegisterPage", viewerObj.turboApp.methods.update)

    registerInputForm = f"""

    """
    # viewerObj.queueTurboAction(registerInput, "registerDiv", viewerObj.turboApp.methods.update)


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


def quizPage(viewerObj: BaseViewer):
    quiz = f"""
<div class="bg-orange-700 flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">


    <div id="teamDiv" class="rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
        <div>HEALTH POINTS</div>
        <div class="flex justify-center w-full h-12 my-8">
            <div class="flex items-center w-5/6 h-full bg-gray-200 rounded-full dark:bg-gray-700">
                <div class="bg-red-600 text-2xl h-12 font-medium text-blue-100 text-center leading-none rounded-full flex items-center justify-center"
                   style="width: 99%">
                  99% <3
                </div>
            </div>
        </div>

        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="rounded w-36 h-36" src="/docs/images/people/profile-picture-5.jpg" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-2xl h-1/3 p-4 m-4">Player 1</div>
                </div>
            </div>
        </div>        
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="rounded w-36 h-36" src="/docs/images/people/profile-picture-5.jpg" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-2xl h-1/3 p-4 m-4">Player 2</div>
                </div>
            </div>
        </div>
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="rounded w-36 h-36" src="/docs/images/people/profile-picture-5.jpg" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-2xl h-1/3 p-4 m-4">Player 3</div>
                </div>
            </div>
        </div>
    </div>

    <div id="quizDiv" class="rounded-lg bg-blue-700 flex flex-col items-center justify-center w-full h-full">

        <div class="text-white font-bold text-2xl h-1/3 p-4 m-4" id="test">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae risus efficitur quam imperdiet sagittis. Suspendisse rutrum iaculis lectus sit amet maximus. Integer tincidunt in arcu vitae condimentum. Nunc porta ex elit, eget sollicitudin tellus pharetra quis. Ut laoreet, enim maximus dapibus ullamcorper, arcu leo scelerisque quam, a vulputate ligula turpis eu dolor. Proin sem sem, elementum ut nulla nec, fermentum fringilla libero. Maecenas eu facilisis erat, vitae iaculis orci. Donec volutpat enim vitae leo convallis hendrerit. 

        </div>

        <div class="grid grid-cols-2 gap-4 px-12 py-4 place-content-stretch h-1/2 w-5/6"> 
            <button class="rounded-lg bg-yellow-400 flex items-center justify-center h-full w-full">
                <div id="option0" class="text-white font-bold text-2xl">Button 1</div>
            </button>
            <button class="rounded-lg bg-red-700 flex items-center justify-center h-full w-full">
                <div id="option1" class="text-white font-bold text-2xl">Button 2</div>
            </button>
            <button class="rounded-lg bg-orange-400 flex items-center justify-center h-full w-full">
                <div id="option2" class="text-white font-bold text-2xl">Button 3</div>
            </button>
            <button class="rounded-lg bg-blue-200 flex items-center justify-center h-full w-full">
                <div id="option3" class="text-white font-bold text-2xl">Button 4</div>
            </button>
        </div>
    </div>

<div id="opponentDiv" class="rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
    <div>HEALTH POINTS</div>
    <div class="flex justify-center w-full h-12 my-8">
        <div class="flex items-center w-5/6 h-full bg-gray-200 rounded-full dark:bg-gray-700">
            <div class="bg-red-600 text-2xl h-12 font-medium text-blue-100 text-center leading-none rounded-full flex items-center justify-center"
               style="width: 45%">
              45% <3
            </div>
        </div>
    </div>

    <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="rounded w-36 h-36" src="/docs/images/people/profile-picture-5.jpg" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-2xl h-1/3 p-4 m-4">Player 1</div>
                </div>
            </div>
        </div>        
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="rounded w-36 h-36" src="/docs/images/people/profile-picture-5.jpg" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-2xl h-1/3 p-4 m-4">Player 2</div>
                </div>
            </div>
        </div>
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="rounded w-36 h-36" src="/docs/images/people/profile-picture-5.jpg" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-2xl h-1/3 p-4 m-4">Player 3</div>
                </div>
            </div>
        </div>

</div>
</div>
"""

    viewerObj.queueTurboAction(quiz, "quizPage", viewerObj.turboApp.methods.update)


def newVisitorCallback(viewerObj: BaseViewer):
    initial = "<div id=\"quizPage\"></div>"
    viewerObj.queueTurboAction(initial, "mainDiv", viewerObj.turboApp.methods.update)

    # loginRegisterPage(viewerObj)
    quizPage(viewerObj)
    # loginInput(viewerObj)
    # sendRegister(viewerObj)
    # sendLogin(viewerObj)
    # homePage(viewerObj)


def visitorLeftCallback(viewerObj: BaseViewer):
    print("Visitor Left: ", viewerObj.viewerID)


def formSubmitCallback(viewerObj: BaseViewer, form: dict):
    if form is not None:
        purpose = form.pop("PURPOSE")

        if purpose == FormPurposes.register.value:
            print(form)

        elif purpose == FormPurposes.login.value:
            print(form)



extraHeads = f"""<script src="https://cdn.tailwindcss.com"></script>"""
bodyBase = """<body class="bg-slate-700"><div id="mainDiv"><div></body>"""


baseApp, turboApp = createApps(formSubmitCallback, newVisitorCallback, visitorLeftCallback, CoreValues.appName.value,
                               Routes.webHomePage.value, Routes.webWS.value, ServerSecrets.webFernetKey.value,
                               extraHeads, bodyBase, CoreValues.title.value, False)

@baseApp.get(Routes.internalConnection.value)
def _internalConn():

    return ""


print(f"http://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None).serve_forever()
