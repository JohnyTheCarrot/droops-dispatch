import re, os, sys, subprocess
import requests, json, copy, platform

import dispatch_config
# Having long single-line imports freaks some version of Python out

version = 108
firstcommand = ""

def AskConsent(text="Confirm"):
    confirmation = input(f"{text} (Y/N): ")
    validated = re.match(r'([yYnN])', confirmation)
    if validated:
        return re.match(r'[yY]', confirmation)
    else:
        return False

def CheckUpdate():
    url = "https://raw.githubusercontent.com/JohnyTheCarrot/droops-dispatch/canary/version.txt"
    headers = {
        'User-Agent': f"Droop's Dispatch Updater ({dispatch_config.user_agent}, v1.0.0)",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers)
    if int(response.text) > version:
        print("")
        print("==============================================================")
        print(f"You're running {int(response.text) - version} versions behind! Run \"runupdate\" to update.")
        print("==============================================================")
        print("")
    else:
        print("You're up to date, great! :)\n")

def RunUpdate():
    print(f"\nWARNING: Running this command WILL override the {os.path.basename(__file__)} file!")
    print(f"If you have not made any changes to the {os.path.basename(__file__)} script you can ignore this warning.")
    print("Are you sure you want to continue?\n")
    if AskConsent():
        url = "https://raw.githubusercontent.com/JohnyTheCarrot/droops-dispatch/canary/dispatch.py"
        headers = {
            'User-Agent': f"Droop's Dispatch Updater ({dispatch_config.user_agent}, v1.0.0)",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers)
        f = open(os.path.basename(__file__), "w")
        f.write(response.text)
        f.close()
        input("Done. Press enter to continue.")
        Restart()
    else:
        print("Canceled update.")

if dispatch_config.enable_splash:
    if dispatch_config.custom_splash:
        f = open(dispatch_config.custom_splash_file_path, 'r')
        print(f.read())
        print("\n")
    else:
        url = "https://watchanimeattheoffice.com/humans.txt"
        headers = {
            'User-Agent': f"DiscordBot ({dispatch_config.user_agent}, v1.0.0)",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)

CheckUpdate()

def HasField(variable: str):
    obj = dispatch_config.webhook_payload
    try:
        for embed in obj["embeds"]:
            for field in embed["fields"]:
                if variable in field["value"]:
                    return True
        return False
    except KeyError:
        return False

def HasImageVariable():
    obj = dispatch_config.webhook_payload
    try:
        for embed in obj["embeds"]:
            if '[IMAGE]' in embed["image"]['url']:
                return True
            if '[IMAGE]' in embed["thumbnail"]['url']:
                return True
        return False
    except KeyError:
        return False

def PushUpdate(branch_id = dispatch_config.default_branch):
    if AskConsent():
        confirmation = input("Fire webhook? (Y/N): ") if dispatch_config.webhook_url is not None and (HasField("[DEVELOPER]") or HasField("[NOTES]"))  else 'n'
        validated = re.match(r'([yYnN])', confirmation)
        if validated and re.match(r'[yY]', confirmation):
            note = input("Note: ") if HasField("[NOTES]") else 'None'
            if note == 'None':
                pass
            elif not note:
                print("Please add a note")
                return
            developer = input("Developer Tag (username#discrim): ") if HasField("[DEVELOPER]") else 'None'
            if developer == 'None':
                pass
            elif not developer:
                print("Please identify yourself")
                return
            image = input("Image URL: ") if HasImageVariable() else 'None'
            if image == 'None':
                pass
            elif not image:
                print("Please provide an image URL.")
                return
            if (note != 'None' or developer != 'None' or image != 'None') and AskConsent():
                print("success")
                FireWebhook(developer, note, image)
            else:
                return
        else:
            if AskConsent():
                print("Pushing silent update.")
            else:
                print("Update canceled.")
                return
        subprocess.call(["dispatch", "build", "push", branch_id, dispatch_config.dispatch_config_file, dispatch_config.game_path])
    else:
        print("Update canceled.")

def DRMWrap():
    print("This action is destructive and overwrites the executable. Make sure you've got a backup handy if needed!")
    if AskConsent(text="Continue?"):
        subprocess.call(["dispatch", "build", "drm-wrap", dispatch_config.app_id, dispatch_config.game_path])
    else: print("Cancelled DRM-wrap.")

def ListBranches():
    subprocess.call(["dispatch", "branch", "list", dispatch_config.app_id])

def ListBuilds(branch_id: int):
    subprocess.call(["dispatch", "build", "list", dispatch_config.app_id, branch_id])

