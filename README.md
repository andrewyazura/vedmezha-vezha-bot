# Vedmezha Vezha Bot

Telegram bot for making table reservation at Vedmezha Vezha club

## Requirements

* Python 3.8

## Setup

1. Create virtual environment
2. Install packages from `requirements.txt`
3. Create `.env` file and configure it
   1. Use `.env.example` as an example
4. Make sure all specified paths in `.env` exist
5. Run using `python3.8 app.py`

## Config guide

* `BOT_TOKEN` - bot's token
* `BOT_OWNER_ID` - bot owner's telegram ID
* `BOT_REPORT_ID` - telegram ID of user who will receive error messages

* `DEFAULTS_PARSE_MODE` - default parse mode for messages (use HTML)
* `DEFAULT_RUN_ASYNC` - if True - bot can run async, else not

* `DATABASE_FILE` - path to database file (example: `./database/db.json`)

* `LOG_FILENAME` - path to log file (example: `./logs/telegram_bot.log`)

* `FILE_URL_ABOUT` - URL to image that is sent in response to "Про клуб 🙌" message
* `FILE_URL_LOCATION` - URL to image that is sent in response to "Місце розташування 🌍" message

* `TABLES_AMOUNT` - amount of tables
* `TABLES_FORMAT` - how to display table name (must contain `{}`)

* `RESERVATION_TIMEDELTA` - how many time in advance can a reservation be made
* `RESERVATION_OPENING_TIME` - when club opens
* `RESERVATION_CLOSING_TIME` - when club closes
* `RESERVATION_CLEAR_INTERVAL` - amount of time between removing old reservations
