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
###### Example
`DISPATCH >: login`
##### Parameters
None

### update
###### Example
`DISPATCH >: update 532009786162806794`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch you'd like to upload the update to        |

### build publish
###### Example
`DISPATCH >: build publish 532009786162806794 539036401950261275`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch the update was uploaded on       |
| build_id         | ID of the build       |

### build list
###### Example
`DISPATCH >: build list 532009786162806794`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch you'd like to list the builds of       |

### branch list
###### Example
`DISPATCH >: branch list`
##### Parameters
None

### branch delete
###### Example
`DISPATCH >: branch delete 532009786162806794`
##### Parameters

| argument         | description |
| ---------------- | ----------- |
| branch_id        | ID of the branch you'd to delete       |

### restart
###### Example
`DISPATCH >: restart`
##### Parameters
None

### clear/cls
###### Example
`DISPATCH >: clear`
`DISPATCH >: cls`
##### Parameters
None

### exit
###### Example
`DISPATCH >: exit`
##### Parameters
None

## Configuration

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
