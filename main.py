import PySimpleGUIQt as gui
import shutil
import os
import webbrowser as web
import random
import json

def duplicate(filepath):
    global dneFileName
    global customFileName
    global customFile
    #global dneExists
    if "items_game.txt" in filepath and "scripts" in filepath:
        target = filepath.replace("items_game.txt","items_game_DNE.txt")
        shutil.copyfile(filepath,target)
        dneFileName = target
        customFileName = filepath
        customFile = open(customFileName,"r+")
        return True
    else:
        window["Errors"].update("Error: This doesn't appear to be the right file :(  . Check your file path before continuing.")


def swapgloves(glove1style,glove1finish,glove2style,glove2finish):
    global styleIDS
    global customFileName
    global finishIDS
    customFile = open(customFileName,"r")
    glove1styleline = 0
    glove2styleline = 0
    glove1finishline = 0
    glove2finishline = 0
    lines = customFile.readlines()
    for line in lines:
        if line == ('\t\t"'+ str(styleIDS[glove1style])+'"\n') and glove1styleline == 0:
            glove1styleline = lines.index(line)
            print("The line for " + glove1style + " is line " + str(glove1styleline))
        if line == ('\t\t"'+ str(finishIDS[glove1finish])+'"\n') and glove1finishline == 0:
            glove1finishline = lines.index(line)
            print("The line for " + glove1finish + " is line " + str(glove1finishline))
        if line == ('\t\t"'+ str(styleIDS[glove2style])+'"\n') and glove2styleline == 0:
            glove2styleline = lines.index(line)
            print("The line for " + glove2style + " is line " + str(glove2styleline))
        if line == ('\t\t"'+ str(finishIDS[glove2finish])+'"\n') and glove2finishline == 0:
            glove2finishline = lines.index(line)
            print("The line for " + glove2finish + " is line " + str(glove2finishline))
    #SWAP THE POSITIONS
    lines[glove1styleline],lines[glove2styleline] = lines[glove2styleline],lines[glove1styleline]
    lines[glove1finishline],lines[glove2finishline] = lines[glove2finishline],lines[glove1finishline]
    print("Files Swapped")
    return(lines)

gui.theme("SystemDefault1")

# Loads glove IDs etc.
data_file = open("data.json","r")
data = json.load(data_file)

gloves = data["gloves"]
styleIDS = data["styleIDS"]
finishIDS = data["finishIDS"]

# Tries to find items_game.txt directory
program_data_path = os.getenv("PROGRAMFILES(X86)")
if os.path.exists(f"{program_data}/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/scripts/items"):
    print("Found an existing")

dneFileName = ""
customFileName = ""
dneExists = False

# Old layout
layout = [
            [gui.Image("assets/title.png")],
            [gui.Text("Please enter path to items_game.txt located at: Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\scripts\\items  in the drive containing your CS:GO files", key = "filepath_location")],
            [gui.Text("Step 1. Enter file path for items_game.txt",key = "step1text"),gui.Input(enable_events=True, key="filepath",default_text=default_file_path), gui.FileBrowse(key="browsebutton")],
            [gui.Text("Step 2. Duplicate items_game.txt",key="step2text"), gui.Button("Create editable file",key="duplicatefile")],
            [gui.Text("Step 3. Choose Items to Swap",key="step3text")],
            [gui.Text("Style: Replace "),gui.Combo(["Bloodhound","Broken Fang","Driver","Hand Wraps","Hydra","Moto","Specialist","Sport"],key = "style1",enable_events = True, readonly=True,tooltip = "Choose the glove that you have in game",default_value = "Choose Glove Type"),gui.Text(" With "),gui.Combo(["Bloodhound","Broken Fang","Driver","Hand Wraps","Hydra","Moto","Specialist","Sport"],key = "style2",enable_events = True,readonly = True,tooltip = "Choose the glove you WISH you had in game",default_value = "Choose Glove Type")],
            [gui.Text("Finish: Replace "),gui.Combo(["Bronzed"],key = "finish1",enable_events = True, readonly=True,tooltip = "Choose the glove that you have in game"),gui.Text(" With "),gui.Combo(["Bronzed"],key = "finish2",enable_events = True,readonly = True,tooltip = "Choose the glove you WISH you had in game")],
            [gui.Text("Step 4. SWAP ITEMS",key="step4text"), gui.Button("SWAP DATA", key = "swap",disabled  =True, tooltip = "Make sure to complete steps 1-3 First.")],
            [gui.Text("Step 5. Launch CS:GO"), gui.Button("Launch CS:GO", key = "launch")],
            [gui.Text("")],
            [gui.Text("")],
            [gui.Text("Status: "),gui.Text("CS:GO Files Unedited", key="filestatus"), gui.Button("UNDO CHANGES",key="undo",disabled = True)],
            [gui.Text("", key = "Errors", text_color = "#FF0000")],
            [gui.Button("Join my Discord!", key = "discord"),gui.Button("Support me on patreon!", key = "patreon"),gui.Button("View all gloves", key = "csgostash"),gui.Button("HELP", key = "help")]

        ]

