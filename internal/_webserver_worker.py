from gevent import monkey
monkey.patch_all()

from random import choice, randrange, choices
from requests import get
from flask import request
from random import shuffle
from threading import Thread
from time import time, sleep
from randomisedString import Generator as StringGenerator
from dynamicWebsite import *
from Enums import *
from gevent.pywsgi import WSGIServer
from Methods import *
from customisedLogs import Manager as LogManager
from werkzeug.security import check_password_hash, generate_password_hash
from json import loads


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


def renderHomepage(viewerObj: BaseViewer):
    home = f"""
<div class="px-12 w-full sm:px-12">
        <nav class="relative flex items-center justify-between h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto">
                    <a href="#" class="flex items-center space-x-4">
                        <!-- Logo Image -->
                        <img class="w-auto h-14 sm:h-18" src="/better-education-cdn-file?type=image&name=dice.png" loading="lazy" width="202" height="80">
                        <!-- GAMBIT Text -->
                        <p class="text-3xl text-white font-bold">GAMBIT</p>
                    </a>
                </div>
            </div>
        
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="py-4 inline-flex rounded-full shadow">   
                    <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF(FormPurposes.renderAuth.value)}
                        <button type="submit" mt-100 class="font-custom inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 border border-transparent rounded-3xl cursor-pointer hover:font-bold hover:scale-105 hover:transition duration-300 ease-in-out">
                            Join Now
                        </button>
                    </form>
                </div>
            </div>
        </nav>


    <div class="relative pt-6 pb-16 sm:pb-24">

        <div id="imageBackground" class="py-12 relative image-container w-full">
            <!-- Image -->
            <img src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=background-image.jpg" style="opacity: 0.7;" alt="Home screen image" class="rounded-3xl w-full h-5/6 object-cover">
            
            <!-- Start Learning Button -->
            <form onsubmit="return submit_ws(this)">
                {viewerObj.addCSRF(FormPurposes.renderQuizLobby.value)}
                <button type="submit" class="absolute top-1/3 left-1/2 transform -translate-x-1/2 bg-white font-bold text-4xl rounded-full p-12 hover:scale-105 hover:transition duration-300 ease-in-out" style="color: #23003d;">
                    START LEARNING
                </button>
            </form>

            <!-- Headline Text -->
            <p class="flex justify-center absolute top-2/3 left-1/2 transform -translate-x-1/2 translate-y-1 text-white font-bold text-7xl w-full">
                All Your Education Needs In One
            </p>
        </div>
    </div>
</div>



"""

    viewerObj.queueTurboAction(home, "fullPage", viewerObj.turboApp.methods.update)


def renderAuthPage(viewerObj: BaseViewer):
    loginRegister = f"""
<nav class="my-6 relative flex items-center justify-between sm:h-10 md:justify-center" aria-label="Global">
    <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
        <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto">
            <a href="#">
                <span class="sr-only">Gambit - All in One Education</span>
                <img class="w-auto h-14 sm:h-18" src="https://www.svgrepo.com/show/448244/pack.svg" loading="lazy"
                     width="202" height="80">
            </a>
            <div class="flex items-center -mr-2 md:hidden">
                <button class="inline-flex items-center justify-center p-2 text-blue-700 bg-yellow-700 rounded-lg hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-50"
                        type="button" aria-expanded="false">
                </button>
            </div>
        </div>
    </div>
    <div class="hidden md:flex md:space-x-10 list-none">
        <p class="text-3xl text-white font-bold">THE ALL IN ONE EDUCATION PLATFORM </p>
    </div>
    <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
        <div class="py-4 inline-flex rounded-full">
        </div>
    </div>
</nav>


<div class="flex items-center justify-center min-h-screen">
    <div class="flex items-center bg-transparent rounded-lg p-8 justify-stretch h-3/4 min-h-0 grid grid-cols-2 gap-8 place-content-stretch mx-6 w-full">
        <!-- Login Section -->
        <div id="loginDiv" class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-96 shadow-2lg hover:scale-105 hover:transition duration-300 ease-in-out">
            <button id="loginButton" class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-96 w-full shadow-2xl">
                <div class="w-full text-white font-bold text-4xl">Login</div>
            </button>
            <div id="loginFormContainer" class="hidden w-full rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-96 shadow-2xl">
                <form onsubmit="return submit_ws(this)">
                    {viewerObj.addCSRF(FormPurposes.login.value)}
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="username" placeholder="Username">
                    <input autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           type="password" name="password" placeholder="Password">
                    <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit</button>
                </form>
            </div>
        </div>

        <!-- Register Section -->
        <div id="registerDiv" sty class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-96 shadow-lg hover:scale-105 hover:transition duration-300 ease-in-out">
            <button id="registerButton" class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-96 w-full shadow-2xl">
                <div class="w-full text-white font-bold text-4xl">Register</div>
            </button>

            
                <div id="registerFormContainer"
                     class="hidden w-full rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-96 shadow-lg">
                    <form class="w-full px-6" onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF(FormPurposes.register.value)}
                        
                        <input type="text" autocomplete="off"
                               class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               name="name" placeholder="Name">
                               
                        <input type="text" autocomplete="off"
                               class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               name="age" placeholder="Age">
                               

                        <input type="text" autocomplete="off"
                               class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               name="email" placeholder="Email">

                        <input type="password" autocomplete="off"
                               class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               name="password" placeholder="Password">

                        <input type="password" autocomplete="off"
                               class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               name="confirm_password" placeholder="Confirm Password">
                               
                        <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit
                        </button>
                    </form>
                </div>
            
        </div>

        <div id="loginWarning"
             class="text-2xl flex col-span-2 items-center justify-center text-white rounded-lg px-4 py-2 text-center font-semibold w-full"></div>
        <div id="registrationWarning"
             class="text-2xl flex col-span-2 items-center justify-center text-white rounded-lg px-4 py-2 text-center font-semibold w-full"></div>
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
    viewerObj.queueTurboAction(loginRegister, "fullPage", viewerObj.turboApp.methods.update)
    sendRegisterForm(viewerObj)
    sendLoginForm(viewerObj)


def renderQuizGamePage(viewerObj: BaseViewer):
    quiz = f"""
