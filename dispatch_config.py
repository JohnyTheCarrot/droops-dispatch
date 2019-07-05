#Basic Configuration
app_id = "your_app_id_here"
default_branch = "your_default_branch_here"
enable_splash = True
custom_splash = False
custom_splash_file_path = "custom_splash.txt"
#	your email/domain
user_agent = "example.com"
#I'm talking about the config you'd normally use if you weren't using this client. Normal Discord gamedev Dispatch config.json.
#Path to your dispatch config.
dispatch_config_file = "config.json"
game_path = "game/windows"


#Webhook Config
webhook_url = ""
"""

Check the official Discord documentation on how to construct an embed:
https://discordapp.com/developers/docs/resources/channel#embed-object
If you'd like your message to have text, specify it outside of field "embeds" with "content": "content here"
For the color, it requires you to pass the color as an integer. See this useful tool to get that integer for your desired color:
https://www.shodor.org/stella2java/rgbint.html

Variables:
[DEVELOPER] If specified, the update method will request the updater to identify themselves. It will then replace the variable with said input.
[NOTES] If specified, the update method will request the updater to describe the update they're pushing out. It will then replace the variable with said input.
[IMAGE] If specified, the update method will request the updater to specify an image url to post in the embed.

"""
webhook_payload = {
		"embeds": [{
			"title": "New Update",
			"fields": [
				{
					"name": "Developer",
					"value": "[DEVELOPER]"
				},
				{
					"name": "Update Notes",
					"value": "[NOTES]"
				}
			],
			"color": 6356832,
			"image": {
				"url": "[IMAGE]"
			}
		}]
	}