# Birthday Lord Bot
Is a telegram bot that will remind you about your friends' birthdays.

# How to use
1. Create _cache_ directory.
```bash
birthday-lord-bot$ mkdir cache
```

2. Place Goggle Sheets Service account json key file into created directory _cache_  (see instructions how to get it below)

3. Fill in settings in _config.yaml_.
    - `google_sheets_credentials_file` should contain your json key file name from previous step.
    - `google_sheets_spreadsheet_id` should contain ID of your spreadsheet with birthdays. You can extract it from URL. When you editing spreadsheet in a browser you'll see it inside the address bar: `https://docs.google.com/spreadsheets/d/**SPREADSHEETID**/edit#gid=0`.

4. Add access to read your streadsheet with birthdays for service account.

5. Run docker.
```bash
birthday-lord-bot$ docker-compose run --build -d
```

# How to get Google Sheets API service account
Go to https://console.developers.google.com/cloud-resource-manager and press Create Project.

Go to project Settings -> Roles and add your real email as owner.

In project Settings -> Service Accounts create one with role owner. Then create json key for this service account and save file reliably.
Save email of service account. You can allow access to your spreadsheet for the bot by adding rights to read for this email in Google Sheets UI.
