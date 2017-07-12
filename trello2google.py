#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'matteomadeddu'
__author__ = 'valentinarho'

import gcal
import trello


def sync_trello(gInstance, tInstance):
    # trello events
    trelloDict = tInstance.get_dict_of_dated_cards()
    # events dictionary indexed by trello identifier
    googleDict = gInstance.get_all_events()

    #print trelloDict

    for trellokey in trelloDict:
        idEvento = trelloDict[trellokey].get("id")
        # TIME FORMAT: %Y-%m-%dT%H:%M:%S.000Z
        time = trelloDict[trellokey].get("date") + "T" + trelloDict[trellokey].get("hour")

        cl = trelloDict[trellokey].get("checkList")
        ev = googleDict.get(idEvento, "")
        for x in ev:
            test = x

        if ev == "":
            # create google event
            google_instance.insert_trello_checklist(name=trellokey, date=time, id=idEvento, checklist=cl)
            pass
        else:
            # update info of the event
            google_instance.update_trello_checklist(test, name=trellokey, date=time, id=idEvento, checklist=cl)
            del (googleDict[idEvento])

    for eventKey in googleDict:
        ev = googleDict.get(eventKey, "")
        for x in ev:
            test = x

        google_instance.delete_event(test)


if __name__ == "__main__":
    print "The following events have been added to the calendar: "
    google_instance = gcal.Google()
    trello_instance = trello.Trello()

    sync_trello(google_instance, trello_instance)
    print "Process completed."