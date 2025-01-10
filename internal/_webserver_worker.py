from gevent import monkey
monkey.patch_all()
from json import dumps
import os
import wave
from random import choice, randrange, choices
from flask import request, send_from_directory, Response
from random import shuffle
from threading import Thread
from time import time, sleep
from randomisedString import RandomisedString as StringGenerator
from dynamicWebsite import DynamicWebsite
from Enums import *
from gevent.pywsgi import WSGIServer
from Methods import *
from customisedLogs import Manager as LogManager
from werkzeug.security import check_password_hash, generate_password_hash
from json import loads


def navBar(viewerObj: DynamicWebsite.BaseViewer):
    navigation_bar = f"""

        <div class="relative flex items-center justify-center h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto">
                    <a href="#" class="flex items-center space-x-4">
                        <!-- Logo Image -->
                        <img class="w-auto h-14 sm:h-18" src="/-cdn-file?type=image&name=dice.png" loading="lazy" width="202" height="80">
                        <!-- GAMBIT Text -->
                        <p class="text-3xl text-white font-bold">GAMBIT</p>
                    </a>
                </div>
            </div>
            <div class="text-white font-semibold text-3xl flex justify-center mt-3">THE ALL IN ONE EDUCATION PLATFORM</div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="p-4 inline-flex rounded-full">   
                    <form>
                        {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
                        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-6">
                            Log out
                        </button>
                    </form>
                </div>
            </div>
        </div>
    """

    viewerObj.updateHTML(navigation_bar, "navBar", DynamicWebsite.UpdateMethods.update)


def renderLogo(viewerObj: DynamicWebsite.BaseViewer, allowNavigation=True):
    logo = f"""
    <form>
        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-6 bg-transparent">
            {viewerObj.addCSRF(FormPurposes.renderSubCategories.value) if allowNavigation else ""}
            <img class="w-auto h-14 sm:h-18" src="/-cdn-file?type=image&name=dice.png" loading="lazy" width="202" height="80">
            <p class="text-3xl text-white font-bold">GAMBIT</p>
        </button>
    </form>"""
    viewerObj.updateHTML(logo, "navLogoButton", DynamicWebsite.UpdateMethods.update)


def renderHomepage(viewerObj: DynamicWebsite.BaseViewer):
    home = f"""

        <div class="relative flex items-center justify-center h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto"></div>
            </div>
            <div class="text-white font-semibold text-3xl flex justify-center mt-3">THE ALL IN ONE EDUCATION PLATFORM</div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="p-4 inline-flex rounded-full">   
                    <form>
                        {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
                        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-6">
                            Log out
                        </button>
                    </form>
                </div>
            </div>
        </div>

    <div class="px-12 w-full sm:px-12 md:px-12 lg:px-12">
        <div class="relative pt-6 pb-16 sm:pb-24">
            <div id="imageBackground" class="relative py-12 w-full h-5/6">
                <!-- Image -->
               <!-- <img src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=background-image.jpg" style="opacity: 0.7;" alt="Home screen image" class="rounded-3xl w-full h-5/6 object-cover"> -->

                <video autoplay muted loop class="absolute rounded-3xl w-full h-5/6 object-cover z-0">
                    <source src="{Routes.cdnFileContent.value}?type={CDNFileType.video.value}&name=login_background_video1.mp4"
                    type="video/mp4"> </video>
                <!-- Start Learning Button -->
                <form>
                    {viewerObj.addCSRF(FormPurposes.renderSubCategories.value)}
                    <button type="submit" class="absolute top-1/3 left-1/2 transform -translate-x-1/2 bg-white font-bold text-4xl rounded-full p-12 hover:scale-105 transition duration-300 ease-in-out" style="color: #23003d;">
                START LEARNING
            </button>
                </form>

                <!-- Headline Text -->
                <p class="flex justify-center absolute top-2/3 left-1/2 transform -translate-x-1/2 translate-y-1 text-white font-bold text-7xl w-full relative z-10">
                    All Your Education Needs In One
                </p>

            </div>
        </div>
    </div>
"""
    viewerObj.updateHTML(home, "fullPage", DynamicWebsite.UpdateMethods.update)
    renderLogo(viewerObj)