# Defines the layout
layout = [
    [gui.Text("GloveSwap",justification = "center",font = ("Trebuchet MS",30,"bold"))],
    [gui.HorizontalSeparator()],
    []
]

# Creates the window
window = gui.Window('GloveSwap for CS:GO Workshop', layout, icon="assets/icon.ico")

while True:
    event, values = window.read()

    path = values["filepath"]
    window["Errors"].update("", text_color = "#FF0000")

    # Checks events

    #Update glove updatechoice
    if event == "style1":
        window["finish1"].update(values=gloves[values["style1"]])
    if event == "style2":
        window["finish2"].update(values=gloves[values["style2"]])


    if event == "swap":
        window["Errors"].update("Swapping " + str(values["style1"]) + " "+ str(values["finish1"]) + " with " + str(values["style2"]) + " " + str(values["finish2"]))
        newlistoflines = swapgloves(values["style1"],values["finish1"],values["style2"],values["finish2"])
        customFile.close()
        os.remove(customFileName)
        customFile = open(customFileName,"w")
        for line in (newlistoflines):
            customFile.write(line)
        customFile.close()
        window["Errors"].update("Successfully swapped  " + str(values["style1"]) + " "+ str(values["finish1"]) + " with " + str(values["style2"]) + " " + str(values["finish2"]), text_color = "#00FFFF")


    if event == "duplicatefile":
        if duplicate(path) == True:
            window["duplicatefile"].update(disabled = True)
            window["filepath"].update(disabled = True)
            window["browsebutton"].update(disabled = True)
            window["swap"].update(disabled = False)
            window["filestatus"].update("Custom items_game.txt file active. Do not play on official CS:GO Servers.")
            window["undo"].update(disabled = False)
            window["Errors"].update("Success! You may now use the swap tool to edit items_game.txt, or edit manually. DO NOT edit or remove items_game_DNE.txt manually.", text_color = "#00FFFF")
            window["step2text"].update(text_color = "#11FF33")



    if event == "undo":
        window["undo"].update(disabled = True)
        os.remove(customFileName)
        shutil.copyfile(dneFileName,customFileName)
        window["duplicatefile"].update(disabled = False)
        window["filepath"].update(disabled = False)
        window["browsebutton"].update(disabled = False)
        window["filestatus"].update("CS:GO Files Unedited")
        window["Errors"].update("Your CS:GO Files have been reset. You should now be able to play on official CS:GO servers.", text_color = "#00FFFF")
        window["swap"].update(disabled = True)
        window["step2text"].update(text_color = "#FF0000")


    if event == "launch":
        web.open("steam://rungameid/730")
    if event == "discord":
        web.open("https://discord.gg/Nv49S9Ja5A")
    if event == "patreon":
        web.open("https://www.patreon.com/bonzane1")
    if event == "help":
        web.open("https://www.gloveswap.net/help")
    if event == "csgostash":
        web.open("https://csgostash.com/gloves")




    # Checks values
    if path != "":
        #layout.append([gui.Text("items_game.txt is locted at: " + str(path)])
        window["filepath_location"].update("Path to items_game.txt: " + path)
        window["step1text"].update(text_color = "#11FF33")
    else:
        window["filepath_location"].update("Please enter path to items_game.txt located at: Steam\steamapps\common\Counter-Strike Global Offensive\csgo\scripts\items in the drive containing your CS:GO files")
        window["step1text"].update(text_color = "#FF0000")


    if event == gui.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

window.close()
