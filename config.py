#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'valentinarho'
__author__ = 'matteomadeddu'

##### GOOGLE CALENDAR CONFIGURATION

# Setup your Google email and password
EMAIL = 'trello2google@gmail.com'
PASS = 'password'

# Define the name for the calendar dedicated to Trello events and trello2google app.
# if the calendar not exists the app will create it for you!
NOME_CALENDARIO = 'Trello Events'

##### TRELLO CONFIGURATION

# Application key and secret:
# Get it from this url: https://trello.com/1/appKey/generate
KEY = "TODO5ecac5876ad67fb32azzzzzzzzzz"
SECRET = "TODOs60c7c08aab64cab97a8370265caba6dfc2970f2635016803ac9azzzzzzz"

# Get forever token from visiting this url (first complete the url with your API-KEY)
# https://trello.com/1/authorize?key=__YOUR-APP-KEY__&name=Trello2Google&expiration=never&response_type=token
FOREVER_TOKEN = "TODO"

# Boards to convert
# On the left the board name, on the right the board id!
# Get your board id from Trello URL: https://trello.com/b/____BOARD-ID____/title-of-board
# Visit your board from a browser, and copy the ___BOARD-ID___ string.
BOARDS = {
    'Board One' : 'TODOfecdd2e8a35469000zzz',
    'Board Two' : 'TODOffa426a6793f36001zzz',
}