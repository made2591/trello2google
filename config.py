#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'valentinarho'
__author__ = 'matteomadeddu'

##### GOOGLE CALENDAR CONFIGURATION
EMAIL = 'trello2google@gmail.com'
PASS = 'password'
# You must define the name for the calendar dedicated to Trello events and trello2google app.
# if the calendar not exists the app will create it for you!
NOME_CALENDARIO = 'Calendario di trello2google'

##### TRELLO CONFIGURATION
# Get key and secret from
# PASS
KEY = "ce165ecac5876ad67fb32azzzzzzzzzz"
SECRET = "62a8760c7c08aab64cab97a8370265caba6dfc2970f2635016803ac9a8947zzz"
# Get forever token from
# https://trello.com/1/authorize?key=__KEY__&name=__NAME_OF_APPLICATION__&expiration=never&response_type=token
FOREVER_TOKEN = "7570779e2ce8aaf7ede6ce79db0df9dfdbd19059f91a45c42dc5dfa31f456zzz"

# Definite a mano con il token sull'url della board (visibile tramite browser)
BOARDS = {
    'Cose da vedere' : '51aefecdd2e8a35469000zzz',
    'Cose da fare' :   '51aeffa426a6793f36001zzz',
}