#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'valentinarho'
__author__ = 'matteomadeddu'

import gcal
import trello
import json

def trelloSync(gInstance, tInstance):
    # json di eventi di trello
    trelloDict = tInstance.get_dict_of_dated_cards()
    # dizionario di event indicizzato by codice di trello
    googleDict = gInstance.getCalendarEvents()

    #print trelloDict

    for trellokey in trelloDict:
        idEvento = trelloDict[trellokey].get("id")
        # TIME FORMAT: %Y-%m-%dT%H:%M:%S.000Z
        time = trelloDict[trellokey].get("date")+"T"+trelloDict[trellokey].get("hour")
        #print trelloDict[trellokey]
        cl = trelloDict[trellokey].get("checkList")
        ev = googleDict.get(idEvento, "")
        for x in ev:
            prova = x

        if ev == "":
            # crea l'evento su google
            googleInstance.insertTrelloEvent(name=trellokey, date=time, id=idEvento, checklist=cl)
            pass
        else:
            # aggiorna le info dell'evento
            googleInstance.updateTrelloEvent(prova, name=trellokey, date=time, id=idEvento, checklist=cl)
            del(googleDict[idEvento])

    for eventKey in googleDict:
        ev = googleDict.get(eventKey, "")
        for x in ev:
            prova = x

        googleInstance.removeEvent(prova)

if __name__ == "__main__":
    googleInstance = gcal.Google()
    trelloInstance = trello.Trello()

    trelloSync(googleInstance, trelloInstance)
