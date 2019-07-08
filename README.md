# droops-dispatch
> **Note:**
> You need to have a gamedev license from Discord.
> You can buy a license by selecting/creating an application on [Discord's Developer Portal](https://discordapp.com/developers/applications).

#### IMPORTANT
Don't forget to set Discord's first party Dispatch as 'dispatch' in your environment variables!

### How it works:
It listens for your shorter command, and executes the longer, normal command for you.

For example:

`update 532009786162806794`

would do

`dispatch build push 532009786162806794 config.json Game/Windows`

## Commands
### login
Opens Discord's oauth2 window to authorize Dispatch with your account.
###### Example
`DISPATCH >: login`
##### Parameters
None

### update
Uploads the game files to the specified branch.
###### Example
`DISPATCH >: update 532009786162806794`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch you'd like to upload the update to        |

### build publish
Publishes a build for it's branch.
Note that, to publish a build, it had to be uploaded with the update command to said branch first.
You **cannot** publish a build for branch 2 when it was uploaded to branch 1.
###### Example
`DISPATCH >: build publish 532009786162806794 539036401950261275`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch the update was uploaded on       |
| build_id         | ID of the build       |

### build list
Lists all builds for the specified branch.
###### Example
`DISPATCH >: build list 532009786162806794`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch you'd like to list the builds of       |

### branch list
Lists all branches.
###### Example
`DISPATCH >: branch list`
##### Parameters
None

### branch delete
Deletes the specified branch.
###### Example
`DISPATCH >: branch delete 532009786162806794`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch you'd to delete       |


## CLI Commands

### checkupdate
Checks for updates.
###### Example
`DISPATCH >: checkupdate`
##### Parameters
None

### runupdate
Downloads & installs update.
###### Example
`DISPATCH >: runupdate`
##### Parameters
None

### restart
Restarts the CLI, **required** for when you have changed the config.
###### Example
`DISPATCH >: restart`
##### Parameters
None

### clear/cls
Clears the console.
###### Example
`DISPATCH >: clear`

`DISPATCH >: cls`
##### Parameters
None

### exit
Exits the CLI.
###### Example
`DISPATCH >: exit`
##### Parameters
None

## Configuration
### NOTE:
> A restart of the CLI is **required** after every config change.
> You can restart the CLI with the `restart` command.

| variable         | type        | description                            |
| ---------------- | ----------- | -------------------------------------- |
| app_id           | Int64       | The snowflake ID of your SKU           |
| default_branch   | Int64       | The snowflake ID of the branch the update command should default to, should the branch argument not be passed |
| enable_splash    | Bool        | Whether or not to post a splash on startup |
| custom_splash    | Bool        | True for a custom splash, False for the default splash |
| custom_splash_file_path | str  | Filepath of the custom splash, if enabled  |
| user_agent       | str         | Your email or website domain. Used to identify your requests to Discord. |
| dispatch_config_file | str     | Filepath of your Dispatch config. WARNING: NOT the same as the config file of the client! |
| game_path        | str         | Filepath of your game files to be uploaded to Discord |
| webhook_url      | str         | Webhook URL to fire for game upload webhook |
| webhook_payload  | dict        | JSON object of the webhook post              |
