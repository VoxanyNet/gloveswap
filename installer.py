import shutil
import wget
import PySimpleGUIQt as gui
import os
import sys
import shutil
from swinlnk.swinlnk import SWinLnk

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
    install_location = f"{user_path}/AppData/Local"
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
        open(f"{install_location}\\GloveSwap")

        # Download and extract application and assets
        wget.download("http://cdn.vxny.net/gloveswap/downloads/application/gloveswap.zip",out=install_location)
        shutil.unpack_archive(f"{install_location}/GloveSwap/gloveswap.zip", f"{install_location}/GloveSwap")

        # Creates dekstop icon
        swl = SWinLnk()
        swl.create_lnk(f"{install_location}/GloveSwap/gloveswap.exe", f"{user_path}/Desktop")

    if event == "-EXIT-":
        sys.exit()