# Birthdays Lord Bot
Is a telegram bot that will remind you about your friends' birthdays.

# How to use
1. Create _cache_ directory.
```bash
birthdays-lord-bot$ mkdir cache
```

2. Place Goggle Sheets Service account json key file into created directory _cache_  (see instructions how to get it below)

3. Fill in settings in _config.yaml_.

4. Add access to read your streadsheet with birthdays for service account.

5. Run docker.
```bash
birthdays-lord-bot$ docker-compose run --build -d
```

# How to get Google Sheets API service account
Go to https://console.developers.google.com/cloud-resource-manager and press Create Project. Create a new project.

Go to the project Settings -> Roles and add your real email as owner.

In project Settings -> Service Accounts create one with role owner. Then create json key for this service account and save file reliably.
Save email of service account. You can allow access to your spreadsheet for the bot by adding rights to read for this email in Google Sheets UI.