def renderAuthPage(viewerObj: DynamicWebsite.BaseViewer):
    loginRegister = f"""

<div class="relative min-h-screen flex justify-center">
    <!-- Background Video -->
    <video autoplay muted loop class="absolute top-0 left-0 w-full h-full object-cover" style="opacity: 0.7;">
        <source src="{Routes.cdnFileContent.value}?type={CDNFileType.video.value}&name=login_background_video1.mp4"
                type="video/mp4">
        Your browser does not support the video tag.
    </video>

    <!-- Overlay Content -->
    <div class="relative flex flex-col items-center justify-start w-full z-10 p-7">
        <!-- GAMBIT Text and Join Now Button -->
        <div class="flex items-center justify-between w-full">
            <div id="navLogoButton" class="flex items-center space-x-4"></div>
            <div class="p-4 inline-flex rounded-full"></div>
        </div>
        <div class="flex justify-center text-3xl text-white font-semibold">THE ALL IN ONE EDUCATION PLATFORM</div>


        <div class="flex items-center justify-center h-3/4 w-full mt-8">
            <div class="grid grid-cols-2 gap-8 place-content-stretch w-full">
                <!-- Login Section -->
                <div id="loginDiv"
                     class="rounded-lg bg-transparent flex items-center justify-center h-96 shadow-2xl hover:scale-105 hover:transition duration-300 ease-in-out backdrop-blur-lg border border-white">
                    <button id="loginButton"
                            class="rounded-lg bg-transparent flex items-center justify-center h-96 w-full shadow-2xl border border-white">
                        <div class="w-full text-white font-bold text-4xl relative z-10">Login</div>
                    </button>
                    <div id="loginFormContainer"
                         class="hidden w-full rounded-lg bg-transparent flex items-center justify-center h-96 shadow-2xl">
                        <form>
                            {viewerObj.addCSRF(FormPurposes.submitLogin.value)}
                            <input type="text" autocomplete="off"
                                   class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                   name="username" placeholder="Username">
                            <input autocomplete="off"
                                   class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                   type="password" name="password" placeholder="Password">
                            <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Register Section -->
                <div id="registerDiv"
                     class="rounded-lg bg-transparent flex items-center justify-center h-96 shadow-2xl hover:scale-105 hover:transition duration-300 ease-in-out backdrop-blur-lg border border-white">
                    <button id="registerButton"
                            class="rounded-lg bg-transparent flex items-center justify-center h-96 w-full shadow-2xl border border-white">
                        <div class="w-full text-white font-bold text-4xl">Register</div>
                    </button>

                    <div id="registerFormContainer"
                         class="hidden w-full rounded-lg bg-transparent flex items-center justify-center h-96 shadow-2xl">
                        <form class="w-full px-6">
                            {viewerObj.addCSRF(FormPurposes.submitRegister.value)}

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
    viewerObj.updateHTML(loginRegister, "fullPage", DynamicWebsite.UpdateMethods.update)
    sendRegisterForm(viewerObj)
    sendLoginForm(viewerObj)
    renderLogo(viewerObj, False)


def renderQuizGamePage(viewerObj: DynamicWebsite.BaseViewer):
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


    viewerObj.updateHTML(quiz, "fullPage", DynamicWebsite.UpdateMethods.update)


# Ending Quiz Page
def renderQuizEndPage(viewerObj: DynamicWebsite.BaseViewer):
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
    viewerObj.updateHTML(quizEnd, "fullPage", DynamicWebsite.UpdateMethods.update)


def renderQuizLobbyPage(viewerObj: DynamicWebsite.BaseViewer):
    quizLobby = f"""
            <div class="relative flex items-center justify-center h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto bg-transparent">

                </div>
            </div>
            <div class="text-white font-semibold text-3xl flex justify-center mt-3">THE ALL IN ONE EDUCATION PLATFORM</div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="p-4 inline-flex rounded-full">   
                    <form>
                        {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
                        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-6">
                            Log out
                        </button>
                    </form>
                </div>
            </div>
        </div>
    <div class="bg-[#23003d] flex h-full w-full gap-8 px-6 py-6">

        <div class="w-full">
            <h1 class="flex justify-center text-3xl font-bold text-white">Lobby</h1>

          <div id="quizLobbyDiv" class="p-8 rounded-lg grid grid-cols-3 w-full h-full gap-4"> </div>
        </div>
        <div id="quizFriendListDiv" class="p-6 flex items-center rounded-lg bg-[#490080] flex flex-col h-full w-1/3">
            <!-- Queue Up Button -->
            <form class="w-full"
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
    viewerObj.updateHTML(quizLobby, "fullPage", DynamicWebsite.UpdateMethods.update)
    renderLogo(viewerObj)


def renderQuizMatchFoundPage(viewerObj: DynamicWebsite.BaseViewer):
    matchFound = f"""
        <div class="rounded-lg bg-[#23003d] flex items-center justify-stretch h-full w-full gap-8 px-6 py-6 place-content-stretch">
            <div id="quizDiv" class="rounded-lg bg-gradient-to-t from-gray-700 to-gray-900 flex flex-col items-center justify-center w-full h-full">
                <h1 class=" text-7xl text-white font-bold">MATCH FOUND</h1>
        </div>
        </div>

        """
    viewerObj.updateHTML(matchFound, "fullPage", DynamicWebsite.UpdateMethods.update)


# <div class="bg-[#000000]">
#         <div class="rounded-lg flex flex-col h-full w-1/3">
#             <div class="flex flex-col items-center">
#                 <div class="text-white">HELLO</div>
#             </div>
#         </div>
#     </div>
def renderContentMarketPlace(viewerObj: DynamicWebsite.BaseViewer):
    contentMarketPlace = f"""
    <script>
        function findMarketplaceSearch(text)
        {{
            text = document.getElementById("marketplaceSearch").value.toLowerCase();
            
            for (const [key, value] of Object.entries(document.getElementById("marketplaceHolder").children)) 
            {{ 
                if (value.getAttribute("title").toLowerCase().includes(text.toLowerCase()) || value.getAttribute("subject").toLowerCase().includes(text.toLowerCase()))
                {{
                    value.hidden=false;
                }} else {{
                    value.hidden=true;
                }}
            }}
        }}    
        document.getElementById("marketplaceSearch").addEventListener("input", findMarketplaceSearch);

    </script>
    <nav class="relative flex items-center justify-between h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto"></div>
            </div>

            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="p-4 inline-flex rounded-full">   
                    <form>
                        {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
                        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-9">
                            Log out
                        </button>
                    </form>
                </div>
            </div>
        </nav>
        <div class="p-6 m-6">
            <div class="text-white text-7xl w-full">CONTENT MARKETPLACE</div>
            <div class="text-gray-300 text-xl my-7">Explore a wide range of educational videos. offering easy-to-follow tutorials and expert insights. <br>Learn at your own pace with engaging content designed for all levels.</div>
        </div>
        <div class="w-full p-6 -mt-4 relative">
            <input type="text" id="marketplaceSearch" placeholder="Search..." class="bg-gray-800 w-full p-5 text-lg border rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"/>  
        </div>


<!-- Video display goes here -->

<div class="heading text-center font-semibold text-2xl m-5 text-gray-100">VIDEOS HERE</div>

<div id="marketplaceHolder" class="holder mx-auto w-10/12 grid sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
    <!-- each -->
    <div class="rounded-lg each mb-10 m-2 shadow-lg border-gray-800 bg-gray-100 relative" subject="Operating Systems" title="Operating System Syllabus Discussion for all College/University & Competitive exams">
        <img class="rounded-lg w-full" src="https://cdn.hashnode.com/res/hashnode/image/upload/v1700577267403/a4f278fb-2ff6-40e8-af45-dadc5aa794be.jpeg" alt=""/>
        <div class="badge absolute top-0 right-0 bg-indigo-500 m-1 text-gray-200 p-1 px-2 text-xs font-bold rounded">
            10:53
        </div>
        <div class="info-box text-xs flex p-1 font-semibold text-gray-500 bg-gray-300">
            <span class="mr-1 p-1 px-2 font-bold">105 views</span>
            <span class="mr-1 p-1 px-2 font-bold border-l border-gray-400">105 Likes</span>
            <span class="mr-1 p-1 px-2 font-bold border-l border-gray-400">105 Dislikes</span>
        </div>
        <div class="desc p-4 text-gray-800">
            <a href="https://youtube.com/watch?v=bkSWJJZNgf8" target="_new"
               class="title font-bold block cursor-pointer hover:underline">Multiprogramming and Multitasking Operating System</a>
            <a href="" target="_new"
               class="badge bg-indigo-500 text-blue-100 rounded px-1 text-xs font-bold cursor-pointer">@youtube_channel_link_here</a>
            <span class="description text-sm block py-2 border-gray-400 mb-2">Video Description Here</span>
        </div>
    </div>
  

    <!-- each -->
    <div class="rounded-lg each mb-10 m-2 shadow-lg border-gray-800 bg-gray-100 relative" subject="Operating Systems" title="Multiprogramming and Multitasking Operating System">
        <img class="rounded-lg w-full" src="https://cdn.automationforum.co/uploads/2018/12/operating-sys.png" alt=""/>
        <div class="badge absolute top-0 right-0 bg-indigo-500 m-1 text-gray-200 p-1 px-2 text-xs font-bold rounded">
            10:53
        </div>
        <div class="info-box text-xs flex p-1 font-semibold text-gray-500 bg-gray-300">
            <span class="mr-1 p-1 px-2 font-bold">105 views</span>
            <span class="mr-1 p-1 px-2 font-bold border-l border-gray-400">105 Likes</span>
            <span class="mr-1 p-1 px-2 font-bold border-l border-gray-400">105 Dislikes</span>
        </div>
        <div class="desc p-4 text-gray-800">
            <a href="https://youtube.com/watch?v=3MqyDWDpZoI" target="_new"
               class="title font-bold block cursor-pointer hover:underline">Multiprogramming and Multitasking Operating System</a>
            <a href="" target="_new"
               class="badge bg-indigo-500 text-blue-100 rounded px-1 text-xs font-bold cursor-pointer">@youtube_channel_link_here</a>
            <span class="description text-sm block py-2 border-gray-400 mb-2">Video Description Here</span>
        </div>
    </div>
 

    <!-- each -->
    <div class="rounded-lg each mb-10 m-2 shadow-lg border-gray-800 bg-gray-100 relative" subject="Programming" title="Roadmap of DSA | Syllabus of Data structure">
        <img class="rounded-lg w-full" src="https://media.geeksforgeeks.org/wp-content/cdn-uploads/20230706095706/intro-data-structure-%E2%80%93-1.png" alt=""/>
        <div class="badge absolute top-0 right-0 bg-indigo-500 m-1 text-gray-200 p-1 px-2 text-xs font-bold rounded">
            10:53
        </div>
        <div class="info-box text-xs flex p-1 font-semibold text-gray-500 bg-gray-300">
            <span class="mr-1 p-1 px-2 font-bold">105 views</span>
            <span class="mr-1 p-1 px-2 font-bold border-l border-gray-400">105 Likes</span>
            <span class="mr-1 p-1 px-2 font-bold border-l border-gray-400">105 Dislikes</span>
        </div>
        <div class="desc p-4 text-gray-800">
            <a href=" https://youtube.com/watch?v=qNGyI95E5AE" target="_new"
               class="title font-bold block cursor-pointer hover:underline">Roadmap of DSA | Syllabus of Data structure</a>
            <a href="" target="_new"
               class="badge bg-indigo-500 text-blue-100 rounded px-1 text-xs font-bold cursor-pointer">@youtube_channel_link_here</a>
            <span class="description text-sm block py-2 border-gray-400 mb-2">Video Description Here</span>
        </div>
    </div>
</div>  


    """
    viewerObj.updateHTML(contentMarketPlace, "fullPage", DynamicWebsite.UpdateMethods.update)
    renderLogo(viewerObj)


def renderSubCategories(viewerObj: DynamicWebsite.BaseViewer):
    subCategories = f"""
        <nav class="relative flex items-center justify-between h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto"></div>
            </div>

            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="p-4 inline-flex rounded-full">   
                    <form>
                        {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
                        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-9">
                            Log out
                        </button>
                    </form>
                </div>
            </div>
        </nav>

<div class="px-12 w-full sm:px-12 md:px-12 lg:px-12">
    <div class="relative pt-6 pb-16 sm:pb-24">
        <div class="relative py-12 w-full h-5/6">
            <div class="bg-gray-700 grid grid-cols-2 grid-rows-3 grid-flow-col gap-8 p-8 rounded-lg h-5/6">
                <div class="col-span-3 flex justify-center items-center text-white text-5xl font-bold h-full">
                    SUB-CATEGORIES
                </div>
                <!-- First container -->
                <form>
                    {viewerObj.addCSRF(FormPurposes.renderMusicPage.value)}
                    <div class="bg-gray-200 rounded-lg">
                        <button class="bg-gray-400 rounded-lg text-center w-full h-full">MUSIC</button>
                    </div>
                </form>

                <form>
                    {viewerObj.addCSRF(FormPurposes.renderQuizLobby.value)}
                    <div class="bg-gray-200 rounded-lg">
                        <button class="bg-gray-400 rounded-lg text-center w-full h-full">QUIZ</button>
                    </div>
                </form>

                <form>
                    {viewerObj.addCSRF(FormPurposes.renderNotesPage.value)}
                    <div class="bg-gray-200 rounded-lg">
                        <button class="bg-gray-400 rounded-lg text-center w-full h-full">NOTES</button>
                    </div>
                </form>

                <form>
                    {viewerObj.addCSRF(FormPurposes.renderContentMarketplacePage.value)}
                    <div class="bg-gray-200 rounded-lg">
                        <button class="bg-gray-400 rounded-lg text-center w-full h-full">MARKETPLACE</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>


    """
    viewerObj.updateHTML(subCategories, "fullPage", DynamicWebsite.UpdateMethods.update)
    renderLogo(viewerObj)


def renderNotesRepository(viewerObj: DynamicWebsite.BaseViewer):
    notesRepository = f"""
    <script>
        function findNote(text)
        {{
            text = document.getElementById("noteSearch").value.toLowerCase();
            
            for (const [key, value] of Object.entries(document.getElementById("notesHolder").children)) 
            {{ 
                if (value.getAttribute("title").toLowerCase().includes(text.toLowerCase()) || value.getAttribute("subject").toLowerCase().includes(text.toLowerCase()))
                {{
                    value.hidden=false;
                }} else {{
                    value.hidden=true;
                }}
            }}
        }}    
        document.getElementById("noteSearch").addEventListener("input", findNote);

    </script>
        <div class="relative flex items-center justify-center h-20 w-full bg-black" aria-label="Global">
            <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
                <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto"></div>
            </div>
            <div class="text-white font-semibold text-3xl flex justify-center">THE ALL IN ONE EDUCATION</div>
            <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
                <div class="p-4 inline-flex rounded-full">   
                    <form>
                        {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
                        <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-9">
                            Log out
                        </button>
                    </form>
                </div>
            </div>
        </div>
        
        
    <!-- component -->
    <div class="text-gray-600 body-font">
    <div id="notesUpload" class="container px-5 py-24 mx-auto"></div>
        <div class="w-full p-6 -mt-4 relative">
            <input type="text" id="noteSearch" placeholder="Search..." class="bg-gray-800 w-full p-5 text-lg border rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"/> 
        </div>
    <div id="notesHolder" class="flex flex-wrap -m-4"></div>
</div>
"""

    viewerObj.updateHTML(notesRepository, "fullPage", DynamicWebsite.UpdateMethods.update)
    renderNotesUploader(viewerObj)
    renderLogo(viewerObj)
    renderAvailableNotes(viewerObj)


def renderAvailableNotes(viewerObj: DynamicWebsite.BaseViewer):
    finalNotes = ""
    for noteObj in SQLconn.execute(f"SELECT NoteID from notes where UserID=\"{liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewerObj.viewerID)}\""):
        noteObjs = SQLconn.execute(f"SELECT NoteID, Subject, Header, Description from note_relevance where NoteID=\"{noteObj['NoteID'].decode()}\" limit 1")
        if noteObjs:
            noteObj = noteObjs[0]
            finalNotes += f"""
                <div id="{noteObj['NoteID'].decode()}" class="p-4 md:w-1/3" title="{noteObj['Header']}" subject="{noteObj['Subject']}">
                    <div class="h-full rounded-xl shadow-cla-blue bg-gradient-to-r from-indigo-50 to-blue-50 overflow-hidden">
                        <img class="lg:h-48 md:h-36 w-full object-cover object-center scale-110 transition-all duration-400 hover:scale-100"
                             src="https://images.unsplash.com/photo-1624628639856-100bf817fd35?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8M2QlMjBpbWFnZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=600&q=60"
                             alt="blog">
                        <div class="p-6">
                            <h2 class="tracking-widest text-xs title-font font-medium text-gray-400 mb-1">{noteObj['Subject']}</h2>
                            <h1 class="title-font text-lg font-medium text-gray-600 mb-3">{noteObj['Header']}</h1>
                            <div class="leading-relaxed mb-3">{noteObj['Description']}</div>
                            <div class="flex items-center flex-wrap">
                                                       
                            <button class="bg-gradient-to-r from-cyan-400 to-blue-400 hover:scale-105 drop-shadow-md shadow-cla-blue px-4 py-1 rounded-lg">
                                <a href="{Routes.cdnFileContent.value}?type={CDNFileType.text.value}&name={noteObj['NoteID'].decode()}.txt" class="text-white">View</a>
                            </button>
                            </div>
                        </div>
                    </div>
                </div>
                """
    viewerObj.updateHTML(finalNotes, "notesHolder", DynamicWebsite.UpdateMethods.update)


def renderNotesUploader(viewerObj: DynamicWebsite.BaseViewer):
    form = f"""
    <form>
        {viewerObj.addCSRF(FormPurposes.submitNote.value)}
        <div class="rounded-lg bg-gray-800 h-full md:px-6 pt-6 pb-6">
            <div class=" bg-gray-800 rounded-md px-6 py-10 w-full mx-auto h-full">
                <h1 class="text-center text-2xl font-bold text-white mb-10">CREATE NOTES HERE</h1>
                <div class="space-y-4">
                    <div>
                        <label for="title" class="text-lx font-serif">Header:</label>
                        <input type="text" placeholder="Header" name="header" class="ml-2 outline-none py-1 px-2 text-md bg-gray-700 rounded-md"/>
                    </div>
                    <div>
                        <label for="description" class="text-lx font-serif">Description:</label>
                        <input type="text" placeholder="Description" name="description" class="ml-2 outline-none py-1 px-2 text-md bg-gray-700 rounded-md"/>
                    </div>
                    <div>
                        <label for="content" class="block mb-2 text-lg font-serif">Content</label>
                        <textarea name="content" cols="30" rows="20" placeholder="Write notes here..." class="w-full font-serif p-4 text-white bg-gray-700 outline-none rounded-md"></textarea>
                    </div>
                    
                    <!-- Dropdown menu -->
                    <select class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" name="subject">
                        <option value="english">English</option>
                        <option value="maths">Maths</option>
                        <option value="science">Science</option>
                    </select>

                    <button type="submit" class=" px-6 py-2 mx-auto block rounded-md text-lg font-semibold text-indigo-100 bg-indigo-600">
                        PUBLISH
                    </button>
                </div>
            </div>
        </div>
    </form>
    """
    viewerObj.updateHTML(form, "notesUpload", DynamicWebsite.UpdateMethods.update)



def renderMusicPage(viewerObj: DynamicWebsite.BaseViewer):
    musicPage = f"""
    
    <div class="relative flex items-center justify-center h-20 w-full bg-black" aria-label="Global">
        <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
            <div id="navLogoButton" class="flex items-center justify-between w-full md:w-auto"></div>
        </div>
        <div class="text-white font-semibold text-3xl flex justify-center mt-3">THE ALL IN ONE EDUCATION PLATFORM</div>
        <div id="musiclayer2" class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
        </div>
    </div>
"""
    viewerObj.updateHTML(musicPage, "fullPage", DynamicWebsite.UpdateMethods.update)
    musicPageL2 = f"""
     <div class="p-4 inline-flex rounded-full">   
        <form>
            {viewerObj.addCSRF(FormPurposes.renderAuthPage.value)}
            <button type="submit" class="text-3xl text-white font-bold inline-flex items-center px-14 py-3 text-2xl text-white bg-gray-800 rounded-full cursor-pointer hover:scale-105 hover:transition duration-300 ease-in-out mt-6">
                Log out
            </button>
        </form>
    </div>
    """
    viewerObj.updateHTML(musicPageL2, "musiclayer2", DynamicWebsite.UpdateMethods.update)

    renderLogo(viewerObj)


def sendRegisterForm(viewerObj:DynamicWebsite.BaseViewer):
    form = f"""<form>
                        {viewerObj.addCSRF(FormPurposes.submitRegister.value)}
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
    viewerObj.updateHTML(form, "registerFormContainer", DynamicWebsite.UpdateMethods.update)


def sendLoginForm(viewerObj:DynamicWebsite.BaseViewer):
    form = f"""<form>
                    {viewerObj.addCSRF(FormPurposes.submitLogin.value)}
                    <input type="text" autocomplete="off"
                           class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           name="username" placeholder="Username">
                    <input autocomplete="off" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 mb-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                           type="password" name="password" placeholder="Password">
                    <button type="submit" class="bg-white text-blue-700 font-bold p-4 w-full rounded">Submit</button>
                </form>"""
    viewerObj.updateHTML(form, "loginFormContainer", DynamicWebsite.UpdateMethods.update)



class MusicStream:
    def __init__(self, fileName, category, onComplete):
        self.onComplete = onComplete
        self.category = category
        self.fileName = fileName
        self.wf = wave.open(self.fileName, 'rb')
        self.currentData = b""
        Thread(target=self.read).start()
        print(f"New Song Started [{category}]: {fileName}")


    def read(self):
        while True:
            self.currentData = self.wf.readframes(self.wf.getframerate()//10)
            if not self.currentData:
                self.onComplete(self.category, self)
                break
            else: sleep(1/10)


    def header(self):
        channels = 2
        bitsPerSample = 16
        sampleRate = self.wf.getframerate()
        datasize = 2000 * 10 ** 6
        o = bytes("RIFF", 'ascii')
        o += (datasize + 36).to_bytes(4, 'little')
        o += bytes("WAVE", 'ascii')
        o += bytes("fmt ", 'ascii')
        o += (16).to_bytes(4, 'little')
        o += (1).to_bytes(2, 'little')
        o += channels.to_bytes(2, 'little')
        o += sampleRate.to_bytes(4, 'little')
        o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')
        o += (channels * bitsPerSample // 8).to_bytes(2, 'little')
        o += bitsPerSample.to_bytes(2, 'little')
        o += bytes("data", 'ascii')
        o += datasize.to_bytes(4, 'little')
        return o


class MusicCollection:
    def __init__(self):
        self.activeStreams:dict[str,MusicStream|None] = {}
        self.musicFiles:dict[str, list[str]] = {"CLASSICAL":[], "JAZZ":[], "AMBIENT":[], "LOFI":[]}
        for cat in self.musicFiles:
            for fileName in os.listdir(f"{folderLocation}/static/audio/{cat}"):
                self.musicFiles[cat].append(f"{folderLocation}\\static\\audio\\{cat}\\{fileName}")
            shuffle(self.musicFiles[cat])
            self.categoryNext(cat, None)


    def categoryNext(self, category:str, stream:MusicStream|None):
        if category not in self.activeStreams: self.activeStreams[category] = None
        if stream: self.musicFiles[category].append(stream.fileName)
        self.activeStreams[category] = MusicStream(self.musicFiles[category].pop(0), category, self.categoryNext)


    def getData(self, category:str):
        if category in self.activeStreams:
            return self.activeStreams[category]


class Player:
    def __init__(self, viewer: DynamicWebsite.BaseViewer|None=None):
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
                    player.viewerObj.updateHTML(str(4 - int(time() - partyTimerStartedAt)), "queueTimer", DynamicWebsite.UpdateMethods.update)
                sleep(1)
        if sum([len(team.players) for team in self.teams]) > 1:
            self.partyComplete()
        else:
            self.timerInitialised = False
            for player in self.userIDToPlayer.values():
                player.viewerObj.updateHTML("Waiting...", "queueTimer", DynamicWebsite.UpdateMethods.update)


    def joinTeam(self, viewer: DynamicWebsite.BaseViewer|None=None):
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


    def leaveTeam(self, viewer: DynamicWebsite.BaseViewer, team:Team|None=None):
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
        self.addedToDB = False
        self.endTime = 0.0

        self.questions: list[Question] = []
        self.questionIndex = -1

    def renderPlayers(self):
        for playerToRenderFor in self.party.userIDToPlayer.values():
            if playerToRenderFor.isHuman:
                for playerToRender in self.party.userIDToPlayer.values():
                    playerDiv = f"""
                            <div class="rounded-lg bg-[#eacfff] mx-4 my-2 flex justify-between items-center">
                                <img class="mx-4 rounded-full border-4 border-white w-28 h-28" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profile_{playerToRender.userName[0].upper()}.png" alt="Extra large avatar">
                                <div class="flex items-center gap-4">
                                    <div class="font-medium dark:text-white">
                                        <div class="text-black text-bold text-xl m-4">Name: {playerToRender.userName}</div>
                                    </div>
                                </div>
                            </div>
                            """
                    if playerToRenderFor.team == playerToRender.team:
                        playerToRenderFor.viewerObj.updateHTML(playerDiv, "selfTeam", DynamicWebsite.UpdateMethods.newDiv)
                    else:
                        playerToRenderFor.viewerObj.updateHTML(playerDiv, "otherTeam", DynamicWebsite.UpdateMethods.newDiv)

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
            player.viewerObj.updateHTML(currentQuestion.questionStatement, "questionText", DynamicWebsite.UpdateMethods.update)
            options = ""
            for optionIndex in range(4):
                options+= f"""
                <form>
                {player.viewerObj.addCSRF(FormPurposes.submitQuizOption.value)}
                <input type="hidden" name="party" value="{self.party.partyID}">
                <input type="hidden" name="option" value="{optionIndex}">
                <button class="rounded-lg bg-gradient-to-r from-purple-500 to-violet-700 flex items-center justify-center h-full w-full hover: font-bold hover:scale-105 hover:transition duration-300 ease-in-out ">
                    <div class="text-white font-bold text-2xl">{currentQuestion.teamOptions[player.team.teamID][optionIndex]}</div>
                </button>
            </form>"""
            player.viewerObj.updateHTML(options, "options", DynamicWebsite.UpdateMethods.update)
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

    def receiveUserInput(self, isHuman: bool, viewer: DynamicWebsite.BaseViewer|Player, optionIndex):
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
                player.viewerObj.updateHTML(options, "options", DynamicWebsite.UpdateMethods.update)
            if len(currentQuestion.optionsPressed) == len(self.party.userIDToPlayer):
                self.updateTeamHealth(player.team, -5)
                sleep(1)
                self.endCurrentQuestion()

    def sendPostQuizQuestion(self, viewer: DynamicWebsite.BaseViewer, questionIndex):
        userID = liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewer.viewerID)
        if userID not in self.party.userIDToPlayer: return
        questionIndex = int(questionIndex)
        postQuestion = f"""<div class="rounded-lg px-2 mx-6 bg-[#eacfff] text-green font-bold text-2xl p-4">
                <div class="text-black font-bold text-2xl h-1/3 p-4 m-4">{self.questions[questionIndex].questionStatement}{self.questions[questionIndex].correctAnswers[0]}</div>
            </div>"""
        viewer.updateHTML(postQuestion, "postQuiz", DynamicWebsite.UpdateMethods.update)
        self.sendPostQuizQuestionList(viewer)

    def sendPostQuizQuestionList(self, viewer:DynamicWebsite.BaseViewer):
        questionList = """<ul class="grid grid-cols-1 gap-2 w-full h-full p-4">"""
        for questionIndex in range(0, self.questionIndex + 1):
            questionList += f"""
                                <li>
                                    <form>
                                        {viewer.addCSRF(FormPurposes.renderPostQuizQuestion.value)}
                                        <input type="hidden" name="party" value="{self.party.partyID}">
                                        <input type="hidden" name="question" value="{questionIndex}">
                                        <button class="rounded-lg hover:scale-105 hover:text-white hover:transition duration-300 ease-in-out bg-gradient-to-r from-purple-500 to-violet-700 text-dark font-bold py-2 px-4 h-full w-full active:bg-blue-700" onclick="this.classList.toggle('bg-blue-400')">{questionIndex+1}</button>
                                    </form>
                                </li>
                                """
        questionList += "</ul>"
        viewer.updateHTML(questionList, "postQuizQuestionList", DynamicWebsite.UpdateMethods.update)

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
                player.viewerObj.updateHTML(bar, f"selfTeamHealthBar", DynamicWebsite.UpdateMethods.update)
                player.viewerObj.updateHTML(str(teamChanged.health), f"selfTeamHealthText", DynamicWebsite.UpdateMethods.update)
            else:
                player.viewerObj.updateHTML(bar, f"otherTeamHealthBar", DynamicWebsite.UpdateMethods.update)
                player.viewerObj.updateHTML(str(teamChanged.health), f"otherTeamHealthText", DynamicWebsite.UpdateMethods.update)

        if teamChanged.health == 0:
            self.saveToDB()
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
                                <img class="mr-4 rounded-full w-16 h-16" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profile_{player.userName[0].upper()}.png" alt="Extra large avatar">
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
                        player.viewerObj.updateHTML("DEFEAT", "resultTextDiv", DynamicWebsite.UpdateMethods.update)
                    else:
                        player.viewerObj.updateHTML("VICTORY", "resultTextDiv", DynamicWebsite.UpdateMethods.update)
                    player.viewerObj.updateHTML(leaderboardDiv, "quizLeaderboard", DynamicWebsite.UpdateMethods.update)

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
        if self.addedToDB: return
        self.addedToDB = True
        playerData = {}
        teamData = []
        for team in self.party.teams:
            teamData.append(team.teamID)
        for player in self.party.userIDToPlayer.values():
            playerData[player.userID] = {"Team":player.team.teamID,"Score":player.score}
        SQLconn.execute(f"INSERT INTO quiz values (\"{self.matchID}\", NOW(), {self.party.teams[0].score}, {self.party.teams[1].score}, '{dumps(teamData)}', '{dumps(playerData)}')")


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
            # if value in self.activeUserIDs: return self.activeUserIDs[value]["USERNAME"]
            received = SQLconn.execute(f"SELECT UserName from user_auth where UserID=\"{value}\" limit 1")
            if received:
                received = received[0]
                return received.get("UserName")
        elif By == self.ByViewerID:
            # if value in self.viewerIDToUserID:
            #     userID = self.viewerIDToUserID[value]
            #     return self.getUserName(self.ByUserID, userID)
            received = SQLconn.execute(f"SELECT UserID from user_devices where ViewerID=\"{value}\" limit 1")
            if received:
                received = received[0]
                return self.getUserName(self.ByUserID, received.get("UserID").decode())

    def getUserID(self, By, value):
        if not value: return
        if By == self.ByUserName:
            # if value in self.usernameToUserID:
            #     return self.usernameToUserID[value]
            received = SQLconn.execute(f"SELECT UserID from user_auth where UserName=\"{value}\" limit 1")
            if received:
                received = received[0]
                return received.get("UserID").decode()
        elif By == self.ByViewerID:
            # if value in self.viewerIDToUserID:
            #     return self.viewerIDToUserID[value]
            received = SQLconn.execute(f"SELECT UserID from user_devices where ViewerID=\"{value}\" limit 1")
            if received:
                received = received[0]
                return received.get("UserID").decode()

    def getParty(self, By, value):
        pass

    def loginCall(self, viewer: DynamicWebsite.BaseViewer, userID):
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
            if received["UserID"].decode() != userID or received["RemoteAddr"] != viewer.cookie.remoteAddress or received["UserAgent"] != viewer.cookie.userAgent or received["HostURL"] != viewer.cookie.hostURL:
                SQLconn.execute(f"DELETE from user_devices WHERE ViewerID=\"{viewer.viewerID}\"")
                addEntry = True
        else: addEntry = True
        if addEntry:
            SQLconn.execute(f"INSERT INTO user_devices values (\"{viewer.viewerID}\", \"{userID}\", \"{viewer.cookie.remoteAddress}\", \"{viewer.cookie.userAgent}\", \"{viewer.cookie.hostURL}\")")

    def logoutCall(self, viewer: DynamicWebsite.BaseViewer, logout: bool = False):
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
    def getKnownLoggedInUserID(viewer: DynamicWebsite.BaseViewer):
        remoteAddr = viewer.cookie.remoteAddress
        userAgent = viewer.cookie.userAgent
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


def registerUser(viewerObj:DynamicWebsite.BaseViewer, form:dict):
    username = form.get("username", "")
    email = form.get("email", "")
    password = form.get("password", "")
    confirm_password = form.get("confirm_password", "")
    name = form.get("name", "")
    age = form.get("age", 0)
    try: age=int(age)
    except:
        viewerObj.updateHTML("Invalid Age", "registrationWarning", DynamicWebsite.UpdateMethods.update)
        sendRegisterForm(viewerObj)
    if not username:
        viewerObj.updateHTML("Invalid Username", "registrationWarning", DynamicWebsite.UpdateMethods.update)
        sendRegisterForm(viewerObj)
    elif SQLconn.execute(f"SELECT UserName from user_auth where UserName=\"{username}\" limit 1"):
        viewerObj.updateHTML("Username Taken", "registrationWarning", DynamicWebsite.UpdateMethods.update)
        sendRegisterForm(viewerObj)
    elif email.count("@")!=1 or email.split("@")[1].count(".")!=1 or not email.split("@")[1].split(".")[0] or not email.split("@")[1].split(".")[1]:
        viewerObj.updateHTML("Email not valid", "registrationWarning", DynamicWebsite.UpdateMethods.update)
        sendRegisterForm(viewerObj)
    elif password == "" or len(password)<8:
        viewerObj.updateHTML("Passwords Not Valid", "registrationWarning", DynamicWebsite.UpdateMethods.update)
        sendRegisterForm(viewerObj)
    elif password!=confirm_password:
        viewerObj.updateHTML("Passwords Dont match", "registrationWarning", DynamicWebsite.UpdateMethods.update)
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

def loginUser(viewerObj:DynamicWebsite.BaseViewer, form:dict):
    username = form.get("username", "")
    password = form.get("password", "")
    received = SQLconn.execute(f"SELECT UserID, PWHash from user_auth where UserName=\"{username}\" limit 1")
    if not received:
        viewerObj.updateHTML("Username Dont Match", "loginWarning", DynamicWebsite.UpdateMethods.update)
        sendLoginForm(viewerObj)
    else:
        received = received[0]
        if not check_password_hash(received["PWHash"].decode(), password):
            viewerObj.updateHTML("Password Dont Match", "loginWarning", DynamicWebsite.UpdateMethods.update)
            sendLoginForm(viewerObj)
        else:
            liveCacheManager.loginCall(viewerObj, received["UserID"].decode())
            renderHomepage(viewerObj)


def publishNote(viewerObj:DynamicWebsite.BaseViewer, form:dict):
    while True:
        noteID = StringGenerator().AlphaNumeric(50,50)
        if not SQLconn.execute(f"SELECT NoteID from notes where NoteID=\"{noteID}\" limit 1"):
            SQLconn.execute(f"INSERT INTO notes values (\"{noteID}\", \"{liveCacheManager.getUserID(liveCacheManager.ByViewerID, viewerObj.viewerID)}\")")
            SQLconn.execute(f"INSERT INTO note_relevance values (\"{noteID}\", \"{form['subject']}\", \"{form['header']}\", \"{form['description']}\")")
            open(f"{folderLocation}\\static\\text\\{noteID}.txt", "wb").write(form['content'].encode())
            break

def formSubmitCallback(viewerObj: DynamicWebsite.BaseViewer, form: dict):
    if form is not None:
        purpose = form.pop("PURPOSE")
        print(liveCacheManager.getUserName(liveCacheManager.ByViewerID, viewerObj.viewerID), purpose, form)

        if purpose == FormPurposes.submitRegister.value:
            registerUser(viewerObj, form)

        elif purpose == FormPurposes.submitLogin.value:
            loginUser(viewerObj, form)

        elif purpose == FormPurposes.startQuiz.value:
            for party in liveCacheManager.activeParties.values():
                if party.joinTeam(viewerObj): return
            newParty = Party(2, 6)
            newParty.joinTeam(viewerObj)

        elif purpose == FormPurposes.submitQuizOption.value:
            partyID = form.pop("party", "")
            party = liveCacheManager.activeParties.get(partyID, None)
            if party: party.gameObj.receiveUserInput(True, viewerObj, form["option"])

        elif purpose == FormPurposes.renderAuthPage.value:
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
                <img class="rounded-full w-48 h-48 mb-4" src="{Routes.cdnFileContent.value}?type={CDNFileType.image.value}&name=profile_{liveCacheManager.getUserName(liveCacheManager.ByViewerID, viewerObj.viewerID)[0].upper()}.png" alt="Extra large avatar">
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
            viewerObj.updateHTML(players, "quizLobbyDiv", DynamicWebsite.UpdateMethods.update)

        elif purpose == FormPurposes.renderPostQuizQuestion.value:
            partyID = form.pop("party", "")
            party = liveCacheManager.activeParties.get(partyID, None)
            if party: party.gameObj.sendPostQuizQuestion(viewerObj, form["question"])

        elif purpose == FormPurposes.renderSubCategories.value:
            renderSubCategories(viewerObj)

        elif purpose == FormPurposes.renderContentMarketplacePage.value:
            renderContentMarketPlace(viewerObj)

        elif purpose == FormPurposes.renderMusicPage.value:
            renderMusicPage(viewerObj)

        elif purpose == FormPurposes.renderNotesPage.value:
            renderNotesRepository(viewerObj)
            renderNotesUploader(viewerObj)
            renderAvailableNotes(viewerObj)

        elif purpose == FormPurposes.submitNote.value:
            publishNote(viewerObj, form)
            renderNotesUploader(viewerObj)
            renderAvailableNotes(viewerObj)



def newVisitorCallback(viewerObj: DynamicWebsite.BaseViewer):
    print("Visitor Joined: ", viewerObj.viewerID)

    initial = "<div id=\"fullPage\"></div>"
    viewerObj.updateHTML(initial, "mainDiv", DynamicWebsite.UpdateMethods.update)
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
    # renderContentMarketPlace(viewerObj)
    # renderSubCategories(viewerObj)
    #renderNotesRepository(viewerObj)
    # renderMusicPage(viewerObj)

def visitorLeftCallback(viewerObj: DynamicWebsite.BaseViewer):
    liveCacheManager.logoutCall(viewerObj)
    print("Visitor Left: ", viewerObj.viewerID)


logger = LogManager()
SQLconn = connectDB(logger)
liveCacheManager = UserCache()

extraHeads = f"""
<script src="https://cdn.tailwindcss.com"></script>
<script>
    function changeMusic(category)
    {{
        if (document.getElementById("musicPlayer").children[0].src.includes("/music/"+category) && document.getElementById("musicPlayer").muted==false)
        {{ 
            document.getElementById("musicPlayer").muted = true;
        }} else {{
            document.getElementById("musicPlayer").children[0].src = "/music/"+category; 
            document.getElementById("musicPlayer").load();
            document.getElementById("musicPlayer").play();
        }}
        
    }}
</script>"""

bodyBase = """
<body style="background-color: #000000;"> 
<audio id="musicPlayer" preload="none"> <source src="" type="audio/x-wav;codec=pcm"> </audio>
<div id="mainDiv"><div>
</body>"""


#musicCollection = MusicCollection()
dynamicWebsiteApp = DynamicWebsite(newVisitorCallback, visitorLeftCallback, formSubmitCallback, None, ServerSecrets.webFernetKey.value,
                                   CoreValues.appName.value,  Routes.webHomePage.value, extraHeads, bodyBase, CoreValues.title.value)
baseApp = dynamicWebsiteApp.start()


@baseApp.get(Routes.cdnFileContent.value)
def _fileContent():
    fileType = request.args.get("type", "").strip()
    fileName = request.args.get("name", "").strip()
    if fileType == CDNFileType.text.value:
         return send_from_directory(folderLocation+"/static/text", fileName, as_attachment=True)
    elif fileType == CDNFileType.font.value:
         return send_from_directory(folderLocation+"/static/font", fileName, as_attachment=True)
    elif fileType == CDNFileType.image.value:
        return send_from_directory(folderLocation + "/static/image", fileName, as_attachment=True)
    elif fileType == CDNFileType.video.value:
        return send_from_directory(folderLocation + "/static/video", fileName, as_attachment=True)
    elif fileType == CDNFileType.html.value:
        return send_from_directory(folderLocation + "/static/html", fileName, as_attachment=True)
    elif fileType == CDNFileType.css.value:
        return send_from_directory(folderLocation + "/static/css", fileName, as_attachment=True)
    elif fileType == CDNFileType.js.value:
        return send_from_directory(folderLocation + "/static/js", fileName, as_attachment=True)
    return ""


@baseApp.get("/favicon.ico")
def _favicon():
    return send_from_directory(folderLocation+"/static/image", "favicon.png", as_attachment=True)


@baseApp.route('/music/<streamCategory>')
def audio(streamCategory):
    def sound(streamCategory):
        if streamCategory not in musicCollection.activeStreams: return print("Invalid stream category")
        first_run = True

        while True:
            current = musicCollection.getData(streamCategory)
            if first_run:
                data = current.header()+current.currentData
                first_run = False
            else:
                sleep(1/10)
                data = current.currentData
            yield data
    return Response(sound(streamCategory))



try:
    open(r"C:\cert\privkey.pem", "r").close()
    print(f"https://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
    WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None, keyfile=r'C:\cert\privkey.pem', certfile=r'C:\cert\cert.pem').serve_forever()
except:
    print(f"http://127.0.0.1:{ServerSecrets.webPort.value}{Routes.webHomePage.value}")
    WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), baseApp, log=None).serve_forever()

