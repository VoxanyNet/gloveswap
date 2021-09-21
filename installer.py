import shutil
import wget
import PySimpleGUIQt as gui
import os
import sys
import shutil
from pycrosskit import shortcuts
import threading
import zipfile
import asyncio

async def install(install_location,user_path):
    try:
        os.mkdir(f"{install_location}/GloveSwap")
    except FileExistsError:
        pass

    # Download and extract application and assets
    wget.download("https://www.dropbox.com/s/fv500qn6ip4kyv8/application.zip?dl=1")

    with zipfile.ZipFile("application.zip", 'r') as zip_ref:
        zip_ref.extractall("GloveSwap")

    os.remove("application.zip")

    # Creates dekstop icon
    short = shortcuts.Shortcut("GloveSwap", f"{install_location}\\GloveSwap\\main.exe", desktop = True)

    return True

# Sets theme to something not ugly
gui.theme("default1")

# Sets the default install location
user_path = f"{os.getenv('USERPROFILE')}"

if os.getenv(user_path) == False:
    install_location = ""
    # We need to set the initial status for the directory as we are unable
    # to evaluate the validity of path until the user does something.
    status_element = gui.Text("Directory does not exist!",text_color = "red", font = ('Segoe UI',10), key = "-DIRECTORY_STATUS-")
    button_disabled = True

else:
    install_location = f"{user_path}\\AppData\\Roaming"
    status_element = gui.Text("Valid directory",text_color = "green", font = ('Segoe UI',10), key = "-DIRECTORY_STATUS-")
    button_disabled = False

layout = [
    [gui.Text("GloveSwap Installer",font = ("Segoe UI",25,"bold"))],
    [gui.Text("")],
    [gui.Input(default_text = install_location, key = "-DIRECTORY_INPUT-", size = (35,1), font = ('Segoe UI',10),enable_events=True),gui.FolderBrowse("Browse", size = (10,1), font = ('Segoe UI',10), initial_folder = os.getenv("USERPROFILE"))],
    [status_element],
    [gui.Text("")],
    [gui.Text("")],
    [gui.Button("Exit", key = "-EXIT-", size = (10,1), font = ('Segoe UI',10)),gui.Button("Install", key = "-INSTALL-", size = (10,1), font = ('Segoe UI',10),disabled = button_disabled)],
]

window = gui.Window("GloveSwap Installer", layout, icon="assets/icon.ico")

while True:
    event, values = window.read()

    if event == "-DIRECTORY_INPUT-":

        install_location = values["-DIRECTORY_INPUT-"]

        # Checks if the file exists, and updates elements accordingly
        if os.path.exists(install_location):
            window["-DIRECTORY_STATUS-"].update("Valid Directory",text_color = "green")
            window["-INSTALL-"].update(disabled = False)
        else:
            window["-DIRECTORY_STATUS-"].update("Directory does not exist!",text_color = "red")
            window["-INSTALL-"].update(disabled = True)

    if event == "-INSTALL-":
        return_value = asyncio.run(install(install_location,user_path))
        #thread = threading.Thread(target = install, args = (install_location,user_path))
        #thread.start()
        print(return_value)
    if event == "-EXIT-":
        sys.exit()