def PublishBuild(branch_id: int, build_id: int):
    subprocess.call(["dispatch", "build", "publish", dispatch_config.app_id, branch_id, build_id])

def DeleteBranch(branch_id: int):
    if AskConsent():
        subprocess.call(["dispatch", "branch", "delete", dispatch_config.app_id, branch_id])
    else: print("Cancelled branch delete.")

def Login():
    subprocess.call(["dispatch", "login"])

def Clear():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")

def Restart():
    Clear()
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.execv(sys.executable, [sys.executable, os.path.join(sys.path[0], __file__)] + sys.argv[1:])
    elif platform.system() == "Windows":
        os.execv(sys.executable, [sys.executable, "\"" + os.path.join(sys.path[0], __file__) + "\""] + sys.argv[1:])

def UpdateDispatch():
    subprocess.call(["dispatch", "update"])

def DispatchVersion():
    subprocess.call(["dispatch", "-V"])
    print("Use 'update-d' to update Dispatch.")

def FireWebhook(developer: str, notes: str, image: str):

    #webhook url
    url = dispatch_config.webhook_url

    payload = copy.deepcopy(dispatch_config.webhook_payload)
    for embed in payload["embeds"]:
        for field in embed["fields"]:
            if "[DEVELOPER]" in field["value"]:
                field["value"] = field["value"].replace("[DEVELOPER]", developer)
            if "[NOTES]" in field["value"]:
                field["value"] = field["value"].replace("[NOTES]", notes)
        try:
            if "[IMAGE]" in embed["image"]["url"]:
                embed["image"]["url"] = image
            if "[IMAGE]" in embed["thumbnail"]["url"]:
                embed["image"]["url"] = image
        except KeyError:
            pass

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print(f"Server response: {response.text}")

def Command():
    global firstcommand
    try:
        # Check if argument has been passed from initial run
        if not firstcommand:
            command = input("DISPATCH >: ")
        else:
            command = firstcommand
            firstcommand = ""
    except KeyboardInterrupt:
        print("Bye.")
        return
    except EOFError:
        print("Bye.")
        return
    args = command.split(' ')
    args.remove(args[0])
    if command == "login":
        Login()
    elif command == "exit":
        print("Bye.")
        exit(0)
    elif command.startswith("update", 0):
        if len(args) == 1:
            PushUpdate(args[0])
        else:
            print("Please specify a branch ID.")
    elif command == "drm-wrap":
        DRMWrap()
    elif command == "branch delete":
        DeleteBranch(args[0])
    elif command == "clear" or command == "cls":
        Clear()
    elif command == "branch list":
        ListBranches()
    elif command == "restart":
        Restart()
    elif command == "checkupdate":
        CheckUpdate()
    elif command == "runupdate":
        print("Updating..")
        RunUpdate()
    elif command.startswith("build", 0):
        if args[0] == "list":
            if len(args) < 2:
                print("Please provide a branch ID.")
            else:
                ListBuilds(args[1])
        elif args[0] == "publish":
            if len(args) < 3:
                print("Please provide a branch ID & build ID in their respective orders.")
            else:
                PublishBuild(args[1], args[2])
        else:
            print("Unknown subcommand.")
    elif command == "version-d":
        DispatchVersion()
    elif command == "update-d":
        UpdateDispatch()
    elif command == "help":
        print("\n"+("="*120))
        print("Help:")
        print("login                                    - Opens browser to authenticate Discord Dispatch.")
        print("update <branch_id>                       - Starts updating process.")
        print("build publish <branch_id> <build_id>     - Publishes uploaded update. Note that you can only publish updates that were updated for that branch ID.")
        print("build list <branch_id>                   - Lists builds for the specified branch.")
        print("branch delete <branch_id>                - Deletes a branch")
        print("branch list                              - Lists branches for SKU.")
        print("checkupdate                              - Checks for a new update.")
        print("drm-wrap                                 - DRM wraps executable specified in the config.")
        print("restart                                  - Restarts the client. Required after updating config or source code.")
        print("clear/cls                                - Clears the console.")
        print("runupdate                                - Will start the update process.")
        print("update-d                                 - Updates Discord Dispatch.")
        print("version-d                                - Prints Discord Dispatch version.")
        print("exit                                     - Exits the client.")
        print("="*120)
        print("If you found a bug you need fixed, feel free to open up an issue on my GitHub, or to push out a fix yourself.\n")
    else:
        print("Unknown command.")
    if command != "exit":
        Command()

print('Use command "exit" to exit and "help" for help.')
# Check if additional arugments have been passed
if len(sys.argv) != 1:
    firstcommand = " ".join(sys.argv[1:])
    print("DISPATCH >: " + firstcommand)
Command()
