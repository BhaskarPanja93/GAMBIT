from gevent import monkey
monkey.patch_all()

from flask import redirect, request
from random import shuffle
from threading import Thread
from time import time, sleep
from pooledMySQL import Manager as MySQLPoolManager
from randomisedString import Generator as StringGenerator
from dynamicWebsite import *
from internal.Enums import *
from gevent.pywsgi import WSGIServer
from internal.Methods import *
from customisedLogs import Manager as LogManager
from werkzeug.security import check_password_hash, generate_password_hash
from json import loads, dumps



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
        <img src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=background-image.jpg" alt="Home screen image" class="rounded-3xl w-full h-5/6 object-cover">
         <form onsubmit="return submit_ws(this)">
                {viewerObj.addCSRF("renderQuiz")}
                <button type="submit" class="absolute top-1/3 left-1/2 transform -translate-x-1/2 bg-blue-700 text-white font-bold text-4xl rounded-full p-12">START LEARNING</button>
        </form>
        <p class="flex justify-center absolute top-2/3 left-1/2 transform -translate-x-1/2 translate-y-1 text-white font-bold text-7xl w-full">
            All Your Education Needs In One</p>
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
                    {viewerObj.addCSRF("login")}
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
                        {viewerObj.addCSRF("register")}
                        
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
<div class="bg-orange-700 flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">

    <div id="teamADiv" class="rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
        <div class="flex flex-col items-center">
            <div>HEALTH POINTS</div>
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


        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="mx-4 rounded w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <img class="mx-4 my-4 rounded-lg w-20 h-20"
                 src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp"
                 alt="Extra large avatar">
                    <div class="flex justify-center text-white text-bold text-xl m-2">Player 1</div>
                    <div class="flex justify-center text-white text-bold text-xl m-2">Correct</div>
                    <div class="flex justify-center text-white text-bold text-xl m-2">Incorrect</div>
                </div>
            </div>
        </div>
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="mx-4 rounded w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-xl m-4">Player 1</div>
                    <div class="text-white text-bold text-xl m-4">Correct</div>
                    <div class="text-white text-bold text-xl m-4">Incorrect</div>
                </div>
            </div>
        </div>
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="mx-4 rounded w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-xl m-4">Player 1</div>
                    <div class="text-white text-bold text-xl m-4">Correct</div>
                    <div class="text-white text-bold text-xl m-4">Incorrect</div>
                </div>
            </div>
        </div>
    </div>

    <div id="quizDiv" class="rounded-lg bg-blue-700 flex flex-col items-center justify-center w-full h-full">
        <div class="rounded-lg px-2 mx-6 bg-blue-100 text-green font-bold text-2xl p-4">
            <div class="text-black font-bold text-2xl h-1/3 p-4 m-4" id="questionText">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae risus efficitur quam imperdiet
                sagittis. Suspendisse rutrum iaculis lectus sit amet maximus. Integer tincidunt in arcu vitae
                condimentum.
                Nunc porta ex elit, eget sollicitudin tellus pharetra quis. Ut laoreet, enim maximus dapibus
                ullamcorper,
                arcu leo scelerisque quam, a vulputate ligula turpis eu dolor. Proin sem sem, elementum ut nulla nec,
                fermentum fringilla libero. Maecenas eu facilisis erat, vitae iaculis orci. Donec volutpat enim vitae
                leo
                convallis hendrerit.

            </div>
        </div>


        <div class="text-white font-bold text-2xl p-4">Select an option</div>

        <div id="options" class="grid grid-cols-2 gap-4 px-12 py-4 place-content-stretch h-1/2 w-5/6"></div>
        </div>

        <div id="teamBDiv" class="rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
            <div class="flex flex-col items-center">
                <div>HEALTH POINTS</div>
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

        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="mx-4 rounded w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-xl m-4">Player 1</div>
                    <div class="text-white text-bold text-xl m-4">Correct</div>
                    <div class="text-white text-bold text-xl m-4">Incorrect</div>
                </div>
            </div>
        </div>
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="mx-4 rounded w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-xl m-4">Player 1</div>
                    <div class="text-white text-bold text-xl m-4">Correct</div>
                    <div class="text-white text-bold text-xl m-4">Incorrect</div>
                </div>
            </div>
        </div>
        <div class="rounded-lg bg-red-200 mx-4 my-2 flex justify-between items-center">
            <img class="mx-4 rounded w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profilepic.webp" alt="Extra large avatar">
            <div class="flex items-center gap-4">
                <div class="font-medium dark:text-white">
                    <div class="text-white text-bold text-xl m-4">Player 1</div>
                    <div class="text-white text-bold text-xl m-4">Correct</div>
                    <div class="text-white text-bold text-xl m-4">Incorrect</div>
                </div>
            </div>
        </div>
    </div>
