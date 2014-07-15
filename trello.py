#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'matteomadeddu'

# TODO fare retrieve del codice della board in automatico

import urllib2
import json
import config


class Trello(object):
    """ Questa classe istanzia un oggetto Trello che gestisce la comunicazione con il server
    """

    def __init__(self, key=config.KEY, secret=config.SECRET, token=config.FOREVER_TOKEN, boards_list=config.BOARDS):
        self.key = key
        self.secret = secret
        self.token = token
        self.boards_list = boards_list

    """ Questo metodo ritorna il dizionario di board definito sopra"""

    def get_boards_of_user(self):
        return self.boards_list

    """ Questo metodo ritorna un dizionario delle liste di una board specifica"""

    def get_lists_of_board(self, board_id):
        dict = self.get_dict_from_json(self.get_json_response(
            "https://api.trello.com/1/board/" + board_id + "?key=" + self.key + "&token=" + self.token + "&lists=all"))
        lists = {}
        for list in dict['lists']:
            lists[list['name']] = list['id']

        return lists

    """ Questo metodo ritorna un dizionario delle cards di una lista specifica (card ancora aperte)"""

    def get_cards_of_list(self, list_id):
        dict = self.get_dict_from_json(self.get_json_response(
            "https://api.trello.com/1/lists/" + list_id + "?key=" + self.key + "&token=" + self.token + "&cards=all"))
        cards = {}
        for card in dict['cards']:

            if card['closed'] == False:

                # Aggiungo l'id della card trovata
                cards[card['name']] = {'id': card['id']}

                # Controllo se la card ha un data di scadenza
                if card['due'] != None:
                    time = str(card['due']).split("T")
                    day = str(time[0])
                    hour = str(time[1][:-5])
                    cards[card['name']]['date'] = day
                    cards[card['name']]['hour'] = hour

                # Controllo se la card ha una descrizione
                if card['desc'] != "":
                    cards[card['name']]['description'] = card['desc']

                # Controllo se nella card c'è una check list
                if len(card['idChecklists']) != 0:
                    cards[card['name']]['idChecklists'] = card['idChecklists']

                # Controllo se nella card ci sono delle label
                if len(card['labels']) != 0:
                    cards[card['name']]['labels'] = card['labels']

        return cards

    """ Questa funzione restituisce un dizionario di checklist (dizionari di check item) di una data card"""

    def get_checklist_item(self, array_of_checklist):

        checklist = {}

        for i in array_of_checklist:

            checkitems = self.get_dict_from_json(self.get_json_response(
                "https://api.trello.com/1/checklists/" + i + "?key=" + self.key + "&token=" + self.token))
            checkitem = {}
            for k in checkitems['checkItems']:
                checkitem[k['name']] = k['state']

            checklist[checkitems['name']] = checkitem

        return checklist

    def get_json_response(self, url):
        response = urllib2.urlopen(url)
        return response.read()

    def get_dict_from_json(self, json_data):
        return json.loads(json_data)

    def get_dict_of_dated_cards(self):

        cards_dict = {}

        for name, value in self.boards_list.items():
            lists = self.get_lists_of_board(value)
            for name, value in lists.items():
                cards = self.get_cards_of_list(value)
                for name, value in cards.items():
                    if value.has_key('date'):
                        if value.has_key('idChecklists'):
                            value['checkList'] = self.get_checklist_item(value['idChecklists'])
                        cards_dict[name] = value
                        print value
        return cards_dict