<div class="bg-[#23003d] flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">

    <div id="teamADiv" class="rounded-lg bg-[#490080] flex flex-col h-full w-1/3">
        <div class="flex flex-col items-center">
            <div class="text-white mb-1">HEALTH POINTS</div>
            <div class="relative size-40 flex items-center justify-center">

                <div id="selfTeamHealthBar"></div>

                <!-- Value Text -->
                <div class="absolute top-1/2 start-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
                    <span class="text-4xl font-bold text-green-600 dark:text-green-500">
                        <div id="selfTeamHealthText"></div>
                        </span>
                    <span class="text-green-600 dark:text-green-500 block">Score</span>
                </div>
            </div>
        </div>

        <div id="selfTeam_create"></div>

    </div>

    <div id="quizDiv" class="rounded-lg bg-[#490080] flex flex-col items-center justify-center w-full h-full">
        <div class="rounded-lg px-2 mx-6 bg-[#eacfff] text-green font-bold text-2xl p-4">
            <div class="bg-[#eacfff] font-bold text-2xl h-1/3 p-4 m-4" style="color:#23003d" id="questionText"> </div>
        </div>


        <div class="text-white font-bold text-2xl p-4">Select an option</div>

        <div id="options" class="grid grid-cols-2 gap-4 px-12 py-4 place-content-stretch h-1/2 w-5/6"></div>
        </div>

        <div id="teamBDiv" class="rounded-lg bg-[#490080] flex flex-col h-full w-1/3">
            <div class="flex flex-col items-center">
                <div class="text-white mb-1" >HEALTH POINTS</div>
                <div class="relative size-40 flex items-center justify-center">

                    <div id="otherTeamHealthBar">
                        <svg class="rotate-[135deg] size-full" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
                            <!-- Background Circle (Gauge) -->
                            <circle cx="18" cy="18" r="16" fill="none"
                                    class="stroke-current text-green-200 dark:text-neutral-700"
                                    stroke-width="1" stroke-dasharray="75 100" stroke-linecap="round"></circle>

                            <!-- Gauge Progress -->
                            <circle cx="18" cy="18" r="16" fill="none"
                                    class="stroke-current text-green-500 dark:text-green-500"
                                    stroke-width="2" stroke-dasharray="15 100" stroke-linecap="round"></circle>
                        </svg>
                    </div>

                    <!-- Value Text -->
                    <div class="absolute top-1/2 start-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
                    <span class="text-4xl font-bold text-green-600 dark:text-green-500">
                        <div id="otherTeamHealthText"></div>
                        </span>
                    <span class="text-green-600 dark:text-green-500 block">Score</span>
                </div>
            </div>
        </div>

        <div id="otherTeam_create"></div>
    </div>
</div>
"""


    viewerObj.queueTurboAction(quiz, "fullPage", viewerObj.turboApp.methods.update)


# Ending Quiz Page
def renderQuizEndPage(viewerObj: BaseViewer):
    quizEnd = f"""
    <div class="bg-[#23003d] flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">
    <div id="leaderboardDiv" class="rounded-lg bg-[#490080] flex flex-col h-full w-1/3">
        <div class="flex flex-col items-center">
            <div class="my-4 text-bold text-white text-3xl font-bold">Leaderboard</div>
        </div>

        <!-- Leaderboard Entries -->
        <div id="quizLeaderboard"></div>
    </div>

    <div id="postQuiz" class="rounded-lg bg-[#490080] flex flex-col items-center justify-center w-full h-full">
        <div class="p-8 rounded-lg mx-6 bg-[#490080] font-bold text-2xl h-full w-full">
            <div id="resultTextDiv" class="flex justify-center items-center text-white font-bold text-2xl h-1/3"></div>
        </div>
    </div>

    <div class="rounded-lg bg-[#490080] flex flex-col h-full w-1/3">
        <div class="flex flex-col items-center">
            <div style="color:white">QUESTIONS LIST</div>
        </div>
        <div id="postQuizQuestionList" class="flex flex-col items-center mt-4"></div>
    </div>