</div>
"""


    viewerObj.queueTurboAction(quiz, "fullPage", viewerObj.turboApp.methods.update)


# Ending Quiz Page
def renderQuizEndPage(viewerObj: BaseViewer):
    quizEnd = f"""
    <div class="bg-orange-700 flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">
    <div id="leaderboardDiv" class="rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
        <div class="flex flex-col items-center">
            <div class="my-4 text-bold underline text-gray text-3xl font-bold">Leaderboard</div>
        </div>

        <!-- Leaderboard Entries -->
        <div id="quizLeaderboard_create"></div>

        </div>
    </div>

        <div class="p-8 rounded-lg bg-blue-700 flex flex-col items-center justify-center w-full h-full">
            <div class="p-8 rounded-lg mx-6 bg-blue-200 text-green font-bold text-2xl h-full w-full">
                <div id="resultTextDiv" class="flex justify-center items-center text-black font-bold text-2xl h-1/3"></div>
            </div>
        </div>

        <div id="questionListDiv" class="rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
            <div class="flex flex-col items-center">
                <div>QUESTIONS LIST</div>
            </div>
            <div class="flex flex-col items-center mt-4">
                <ul class="grid grid-cols-1 gap-2 w-full h-full p-4">
                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question1')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">1</button>
                        <form>
                    </li>
                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question2')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">2</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question3')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">3</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question4')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">4</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question5')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">5</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question6')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">6</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question7')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">7</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question8')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">8</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question9')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">9</button>
                        <form>
                    </li>

                    <li>
                        <form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF('question10')}
                        <button class="rounded-lg bg-blue-100 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">10</button>
                        <form>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    """
    viewerObj.queueTurboAction(quizEnd, "fullPage", viewerObj.turboApp.methods.update)


def renderQuizLobbyPage(viewerObj: BaseViewer):
    quizLobby = f"""

    <div class="bg-orange-700 flex h-full w-full gap-8 px-6 py-6">

        <div class="w-full">
            <h1 class="flex justify-center text-3xl font-bold text-white">Lobby</h1>

          <div id="quizLobbyDiv" class="p-8 rounded-lg grid grid-cols-3 w-full h-full gap-4">
            <div class="bg-blue-500 h-full rounded-lg flex flex-col justify-between items-center py-6">
                <img class="rounded-full w-48 h-48 mb-4" src="static/images/profilepic.webp" alt="Extra large avatar">
                <div class="text-white text-xl font-bold text-center">Username</div> <!-- Increased size and centered -->
                <div class="text-white text-lg text-center">Rank</div> <!-- Increased size and centered -->
                <div class="text-white text-lg text-center">Level</div> <!-- Increased size and centered -->
            </div>

            <div class="bg-red-500 h-full rounded-lg flex flex-col justify-between items-center py-6">
                <img class="rounded-full w-48 h-48 mb-4" src="static/images/profilepic.webp" alt="Extra large avatar">
                <div class="text-white text-lg font-semibold">Username</div>
                <div class="text-white text-md">Rank</div>
                <div class="text-white text-md">Level</div>
            </div>
            <div class="bg-green-500 h-full rounded-lg flex flex-col justify-between items-center py-6">
                <img class="rounded-full w-48 h-48 mb-4" src="static/images/profilepic.webp" alt="Extra large avatar">
                <div class="text-white text-lg font-semibold">Username</div>
                <div class="text-white text-md">Rank</div>
                <div class="text-white text-md">Level</div>
            </div>
          </div>
        </div>
        <div id="quizFriendListDiv" class="p-6 flex items-center rounded-lg bg-blue-700 flex flex-col h-full w-1/3">
            <!-- Queue Up Button -->
            <form class="w-full" onsubmit="return submit_ws(this)">
                {viewerObj.addCSRF('startQueue')}
                <button type="submit" class="w-full p-4 rounded-full flex justify-center bg-gray-700 mb-4">
                    <div id="queueTimer" class="w-full text-white font-bold">QUEUE UP</div>
                </button>
            </form>

            <!-- Friend List Container -->
            <div class="rounded-lg h-full w-full bg-yellow-200 m-8 p-4">
                <!-- Friend List Title -->
                <div class="text-dark font-bold flex justify-center mb-4">FRIEND LIST</div>

                <!-- Individual Friend Entries -->
                <div class="flex flex-col space-y-2">
                    <!-- Friend 1 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 1</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 2 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 2</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 3 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 3</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 4 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 4</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 5 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 5</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 6 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 6</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 7 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 7</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 8 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 8</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 9 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 9</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                    <!-- Friend 10 -->
                    <div class="bg-white rounded-lg p-2 flex justify-between items-center">
                        <span class="font-semibold">Friend 10</span>
                        <button class="bg-blue-500 text-white px-4 py-1 rounded-lg">Invite</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
    """
    viewerObj.queueTurboAction(quizLobby, "fullPage", viewerObj.turboApp.methods.update)


def renderQuizMatchFoundPage(viewerObj: BaseViewer):
    matchFound = f"""
        <div class="bg-orange-700 flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">
            <div id="quizDiv" class="rounded-lg bg-gray-100 flex flex-col items-center justify-center w-full h-full">
                <h1 class="text-7xl text-dark font-bold">MATCH FOUND</h1>
        </div>
        </div>

        """
    viewerObj.queueTurboAction(matchFound, "fullPage", viewerObj.turboApp.methods.update)



def sendRegisterForm(viewerObj:BaseViewer):
    form = f"""<form onsubmit="return submit_ws(this)">
                        {viewerObj.addCSRF("register")}
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
                    {viewerObj.addCSRF("login")}
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="username" placeholder="Username">
                    <input autocomplete="off" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           type="password" name="password" placeholder="Password">
                    <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit</button>
                </form>"""
    viewerObj.queueTurboAction(form, "loginFormContainer", viewerObj.turboApp.methods.update)


class Party:
    def __init__(self):
        self.players: dict[str, dict] = {}  # "abc":{"Team":team, "Viewer":viewer}
        self.sides: dict[str, list[BaseViewer]] = {"A": [], "B": []}
        self.teamSize = {"A": 0, "B": 0}
        self.partyStartAt = time()
        self.gameStarted = False
        self.quiz = None
        Thread(target=self.forceStartTimer).start()

    def forceStartTimer(self):
        while time() - self.partyStartAt < 4 and not self.gameStarted:
            for team in self.sides:
                for player in self.sides[team]:
                    player.queueTurboAction(str(4 - int(time() - self.partyStartAt)), "queueTimer", player.turboApp.methods.update.value)
            sleep(0.1)
        self.initGame()

    def joinTeam(self, viewer: BaseViewer, team=None):
        def _PlayerJoinTeam(self, viewer, team):
            self.teamSize[team] += 1
            self.sides[team].append(viewer)

        if team is None:
            if self.teamSize["A"] + self.teamSize["B"] < 6:
                if self.teamSize["A"] < self.teamSize["B"]:
                    team = "A"
                else:
                    team = "B"
                _PlayerJoinTeam(self, viewer, team)
        else:
            _PlayerJoinTeam(self, viewer, team)

    def leaveTeam(self, viewer: BaseViewer, team):
        if viewer in self.sides[team]:
            self.teamSize[team] -= 1
            self.sides[team].remove(viewer)

    def initGame(self):
        self.gameStarted = True
        for side in self.sides:
            for player in self.sides[side]:
                self.players[player.viewerID] = {"Team": side, "Viewer": player}
                renderQuizMatchFoundPage(player)
        waitingParties.remove(self)
        activeParties.append(self)
        self.quiz = Quiz(turboApp, SQLconn)
        self.quiz.startQuiz(self.sides, self.players)



class Question:
    def __init__(self):
        self.questionID = ""
        self.questionStatement = ""
        self.teamOptions: dict[str, list[str]] = {"A": [], "B": []}
        self.correctAnswers = []

    def setValues(self, questionID, question: str, options: dict[str, list[str]]):
        self.questionID = questionID
        self.questionStatement = question
        self.correctAnswers = options["Correct"]
        for team in self.teamOptions:
            shuffle(options["InCorrect"])
            for _ in range(3):
                while True:
                    option = options["InCorrect"][_]
                    if option not in self.teamOptions[team]:
                        self.teamOptions[team].append(option)
                        break
            self.teamOptions[team].append(options["Correct"][0])
            shuffle(self.teamOptions[team])


class Quiz:
    def __init__(self, turboApp: ModifiedTurbo, MySQLPool: MySQLPoolManager):
        self.sides: dict[str, list[BaseViewer]] = {"A": [], "B": []}
        self.MySQLPool = MySQLPool
        self.turboApp = turboApp

        self.startTime = time()
        self.matchID = StringGenerator().AlphaNumeric(50, 50)
        self.questionsStarted = False
        self.endTime = 0.0

        self.players: dict[str, dict] = {}  # "abc":{"Team":team, "Viewer":viewer}
        self.teamHealth = {}
        self.scores = {}  # "abc":10

        self.questions: list[Question] = []
        self.questionIndex = -1
        self.optionsPressed = {}

    def renderPlayers(self):
        for playerID in self.players:
            for side in self.sides:
                for _player in self.sides[side]:
                    if self.players[playerID]["Team"] == side:
                        self.players[playerID]["Viewer"]
                    else:
                        self.players[playerID]["Viewer"]

    def extractQuestions(self):
        for questionData in self.MySQLPool.execute("SELECT * from questions where QuizEligible=1 ORDER BY RAND() LIMIT 30"):
            question = Question()
            question.setValues(questionData["QuestionID"], questionData["Text"], loads(questionData["Options"]))
            self.questions.append(question)
        self.questionIndex = -1

    def nextQuestion(self):
        self.questionIndex += 1
        self.optionsPressed = {}
        currentQuestion = self.questions[self.questionIndex]
        for playerID in self.players:
            viewer = self.players[playerID]["Viewer"]
            team = self.players[playerID]["Team"]
            viewer.queueTurboAction(currentQuestion.questionStatement, "questionText", viewer.turboApp.methods.update.value)
            options = f"""<form onsubmit="return submit_ws(this)">
                {viewer.addCSRF("quizOption")}
                <input type="hidden" name="option" value="0">
                <button class="rounded-lg bg-yellow-400 flex items-center justify-center h-full w-full">
                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[team][0]}</div>
                </button>
            </form>
            <form onsubmit="return submit_ws(this)">
                {viewer.addCSRF("quizOption")}
                <input type="hidden" name="option" value="1">
                <button class="rounded-lg bg-red-700 flex items-center justify-center h-full w-full">
                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[team][1]}</div>
                </button>
            </form>
            <form onsubmit="return submit_ws(this)">
                {viewer.addCSRF("quizOption")}
                <input type="hidden" name="option" value="2">
                <button class="rounded-lg bg-orange-400 flex items-center justify-center h-full w-full">
                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[team][2]}</div>
                </button>
            </form>
            <form onsubmit="return submit_ws(this)">
                {viewer.addCSRF("quizOption")}
                <input type="hidden" name="option" value="3">
                <button class="rounded-lg bg-blue-200 flex items-center justify-center h-full w-full">
                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[team][3]}</div>
                </button>
            </form>"""
            viewer.queueTurboAction(options, "options", viewer.turboApp.methods.update.value)

    def receiveUserInput(self, viewer: BaseViewer, optionIndex):
        optionIndex = int(optionIndex)
        print(viewer.viewerID, optionIndex, type(optionIndex))
        if len(self.questions[self.questionIndex].teamOptions[self.players[viewer.viewerID]["Team"]]) > optionIndex >= 0:
            if viewer.viewerID not in self.optionsPressed:
                self.optionsPressed[viewer.viewerID] = optionIndex
                options = f"""<button class="col-span-2 rounded-lg bg-yellow-400 flex items-center justify-center h-full w-full">
                                    <div class="text-white font-bold text-2xl">{self.questions[self.questionIndex].teamOptions[self.players[viewer.viewerID]["Team"]][optionIndex]}</div>
                                </button>"""
                viewer.queueTurboAction(options, "options", viewer.turboApp.methods.update.value)
                print(len(self.optionsPressed) , len(self.players))
                if len(self.optionsPressed) == len(self.players):
                    sleep(2)
                    self.endQuestion()

    def endQuestion(self):
        points = {}
        for viewerID in self.optionsPressed:
            if viewerID not in self.scores:
                self.scores[viewerID] = 0
            if self.players[viewerID]["Team"] not in points:
                points[self.players[viewerID]["Team"]] = 0

            option = self.questions[self.questionIndex].teamOptions[self.players[viewerID]["Team"]][self.optionsPressed[viewerID]]
            if option in self.questions[self.questionIndex].correctAnswers:
                points[self.players[viewerID]["Team"]] += 1
                self.scores[viewerID] += 10
            else:
                points[self.players[viewerID]["Team"]] -= 1
                self.scores[viewerID] -= 10

        for side in self.sides:
            if side not in points:
                self.updateHealth(side, -3)
                points[side] = 0
            elif points[side] <= 0:
                self.updateHealth(side, -10)
                points[side] = 0
        for side in self.sides:
            for _otherSide in self.sides:
                if side!=_otherSide and points[side]<points[_otherSide]:
                    self.updateHealth(side, 2*(1+self.questionIndex)*(points[side]-points[_otherSide]))
        print(self.teamHealth)
        print(self.scores)
        self.nextQuestion()

    def updateHealth(self, teamChanged: str, offset):
        self.teamHealth[teamChanged] += offset
        if self.teamHealth[teamChanged] <0: self.teamHealth[teamChanged] = 0
        for playerID in self.players:
            viewer = self.players[playerID]["Viewer"]
            team = self.players[playerID]["Team"]
            bar = f"""<svg class="rotate-[135deg] size-full" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="18" cy="18" r="16" fill="none"
                                class="stroke-current text-green-200 dark:text-neutral-700"
                                stroke-width="1" stroke-dasharray="75 100" stroke-linecap="round"></circle>
                        <circle cx="18" cy="18" r="16" fill="none"
                                class="stroke-current text-green-500 dark:text-green-500"
                                stroke-width="2" stroke-dasharray="{75*self.teamHealth[teamChanged]/100} 100" stroke-linecap="round"></circle>
                    </svg>"""
            if team == teamChanged:
                viewer.queueTurboAction(bar, f"selfTeamHealthBar", viewer.turboApp.methods.update.value)
                viewer.queueTurboAction(str(self.teamHealth[teamChanged]), f"selfTeamHealthText", viewer.turboApp.methods.update.value)
            else:
                viewer.queueTurboAction(bar, f"otherTeamHealthBar", viewer.turboApp.methods.update.value)
                viewer.queueTurboAction(str(self.teamHealth[teamChanged]), f"otherTeamHealthText", viewer.turboApp.methods.update.value)

        if self.teamHealth[teamChanged] == 0:
            sortedPlayerList = dict(sorted(self.scores.items(), key=lambda key_val: key_val[1], reverse=True))
            for side in self.sides:
                for player in self.sides[side]:
                    renderQuizEndPage(player)
                    if side == teamChanged:
                        player.queueTurboAction("DEFEAT", "resultTextDiv", player.turboApp.methods.update)
                    else:
                        player.queueTurboAction("VICTORY", "resultTextDiv", player.turboApp.methods.update)
                    rank = 0
                    for viewerID in sortedPlayerList:
                        rank += 1
                        username = viewerToUsernameMaps.get(viewerID, "")
                        score = sortedPlayerList[viewerID]
                        playerDiv = f"""<div class="rounded-lg bg-red-200 mx-6 my-6 flex justify-between items-center h-20 p-2 w-5/6">
                                    <div class="font-medium text-bold text-3xl dark:text-white">{rank}</div>
                                    <div class="w-full p-4 flex items-center justify-start"> <!-- Updated ID and alignment -->
                                        <img class="mr-4 rounded w-16 h-16" src="static/images/profilepic.webp" alt="Extra large avatar">
                                        <div class="rounded-lg bg-red-700 mr-8 font-medium dark:text-white">
                                            <div class="px-2 text-white text-bold text-xl">{username}</div>
                                            <div class="px-2 text-white text-bold text-xl">Points: {score}</div>
                                        </div>
                                    </div>
                            </div>"""
                        player.queueTurboAction(playerDiv, "quizLeaderboard", player.turboApp.methods.newDiv.value)





    def startQuiz(self, sides: dict[str, list[BaseViewer]], players):
        started = time()
        self.sides = sides
        self.players = players
        self.extractQuestions()
        sleep(3-(time()-started))
        for playerID in self.players:
            renderQuizGamePage(self.players[playerID]["Viewer"])
        for side in sides:
            self.teamHealth[side] = 100
            self.updateHealth(side, 0)
        self.renderPlayers()
        self.nextQuestion()

    def endQuiz(self):
        pass

    def saveToDB(self):
        pass


def registerUser(viewerObj:BaseViewer, form:dict):
    username = form.get("username", "")
    email = form.get("email", "")
    password = form.get("password", "")
    confirm_password = form.get("confirm_password", "")
    name = form.get("name", "")
    age = int(form.get("age", 0))
    if not username:
        viewerObj.queueTurboAction("Invalid Username", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    elif SQLconn.execute(f"SELECT UserName from user_auth where UserName=\"{username}\" limit 1"):
        viewerObj.queueTurboAction("Username Taken", "registrationWarning", viewerObj.turboApp.methods.update.value)
        sendRegisterForm(viewerObj)
    elif email.count("@")!=1 or email.count(".")!=1:
        viewerObj.queueTurboAction("Email not valid", "registrationWarning", viewerObj.turboApp.methods.update.value)
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
                break

def loginUser(viewerObj:BaseViewer, form:dict):
    username = form.get("username", "")
    password = form.get("password", "")
    if not SQLconn.execute(f"SELECT UserName from user_auth where UserName=\"{username}\" limit 1"):
        viewerObj.queueTurboAction("Username Dont Match", "loginWarning", viewerObj.turboApp.methods.update.value)
        sendLoginForm(viewerObj)
    elif not check_password_hash(SQLconn.execute(f"SELECT PWHash from user_auth where UserName=\"{username}\"")[0]["PWHash"].decode(), password):
        viewerObj.queueTurboAction("Password Dont Match", "loginWarning", viewerObj.turboApp.methods.update.value)
        sendLoginForm(viewerObj)
    else:
        renderHomepage(viewerObj)


def formSubmitCallback(viewerObj: BaseViewer, form: dict):
    if form is not None:
        purpose = form.pop("PURPOSE")
        print(purpose, form)

        if purpose == FormPurposes.register.value:
            registerUser(viewerObj, form)

        elif purpose == FormPurposes.login.value:
            loginUser(viewerObj, form)

        elif purpose == FormPurposes.startQueue.value:
            if waitingParties:
                for party in waitingParties:
                    party.joinTeam(viewerObj)
                    break
            else:
                party = Party()
                waitingParties.append(party)
                party.joinTeam(viewerObj)
        elif purpose == "quizOption":
            for party in activeParties:
                if viewerObj.viewerID in party.players:
                    party.quiz.receiveUserInput(viewerObj, form["option"])

        elif purpose == "renderQuiz":
            renderQuizLobbyPage(viewerObj)


def newVisitorCallback(viewerObj: BaseViewer):
    print("Visitor Joined: ", viewerObj.viewerID)

    initial = "<div id=\"fullPage\"></div>"
    viewerObj.queueTurboAction(initial, "mainDiv", viewerObj.turboApp.methods.update)

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
    # quizEndPage(viewerObj)
    # sleep(2)
    #loginInput(viewerObj)
    #sleep(2)
    #sendRegister(viewerObj)
    #sleep(2)
    # sendLogin(viewerObj)
    # sleep(2)


def visitorLeftCallback(viewerObj: BaseViewer):
    print("Visitor Left: ", viewerObj.viewerID)



logger = LogManager()
SQLconn = connectDB(logger)
activeParties:list[Party] = []
waitingParties:list[Party] = []
viewerToUsernameMaps = {}
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
    return redirect(f"http://127.0.0.1:{ServerSecrets.cdnPort.value}/{request.url.replace(request.root_url, '')}")


print(f"http://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None).serve_forever()
