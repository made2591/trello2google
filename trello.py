#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'matteomadeddu'

# TODO Implement the automatic retrieve of the Trello board code

import urllib2
import json
import config

class Trello(object):
    """
    Class that handles communications with the Trello server
    """

    def __init__(self, key=config.KEY, secret=config.SECRET, token=config.FOREVER_TOKEN, boards_list=config.BOARDS):
        self.key = key
        self.secret = secret
        self.token = token
        self.boards_list = boards_list

    def get_boards_of_user(self):
        """
        Returns the dictionary of all user's boards.
        :return:
        """
        return self.boards_list

    def get_lists_of_board(self, board_id):
        """
        Returns all lists contained in the specified board
        :param board_id: the board identifier
        :return:
        """
        dict = self.get_dict_from_json(self.get_json_response(
            "https://api.trello.com/1/board/" + board_id + "?key=" + self.key + "&token=" + self.token + "&lists=all"))
        lists = {}
        for list in dict['lists']:
            lists[list['name']] = list['id']

        return lists

    def get_cards_of_list(self, list_id):
        """
        Returns a dictionary of all cards contained in the specified list
        :param list_id: the list identifier
        :return:
        """
        dict = self.get_dict_from_json(self.get_json_response(
            "https://api.trello.com/1/lists/" + list_id + "?key=" + self.key + "&token=" + self.token + "&cards=all"))
        cards = {}
        for card in dict['cards']:

            if card['closed'] == False:

                # add the card id
                cards[card['name']] = {'id': card['id']}

                # check due date
                if card['due'] != None:
                    time = str(card['due']).split("T")
                    day = str(time[0])
                    hour = str(time[1][:-5])
                    cards[card['name']]['date'] = day
                    cards[card['name']]['hour'] = hour

                # check description
                if card['desc'] != "":
                    cards[card['name']]['description'] = card['desc']

                # check checklist
                if len(card['idChecklists']) != 0:
                    cards[card['name']]['idChecklists'] = card['idChecklists']

                # check labels
                if len(card['labels']) != 0:
                    cards[card['name']]['labels'] = card['labels']

        return cards

    def get_checklist_item(self, array_of_checklist):
        """
        Returns a dictionary of checklists of a card. Each checklist is a dictionary of check items.
        :param array_of_checklist:
        :return:
        """

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

