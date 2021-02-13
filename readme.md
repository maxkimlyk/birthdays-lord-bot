# Birthdays Lord Bot
Is a telegram bot that will remind you about your friends' birthdays.
The bot connects to your Google Sheets table with birthdays.

# How to use
1. Create _cache_ directory.
```bash
birthdays-lord-bot$ mkdir cache
```

2. Create Goggle Sheets Service Account and place json key file into created
 directory _cache_  (see instructions  below).

3. Fill in settings in _config.yaml_:
    - `google_sheets_credentials_file` - name of the file from previous step
    - `telegram_api_token` - telegram bot token from [BotFather](https://t.me/botfather)
    - `telegram_users_id` - list of user ids allowed to use the bot

5. Run docker.
```bash
birthdays-lord-bot$ docker-compose run --build -d
```

# How to get Google Sheets API service account
Go to https://console.developers.google.com/cloud-resource-manager
and press **Create Project**. Create a new project.

Go to the project **Settings** -> **Roles** and add your real email as owner.

In project **Settings** -> **Service Accounts** create one with role owner.
Then create json key for this service account and save file reliably.
Save email of service account. In order to allow bot access to your
spreadsheet you can add read access for this account,
or simply allow access for all users that have a link to your spreadsheet.