</div>
"""
    viewerObj.queueTurboAction(quizEnd, "fullPage", viewerObj.turboApp.methods.update)


def renderQuizLobbyPage(viewerObj: BaseViewer):
    quizLobby = f"""

    <div class="bg-[#23003d] flex h-full w-full gap-8 px-6 py-6">

        <div class="w-full">
            <h1 class="flex justify-center text-3xl font-bold text-white">Lobby</h1>

          <div id="quizLobbyDiv" class="p-8 rounded-lg grid grid-cols-3 w-full h-full gap-4"> </div>
        </div>
        <div id="quizFriendListDiv" class="p-6 flex items-center rounded-lg bg-[#490080] flex flex-col h-full w-1/3">
            <!-- Queue Up Button -->
            <form class="w-full" onsubmit="return submit_ws(this)">
                {viewerObj.addCSRF(FormPurposes.startQuiz.value)}
                <button type="submit" class="w-full p-4 rounded-full flex justify-center bg-gradient-to-r from-purple-500 to-violet-700 hover:scale-105 hover:transition duration-300 ease-in-out mb-4">
                    <div id="queueTimer" class="w-full text-white font-bold">QUEUE UP</div>
                </button>
            </form>

            <!-- Friend List Container -->
            <div class="rounded-lg h-full w-full bg-[#eacfff] m-8 p-4">
                <!-- Friend List Title -->
                <div class="text-dark font-bold flex justify-center mb-4">FRIEND LIST</div>

                <!-- Individual Friend Entries -->
                <div class="flex flex-col space-y-2">
                    <!-- Friend 1-->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 1</span>
                        <button class="bg-gradient-to-r from-purple-500 to-violet-700 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>     
                </div>
            </div>
        </div>

    </div>
    """
    viewerObj.queueTurboAction(quizLobby, "fullPage", viewerObj.turboApp.methods.update)


def renderQuizMatchFoundPage(viewerObj: BaseViewer):
    matchFound = f"""
        <div class="bg-[#23003d] flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">
            <div id="quizDiv" class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex flex-col items-center justify-center w-full h-full">
                <h1 class="text-7xl text-white font-bold">MATCH FOUND</h1>
        </div>
        </div>

        """
    viewerObj.queueTurboAction(matchFound, "fullPage", viewerObj.turboApp.methods.update)



def sendRegisterForm(viewerObj:BaseViewer):
    form = f"""<form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF(FormPurposes.register.value)}
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 mb-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="name" placeholder="Name">
                           
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 mb-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="age" placeholder="Age">
                           
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 mb-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="username" placeholder="Username">
                    
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 mb-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="email" placeholder="Email">
                    
                    <input type="password" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 mb-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="password" placeholder="Password">
                    
                    <input type="password" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 mb-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="confirm_password" placeholder="Confirm Password">
                           <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit
                        </button>
                    </form>"""
    viewerObj.queueTurboAction(form, "registerFormContainer", viewerObj.turboApp.methods.update)


def sendLoginForm(viewerObj:BaseViewer):
    form = f"""<form onsubmit="return submit_ws(this)">
                    {viewerObj.addCSRF(FormPurposes.login.value)}
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="username" placeholder="Username">
                    <input autocomplete="off" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           type="password" name="password" placeholder="Password">
                    <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit</button>
                </form>"""
    viewerObj.queueTurboAction(form, "loginFormContainer", viewerObj.turboApp.methods.update)


class Player:
    def __init__(self, viewer: BaseViewer|None=None):
        self.userName = "BOT_"+StringGenerator().AlphaNumeric(4,4)
        self.userID = "BOT_"+StringGenerator().AlphaNumeric(10,10)
        self.userName = liveCacheManager.getUserName(liveCacheManager.ByViewerID, viewer.viewerID) if viewer else self.userName
        self.userID = liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewer.viewerID) if viewer else self.userID
        self.viewerObj = viewer
        self.team:Team|None = None
        self.isHuman:bool = False if not viewer else True
        self.correctness:float = 0.6
        self.score = 0


class Team:
    def __init__(self, teamID:str):
        self.teamID = teamID
        self.players:dict[str, Player] = {}
        self.score = 0
        self.health = 0

    def playerJoin(self, player:Player):
        if player.userID not in self.players:
            self.players[player.userID] = player
            player.team = self
    def playerLeft(self, player: Player):
        if player.userID in self.players:
            del self.players[player.userID]
            player.team = None



class Party:
    def __init__(self, teamCount:int, playerCount:int):
        self.partyID:str|None = None
        self.userIDToPlayer: dict[str, Player] = {}
        self.teams: list[Team] = []
        self.timerInitialised = False
        self.gameObj:Quiz|None = None
        while not self.partyID or self.partyID in liveCacheManager.activeParties: self.partyID = StringGenerator().AlphaNumeric(5, 30)
        liveCacheManager.partyCreated(self)
        for _ in range(teamCount): self.teams.append(Team(f"{self.partyID}{_}"))
        self.maxPlayers = playerCount


    def startTimer(self):
        if not self.timerInitialised:
            partyTimerStartedAt = time()
            self.timerInitialised = True
            while time() - partyTimerStartedAt < 4 and sum([len(team.players) for team in self.teams]) > 1:
                for player in self.userIDToPlayer.values():
                    player.viewerObj.queueTurboAction(str(4 - int(time() - partyTimerStartedAt)), "queueTimer", player.viewerObj.turboApp.methods.update)
                sleep(1)
        if sum([len(team.players) for team in self.teams]) > 1:
            self.partyComplete()
        else:
            self.timerInitialised = False
            for player in self.userIDToPlayer.values():
                player.viewerObj.queueTurboAction("Waiting...", "queueTimer", player.viewerObj.turboApp.methods.update)


    def joinTeam(self, viewer: BaseViewer|None=None):
        player = Player(viewer)
        if player.isHuman: liveCacheManager.userIDToPartyID[player.userID] = self.partyID
        self.userIDToPlayer[player.userID] = player
        shuffle(self.teams)
        if self.gameObj is None and sum([len(team.players) for team in self.teams]) < 6:
            smallestTeamLength = len(self.teams[0].players)
            for team in self.teams:
                if len(team.players)<smallestTeamLength:
                    team.playerJoin(player)
                    break
            else:
                self.teams[0].playerJoin(player)
            if player.isHuman:
                if sum([len(team.players) for team in self.teams]) == 6: self.partyComplete()
                else: Thread(target=self.startTimer).start()
            return True
        return False


    def leaveTeam(self, viewer: BaseViewer, team:Team|None=None):
        player = self.userIDToPlayer.get(liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewer.viewerID), Player(viewer))
        if player.userID in liveCacheManager.userIDToPartyID: del liveCacheManager.userIDToPartyID[player.userID]
        if team is None:
            for team in self.teams:
                team.playerLeft(player)
        else:
            team.playerLeft(player)
        if sum([len(team.players) for team in self.teams]) <= 0:
            self.destroyParty()


    def partyComplete(self):
        for _ in range(self.maxPlayers - sum([len(team.players) for team in self.teams])): self.joinTeam()
        self.gameObj = Quiz(self)
        self.gameObj.startQuiz()


    def gameComplete(self):
        self.gameObj = None


    def destroyParty(self):
        liveCacheManager.partyDeleted(self)



class Question:
    def __init__(self):
        self.questionID = ""
        self.questionStatement = ""
        self.teamOptions: dict[str, list[str]] = {}
        self.correctAnswers = []
        self.optionsPressed:dict[Player, int] = {}


    def setValues(self, party:Party, questionID, question: str, options: dict[str, list[str]]):
        for team in party.teams: self.teamOptions[team.teamID] = []
        self.questionID = questionID
        self.questionStatement = question
        self.correctAnswers = options["Correct"]
        for teamID in self.teamOptions:
            shuffle(options["InCorrect"])
            for _ in range(3):
                while True:
                    option = options["InCorrect"][_]
                    if option not in self.teamOptions[teamID]:
                        self.teamOptions[teamID].append(option)
                        break
            self.teamOptions[teamID].append(options["Correct"][0])
            shuffle(self.teamOptions[teamID])


class Quiz:
    def __init__(self, party:Party):
        self.party = party

        self.startTime = time()
        self.matchID = StringGenerator().AlphaNumeric(50, 50)
        self.endTime = 0.0

        self.questions: list[Question] = []
        self.questionIndex = -1

    def renderPlayers(self):
        for playerToRenderFor in self.party.userIDToPlayer.values():
            if playerToRenderFor.isHuman:
                for playerToRender in self.party.userIDToPlayer.values():
                    playerDiv = f"""
                            <div class="rounded-lg bg-[#eacfff] mx-4 my-2 flex justify-between items-center">
                                <img class="mx-4 rounded-full border-4 border-white w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
                                <div class="flex items-center gap-4">
                                    <div class="font-medium dark:text-white">
                                        <div class="text-black text-bold text-xl m-4">Name: {playerToRender.userName}</div>
                                    </div>
                                </div>
                            </div>
                            """
                    if playerToRenderFor.team == playerToRender.team:
                        playerToRenderFor.viewerObj.queueTurboAction(playerDiv, "selfTeam", playerToRenderFor.viewerObj.turboApp.methods.newDiv)
                    else:
                        playerToRenderFor.viewerObj.queueTurboAction(playerDiv, "otherTeam", playerToRenderFor.viewerObj.turboApp.methods.newDiv)

    def initQuestions(self):
        for questionData in SQLconn.execute("SELECT * from questions where QuizEligible=1 ORDER BY RAND() LIMIT 30"):
            question = Question()
            question.setValues(self.party, questionData["QuestionID"], questionData["Text"], loads(questionData["Options"]))
            self.questions.append(question)
        self.questionIndex = -1

    def nextQuestion(self):
        if self.endTime != 0: return
        self.questionIndex += 1
        currentQuestion = self.questions[self.questionIndex]
        for player in self.party.userIDToPlayer.values():
            if not player.isHuman: continue
            player.viewerObj.queueTurboAction(currentQuestion.questionStatement, "questionText", player.viewerObj.turboApp.methods.update.value)
            options = ""
            for optionIndex in range(4):
                options+= f"""
                <form onsubmit="return submit_ws(this)">
                {player.viewerObj.addCSRF(FormPurposes.quizOption.value)}
                <input type="hidden" name="party" value="{self.party.partyID}">
                <input type="hidden" name="option" value="{optionIndex}">
                <button class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-full w-full hover: font-bold hover:scale-105 hover:transition duration-300 ease-in-out ">
                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[player.team.teamID][optionIndex]}</div>
                </button>
            </form>"""
            player.viewerObj.queueTurboAction(options, "options", player.viewerObj.turboApp.methods.update.value)
        self.generateBotInputs()

    def generateBotInputs(self):
        currentQuestion = self.questions[self.questionIndex]
        for player in self.party.userIDToPlayer.values():
            if not player.isHuman:
                willAnswerCorrect = choices([True, False], [player.correctness, 1-player.correctness])[0]
                option=0
                for answer in currentQuestion.correctAnswers:
                    option = currentQuestion.teamOptions[player.team.teamID].index(answer)
                    if option!=-1: break
                if willAnswerCorrect:
                    self.receiveUserInput(False, player, option)
                else:
                    incorrectOptions = list(range(len(currentQuestion.teamOptions[player.team.teamID])))
                    incorrectOptions.remove(option)
                    self.receiveUserInput(False, player, choice(incorrectOptions))

    def receiveUserInput(self, isHuman: bool, viewer: BaseViewer|Player, optionIndex):
        if isHuman:
            userID = liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewer.viewerID)
            player = self.party.userIDToPlayer.get(userID)
            if not player: return
        else:
            player = viewer
        optionIndex = int(optionIndex)
        currentQuestion = self.questions[self.questionIndex]
        if len(currentQuestion.teamOptions[player.team.teamID]) > optionIndex >= 0 and player not in currentQuestion.optionsPressed:
            currentQuestion.optionsPressed[player] = optionIndex
            if currentQuestion.teamOptions[player.team.teamID][optionIndex] in currentQuestion.correctAnswers: player.score += 10
            else: player.score -= 5
            if isHuman:
                options = f"""<button class="col-span-2 rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-full w-full">
                                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[player.team.teamID][optionIndex]}</div>
                                </button>"""
                player.viewerObj.queueTurboAction(options, "options", player.viewerObj.turboApp.methods.update.value)
            if len(currentQuestion.optionsPressed) == len(self.party.userIDToPlayer):
                self.updateTeamHealth(player.team, -5)
                sleep(1)
                self.endCurrentQuestion()

    def sendPostQuizQuestion(self, viewer: BaseViewer, questionIndex):
        userID = liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewer.viewerID)
        if userID not in self.party.userIDToPlayer: return
        questionIndex = int(questionIndex)
        postQuestion = f"""<div class="rounded-lg px-2 mx-6 bg-[#eacfff] text-green font-bold text-2xl p-4">
                <div class="text-black font-bold text-2xl h-1/3 p-4 m-4">{self.questions[questionIndex].questionStatement}{self.questions[questionIndex].correctAnswers[0]}</div>
            </div>"""
        viewer.queueTurboAction(postQuestion, "postQuiz", viewer.turboApp.methods.update)
        self.sendPostQuizQuestionList(viewer)

    def sendPostQuizQuestionList(self, viewer:BaseViewer):
        questionList = """<ul class="grid grid-cols-1 gap-2 w-full h-full p-4">"""
        for questionIndex in range(0, self.questionIndex + 1):
            questionList += f"""
                                <li>
                                    <form onsubmit="return submit_ws(this)">
                                        {viewer.addCSRF(FormPurposes.postQuizQuestion.value)}
                                        <input type="hidden" name="party" value="{self.party.partyID}">
                                        <input type="hidden" name="question" value="{questionIndex}">
                                        <button class="rounded-lg hover:scale-105 hover:text-white hover:transition duration-300 ease-in-out bg-gradient-to-r from-purple-500 to-violet-700 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">{questionIndex+1}</button>
                                    </form>
                                </li>
                                """
        questionList += "</ul>"
        viewer.queueTurboAction(questionList, "postQuizQuestionList", viewer.turboApp.methods.update)

    def endCurrentQuestion(self):
        points = {}
        currentQuestion = self.questions[self.questionIndex]
        for player in currentQuestion.optionsPressed:
            if player.team.teamID not in points: points[player.team.teamID] = 0
            if currentQuestion.teamOptions[player.team.teamID][currentQuestion.optionsPressed[player]] in currentQuestion.correctAnswers: points[player.team.teamID] += 1
            else: points[player.team.teamID] -= 1
        for team in self.party.teams:
            if team.teamID not in points:
                self.updateTeamHealth(team, -3)
                points[team.teamID] = 0
            elif points[team.teamID] <= 0:
                self.updateTeamHealth(team, -10)
                points[team.teamID] = 0
        teamA = self.party.teams[0]
        teamB = self.party.teams[1]
        if points[teamA.teamID]<points[teamB.teamID]: self.updateTeamHealth(teamA, 10 * (1 + self.questionIndex) * (points[teamA.teamID] - points[teamB.teamID]))
        self.nextQuestion()

    def updateTeamHealth(self, teamChanged: Team, offset):
        teamChanged.health += offset
        if teamChanged.health < 0:
            teamChanged.health = 0
            print(teamChanged.health)
        for player in self.party.userIDToPlayer.values():
            if not player.isHuman: continue
            bar = f"""<svg class="rotate-[135deg] size-full" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="18" cy="18" r="16" fill="none"
                                class="stroke-current text-green-200 dark:text-neutral-700"
                                stroke-width="1" stroke-dasharray="75 100" stroke-linecap="round"></circle>
                        <circle cx="18" cy="18" r="16" fill="none"
                                class="stroke-current text-green-500 dark:text-green-500"
                                stroke-width="2" stroke-dasharray="{75*teamChanged.health/100} 100" stroke-linecap="round"></circle>
                    </svg>"""
            if player.team == teamChanged:
                player.viewerObj.queueTurboAction(bar, f"selfTeamHealthBar", player.viewerObj.turboApp.methods.update.value)
                player.viewerObj.queueTurboAction(str(teamChanged.health), f"selfTeamHealthText", player.viewerObj.turboApp.methods.update.value)
            else:
                player.viewerObj.queueTurboAction(bar, f"otherTeamHealthBar", player.viewerObj.turboApp.methods.update.value)
                player.viewerObj.queueTurboAction(str(teamChanged.health), f"otherTeamHealthText", player.viewerObj.turboApp.methods.update.value)

        if teamChanged.health == 0:
            self.endTime = time()
            _scoreRank:list[Player] = []
            for player in self.party.userIDToPlayer.values():
                if player.isHuman: renderQuizEndPage(player.viewerObj)
                for alreadyAddedIndex in range(len(_scoreRank)):
                    if player.score > _scoreRank[alreadyAddedIndex].score:
                        _scoreRank.insert(alreadyAddedIndex, player)
                        break
                else:
                    _scoreRank.append(player)

            leaderboardDiv = ""
            rank = 0
            for player in _scoreRank:
                rank += 1
                leaderboardDiv += f"""<div class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 mx-6 my-6 flex justify-between items-center h-20 p-2 w-5/6">
                            <div class="font-medium text-bold text-3xl text-white">{rank}</div>
                            <div class="w-full p-4 flex items-center justify-start"> <!-- Updated ID and alignment -->
                                <img class="mr-4 rounded-full w-16 h-16" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
                                <div class="rounded-lg bg-red-white mr-8 font-medium text-[#23003d]">
                                    <div class="px-2 text-white text-bold text-xl">{player.userName}</div>
                                    <div class="px-2 text-white text-bold text-xl">Points: {player.score}</div>
                                </div>
                            </div>
                    </div>"""
            for player in self.party.userIDToPlayer.values():
                if player.isHuman:
                    self.sendPostQuizQuestionList(player.viewerObj)
                    if player.team == teamChanged:
                        player.viewerObj.queueTurboAction("DEFEAT", "resultTextDiv", player.viewerObj.turboApp.methods.update)
                    else:
                        player.viewerObj.queueTurboAction("VICTORY", "resultTextDiv", player.viewerObj.turboApp.methods.update)
                    player.viewerObj.queueTurboAction(leaderboardDiv, "quizLeaderboard", player.viewerObj.turboApp.methods.update)

    def startQuiz(self):
        for player in self.party.userIDToPlayer.values():
            if player.isHuman: renderQuizMatchFoundPage(player.viewerObj)
        started = time()
        self.initQuestions()
        sleep(3-(time()-started))
        for player in self.party.userIDToPlayer.values():
            if player.isHuman: renderQuizGamePage(player.viewerObj)
        for team in self.party.teams:
            team.health = 100
            self.updateTeamHealth(team, 0)
        self.renderPlayers()
        self.nextQuestion()

    def saveToDB(self):
        pass


class UserCache:
    def __init__(self):
        self._dummyViewer = {"USERNAME": "", "PARTY": None, "VIEWERS": []}

        self.activeParties: dict[str, Party] = {}
        self.activeUserIDs = {"USERID1": self._dummyViewer}
        self.userIDToPartyID = {}
        self.viewerIDToUserID = {}
        self.usernameToUserID = {}

        self.ByUserID = "UID"
        self.ByViewerID = "VID"
        self.ByUserName = "UN"
        self.ByCookie = "C"

    def getUserName(self, By, value: str):
        if not value: return
        if By == self.ByUserID:
            if value in self.activeUserIDs: return self.activeUserIDs[value]["USERNAME"]
            received = SQLconn.execute(f"SELECT UserName from user_auth where UserID=\"{value}\" limit 1")
            if received:
                received = received[0]
                return received.get("UserName")
        elif By == self.ByViewerID:
            if value in self.viewerIDToUserID:
                userID = self.viewerIDToUserID[value]
                return self.getUserName(self.ByUserID, userID)
            received = SQLconn.execute(f"SELECT UserID from user_devices where ViewerID=\"{value}\" limit 1")
            if received:
                received = received[0]
                return self.getUserName(self.ByUserID, received.get("UserID").decode())

    def getUserID(self, By, value):
        if not value: return
        if By == self.ByUserName:
            if value in self.usernameToUserID:
                return self.usernameToUserID[value]
            received = SQLconn.execute(f"SELECT UserID from user_auth where UserName=\"{value}\" limit 1")
            if received:
                received = received[0]
                return received.get("UserID").decode()
        elif By == self.ByViewerID:
            if value in self.viewerIDToUserID:
                return self.viewerIDToUserID[value]
            received = SQLconn.execute(f"SELECT UserID from user_devices where ViewerID=\"{value}\" limit 1")
            if received:
                received = received[0]
                return received.get("UserID").decode()

    def getParty(self, By, value):
        pass

    def loginCall(self, viewer: BaseViewer, userID):
        #self.logoutCall(viewer, True)
        username = self.getUserName(self.ByUserID, userID)
        if userID not in self.activeUserIDs:
            self.activeUserIDs[userID] = self._dummyViewer
            self.activeUserIDs[userID]["USERNAME"] = username
        self.viewerIDToUserID[viewer.viewerID] = userID
        self.usernameToUserID[username] = userID
        if viewer not in self.activeUserIDs[userID]["VIEWERS"]: self.activeUserIDs[userID]["VIEWERS"].append(viewer)
        received = SQLconn.execute(f"SELECT UserID, RemoteAddr, UserAgent, HostURL from user_devices where ViewerID=\"{viewer.viewerID}\"")
        addEntry = False
        if received:
            received = received[0]
            if received["UserID"].decode() != userID or received["RemoteAddr"] != viewer.cookie.remoteAddress or received["UserAgent"] != viewer.cookie.UA or received["HostURL"] != viewer.cookie.hostURL:
                SQLconn.execute(f"DELETE from user_devices WHERE ViewerID=\"{viewer.viewerID}\"")
                addEntry = True
        else: addEntry = True
        if addEntry:
            SQLconn.execute(f"INSERT INTO user_devices values (\"{viewer.viewerID}\", \"{userID}\", \"{viewer.cookie.remoteAddress}\", \"{viewer.cookie.UA}\", \"{viewer.cookie.hostURL}\")")

    def logoutCall(self, viewer: BaseViewer, logout: bool = False):
        userID = self.getUserID(self.ByViewerID, viewer.viewerID)
        username = self.getUserName(self.ByViewerID, viewer.viewerID)
        if userID is not None and userID in self.userIDToPartyID:
            party: Party = self.activeParties.get(self.userIDToPartyID[userID])
            if party: party.leaveTeam(viewer)
        if userID is not None and userID in self.activeUserIDs and viewer in self.activeUserIDs[userID]["VIEWERS"]:
            self.activeUserIDs[userID]["VIEWERS"].remove(viewer)
            if len(self.activeUserIDs[userID]["VIEWERS"]) == 0: del self.activeUserIDs[userID]
        if viewer.viewerID in self.viewerIDToUserID: del self.viewerIDToUserID[viewer.viewerID]
        if username in self.usernameToUserID: del self.usernameToUserID[username]
        if logout: SQLconn.execute(f"DELETE from user_devices WHERE ViewerID=\"{viewer.viewerID}\"")

    @staticmethod
    def getKnownLoggedInUserID(viewer: BaseViewer):
        remoteAddr = viewer.cookie.remoteAddress
        userAgent = viewer.cookie.UA
        hostURL = viewer.cookie.hostURL
        received = SQLconn.execute(f"SELECT UserID, RemoteAddr, UserAgent, HostURL from user_devices where ViewerID=\"{viewer.viewerID}\"")
        if received:
            received = received[0]
            if remoteAddr == received["RemoteAddr"] and userAgent == received["UserAgent"] and hostURL == received["HostURL"]:
                return received["UserID"].decode()

    def partyCreated(self, party: Party):
        self.activeParties[party.partyID] = party

    def partyDeleted(self, party: Party):
        if party.partyID in self.activeParties: del self.activeParties[party.partyID]


def registerUser(viewerObj:BaseViewer, form:dict):
    username = form.get("username", "")
    email = form.get("email", "")
    password = form.get("password", "")
    confirm_password = form.get("confirm_password", "")
    name = form.get("name", "")
    age = form.get("age", 0)
    try: age=int(age)
    except:
        viewerObj.queueTurboAction("Invalid Age", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    if not username:
        viewerObj.queueTurboAction("Invalid Username", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    elif SQLconn.execute(f"SELECT UserName from user_auth where UserName=\"{username}\" limit 1"):
        viewerObj.queueTurboAction("Username Taken", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    elif email.count("@")!=1 or email.count(".")!=1:
        viewerObj.queueTurboAction("Email not valid", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    elif password == "":
        viewerObj.queueTurboAction("Passwords Not Valid", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    elif password!=confirm_password:
        viewerObj.queueTurboAction("Passwords Dont match", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    else:
        while True:
            userID = StringGenerator().AlphaNumeric(50, 50)
            if not SQLconn.execute(f"SELECT UserName from user_auth where UserID=\"{userID}\" limit 1"):
                SQLconn.execute(f"INSERT INTO user_info values (\"{userID}\", now(), \"{name}\", {age})")
                SQLconn.execute(f"INSERT INTO user_auth values (\"{userID}\", \"{username}\", \"{generate_password_hash(password)}\")")
                liveCacheManager.loginCall(viewerObj, userID)
                renderHomepage(viewerObj)
                break

def loginUser(viewerObj:BaseViewer, form:dict):
    username = form.get("username", "")
    password = form.get("password", "")
    received = SQLconn.execute(f"SELECT UserID, PWHash from user_auth where UserName=\"{username}\" limit 1")
    if not received:
        viewerObj.queueTurboAction("Username Dont Match", "loginWarning", viewerObj.turboApp.methods.update.value)
        sendLoginForm(viewerObj)
    else:
        received = received[0]
        if not check_password_hash(received["PWHash"].decode(), password):
            viewerObj.queueTurboAction("Password Dont Match", "loginWarning", viewerObj.turboApp.methods.update.value)
            sendLoginForm(viewerObj)
        else:
            liveCacheManager.loginCall(viewerObj, received["UserID"].decode())
            renderHomepage(viewerObj)


def formSubmitCallback(viewerObj: BaseViewer, form: dict):
    if form is not None:
        purpose = form.pop("PURPOSE")
        print(liveCacheManager.getUserName(liveCacheManager.ByViewerID, viewerObj.viewerID), purpose, form)

        if purpose == FormPurposes.register.value:
            registerUser(viewerObj, form)

        elif purpose == FormPurposes.login.value:
            loginUser(viewerObj, form)

        elif purpose == FormPurposes.startQuiz.value:
            for party in liveCacheManager.activeParties.values():
                if party.joinTeam(viewerObj): return
            newParty = Party(2, 6)
            newParty.joinTeam(viewerObj)

        elif purpose == FormPurposes.quizOption.value:
            partyID = form.pop("party", "")
            party = liveCacheManager.activeParties.get(partyID, None)
            if party: party.gameObj.receiveUserInput(True, viewerObj, form["option"])


        elif purpose == FormPurposes.renderAuth.value:
            liveCacheManager.logoutCall(viewerObj, True)
            renderAuthPage(viewerObj)

        elif purpose == FormPurposes.renderQuizLobby.value:
            renderQuizLobbyPage(viewerObj)
            players = f"""
            <div class="bg-[#490080] h-full rounded-lg flex flex-col justify-between items-center py-6">
                <img class="rounded-full w-48 h-48 mb-4" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=botpic.jpg" alt="Extra large avatar">
                <div class="text-white text-xl font-bold text-center">Bot</div> <!-- Increased size and centered -->
                <div class="text-white text-lg text-center">Iron 1</div> <!-- Increased size and centered -->
                <div class="text-white text-lg text-center">Level 1</div> <!-- Increased size and centered -->
            </div>

            <div class="bg-[#490080] h-full rounded-lg flex flex-col justify-between items-center py-6">
                <img class="rounded-full w-48 h-48 mb-4" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
                <div class="text-white text-lg font-semibold">{liveCacheManager.getUserName(liveCacheManager.ByViewerID, viewerObj.viewerID)}</div>
                <div class="text-white text-md">{choice(["Iron", "Bronze", "Silver"])}{randrange(1,4)}</div>
                <div class="text-white text-md">Level {randrange(1,5)}</div>
            </div>
            <div class="bg-[#490080] h-full rounded-lg flex flex-col justify-between items-center py-6">
                <img class="rounded-full w-48 h-48 mb-4" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=botpic.jpg" alt="Extra large avatar">
                <div class="text-white text-lg font-semibold">Bot</div>
                <div class="text-white text-md">Iron 1</div>
                <div class="text-white text-md">Level 1</div>
            </div>
            """
            viewerObj.queueTurboAction(players, "quizLobbyDiv", viewerObj.turboApp.methods.update)

        elif purpose == FormPurposes.postQuizQuestion.value:
            partyID = form.pop("party", "")
            party = liveCacheManager.activeParties.get(partyID, None)
            if party: party.gameObj.sendPostQuizQuestion(viewerObj, form["question"])


def newVisitorCallback(viewerObj: BaseViewer):
    print("Visitor Joined: ", viewerObj.viewerID)

    initial = "<div id=\"fullPage\"></div>"
    viewerObj.queueTurboAction(initial, "mainDiv", viewerObj.turboApp.methods.update)
    userID = liveCacheManager.getKnownLoggedInUserID(viewerObj)
    if userID:
        liveCacheManager.loginCall(viewerObj, userID)
        renderHomepage(viewerObj)
    else:
        renderAuthPage(viewerObj)
    # sleep(2)
    # renderHomepage(viewerObj)
    # sleep(2)
    # renderQuizLobbyPage(viewerObj)
    # sleep(2)
    # renderQuizMatchFoundPage(viewerObj)
    # sleep(2)
    # renderQuizGamePage(viewerObj)
    # sleep(2)
    # renderQuizEndPage(viewerObj)
    # sleep(2)
    #loginInput(viewerObj)
    #sleep(2)
    #sendRegister(viewerObj)
    #sleep(2)
    # sendLogin(viewerObj)
    # sleep(2)


def visitorLeftCallback(viewerObj: BaseViewer):
    liveCacheManager.logoutCall(viewerObj)
    print("Visitor Left: ", viewerObj.viewerID)



logger = LogManager()
SQLconn = connectDB(logger)
liveCacheManager = UserCache()
extraHeads = f"""<script src="https://cdn.tailwindcss.com"></script>"""
bodyBase = """<body style="background-color: #23003d;"> <div id="mainDiv"><div></body>"""

baseApp, turboApp = createApps(formSubmitCallback, newVisitorCallback, visitorLeftCallback, CoreValues.appName.value,
                               Routes.webHomePage.value, Routes.webWS.value, ServerSecrets.webFernetKey.value,
                               extraHeads, bodyBase, CoreValues.title.value, False)


@baseApp.get(Routes.internalConnection.value)
def _internalConn():
    return ""


@baseApp.errorhandler(404)
def not_found(e):
    return get(f"http://127.0.0.1:{ServerSecrets.cdnPort.value}/{request.url.replace(request.root_url, '')}").content
    #return redirect(f"http://127.0.0.1:{ServerSecrets.cdnPort.value}/{request.url.replace(request.root_url, '')}")


try:
    open(r"C:\cert\privkey.pem", "r").close()
    print(f"https://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
    WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None, keyfile=r'C:\cert\privkey.pem', certfile=r'C:\cert\cert.pem').serve_forever()
except:
    print(f"http://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
    WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None).serve_forever()

