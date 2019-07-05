import re, os, sys, subprocess, requests, dispatch_config, json, copy

def AskConsent():
    confirmation = input("Confirm (Y/N): ")
    validated = re.match(r'([yYnN])', confirmation)
    if validated:
        return re.match(r'[yY]', confirmation)
    else:
        return False

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

def has_field(variable: str):
    obj = dispatch_config.webhook_payload
    try:
        for embed in obj["embeds"]:
            for field in embed["fields"]:
                if variable in field["value"]:
                    return True
        return False
    except KeyError:
        return False

def has_image_variable():
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
        confirmation = input("Fire webhook? (Y/N): ") if dispatch_config.webhook_url is not None and (has_field("[DEVELOPER]") or has_field("[NOTES]"))  else 'n'
        validated = re.match(r'([yYnN])', confirmation)
        if validated and re.match(r'[yY]', confirmation):
            note = input("Note: ") if has_field("[NOTES]") else 'None'
            if note == 'None':
                pass
            elif not note:
                print("Please add a note")
                return
            developer = input("Developer Tag (username#discrim): ") if has_field("[DEVELOPER]") else 'None'
            if developer == 'None':
                pass
            elif not developer:
                print("Please identify yourself")
                return
            image = input("Image URL: ") if has_image_variable() else 'None'
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

def ListBranches():
    subprocess.call(["dispatch", "branch", "list", dispatch_config.app_id])

def ListBuilds(branch_id: int):
    subprocess.call(["dispatch", "build", "list", dispatch_config.app_id, branch_id])

def PublishBuild(branch_id: int, build_id: int):
    subprocess.call(["dispatch", "build", "publish", dispatch_config.app_id, branch_id, build_id])

def DeleteBranch(branch_id: int):
    subprocess.call(["dispatch", "branch", "delete", dispatch_config.app_id, branch_id])

def Login():
    subprocess.call(["dispatch", "login"])

def Clear():
    os.system("cls")

def FireWebhook(developer: str, notes: str, image: str):

    #webhook url
    url = dispatch_config.webhook_url

    #payload = "{\"embeds\": [{\n\t\t\"title\": \"New Update\",\n\t\t\"fields\": [\n\t\t\t{\n\t\t\t\t\"name\": \"Developer\",\n\t\t\t\t\"value\": \"" + developer + "\"\t\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"name\": \"Update Notes\",\n\t\t\t\t\"value\": \""+ notes + "\"\n\t\t\t}\n\t\t],\n\t\t\"color\": 6356832,\n\t\t\"image\": {\n\t\t\t\"url\": \"https://cdn.discordapp.com/icons/379554898641027072/8f0e63d3a481e1d783eb61ba437ba4d1.webp\"\n\t\t}\n\t}]\n}"
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
    command = input("DISPATCH >: ")
    args = command.split(' ')
    args.remove(args[0])
    if command.startswith("login", 0):
        Login()
    elif command.startswith("update", 0):
        if len(args) == 1:
            PushUpdate(args[0])
        else:
            print("Please specify a branch ID.")
    elif command == "branch delete":
        DeleteBranch(args[0])
    elif command == "clear" or command == "cls":
        Clear()
    elif command == "branch list":
        ListBranches()
    elif command == "restart":
        Clear()
        os.execv(sys.executable, [sys.executable, "\""+os.path.join(sys.path[0], __file__)+"\""] + sys.argv[1:])
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
    elif command == "help":
        print("")
        print("===================================================================================================================================================")
        print("Help: (enter arguments without < & >)")
        print("login                                    - Opens browser to authenticate Discord Dispatch.")
        print("update < branch_id >                     - Starts updating process.")
        print("build publish < branch_id > < build_id > - Publishes uploaded update. Note that you can only publish updates that were updated for that branch ID.")
        print("build list < branch_id >                 - Lists builds for the specified branch.")
        print("branch list                              - Lists branches for SKU.")
        print("restart                                  - Restarts the client. Required after updating config or source code.")
        print("clear/cls                                - Clears the console.")
        print("exit                                     - Exits the client.")
        print("===================================================================================================================================================")
        print("If you found a bug you need fixed, feel free to open up an issue on my GitHub, or to push out a fix yourself.")
        print("")
    else:
        print("Unknown command.")
    if command != "exit":
        Command()

print("Use command \"exit\" to exit and \"help\" for help.")
Command()
