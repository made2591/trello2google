#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'valentinarho'

try:
    from xml.etree import ElementTree # for Python 2.5 users
except ImportError:
    from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import time
import config

LUNGHEZZAID = 24
NOME_SERVIZIO = 'GCal-python-test'
debug = True

class Google(object):

    def __init__(self, email=config.EMAIL, psw=config.PASS, trelloCalendarName=config.NOME_CALENDARIO):
        # inizializza i campi dell'utente
        self.email = email
        self.password = psw
        self.trelloCalendarName = trelloCalendarName

        # istanzia i servizi di google calendar
        self.calendarService = self.login(email, psw, NOME_SERVIZIO);

        # rappresenta l'istanza del calendario su google calendar
        self.calendarInstance = self.retrieveTrelloCalendarInstance();

        # codice identificativo dell'utente
        self.calendarUserID = self.calendarInstance.content.src.split('/')[5].replace('%40','@')

        # URI del calendario di trello su google
        self.trelloCalendarUri = "http://www.google.com/calendar/feeds/"+self.calendarUserID+"/private/full-noattendees"


    """ Effettua il login dell'utente a Google Calendar """
    def login(self, mail, psw, nome_servizio):
        calendar_service = gdata.calendar.service.CalendarService()
        calendar_service.email = mail
        calendar_service.password = psw
        calendar_service.source = nome_servizio
        calendar_service.ProgrammaticLogin()
        return calendar_service

    def retrieveTrelloCalendarInstance(self):
        calendarInstance = None
        calendarInstance = self.existsCalendar(self.trelloCalendarName)

        if calendarInstance == None :
            calendarInstance = self.createTrelloCalendar(self.trelloCalendarName)

        return calendarInstance

    """ return il l'istanza di un calendario se il calendario 'calendarName' esiste, None altrimenti """
    def existsCalendar(self, calendarName):
        feed = self.calendarService.GetOwnCalendarsFeed()

        for i, a_calendar in enumerate(feed.entry):
            if a_calendar.title.text == calendarName:
                return a_calendar

        return None

    """ crea il calendario di trello su gCal """
    def createTrelloCalendar(self, calendarName):
        # Create the calendar
        calendar = gdata.calendar.CalendarListEntry()
        calendar.title = atom.Title(text=calendarName)
        calendar.summary = atom.Summary(text='Calendario di prova per Trello2Google')
        calendar.where = gdata.calendar.Where(value_string='Torino')
        calendar.color = gdata.calendar.Color(value='#2952A3')
        calendar.hidden = gdata.calendar.Hidden(value='false')
        trellocalendar = self.calendarService.InsertCalendar(new_calendar=calendar)
        return trellocalendar;

    """ Stampa a video i calendari dell'utente """
    def printUserCalendars(self, calendar_service):
        feed = calendar_service.GetOwnCalendarsFeed()
        print feed.title.text
        for i, a_calendar in enumerate(feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text,)


    """ Inserisce un nuovo evento nel calendario di trello """
    def insertSingleEvent(self, title,
                          content='', where='',
                          start_time=None, end_time=None):

        # crea un oggetto Event e lo inizializza
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=content)
        event.where.append(gdata.calendar.Where(value_string=where))

        if start_time is None:
            # Use current time for the start_time and have the event last 1 hour
            start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))

        # inserisce l'evento nel calendario di trello
        new_event = self.calendarService.InsertEvent(event, self.trelloCalendarUri)
        return new_event

    def insertTrelloEvent(self, name, date, id, checklist):
        cont = ""
        if checklist != None:
            for k  in checklist:
                cont = cont + "\n\n" + k
                list = checklist[k]
                for item in list:
                    cont += "\n- "
                    state = list[item]
                    if state == "complete":
                        cont += "(DONE) "
                    else:
                        cont += "(TODO) "
                    cont += item
        cont = cont+"\n\n\n\n "+id
        self.insertSingleEvent(name, content=cont, start_time=date)

    def updateTrelloEvent(self, event, name, date, id, checklist):
        event.title = atom.Title(text=name)
        event.where.append(gdata.calendar.Where(value_string=date))
        cont = ""

        if checklist != None:
            for k  in checklist:
                cont = cont + "\n\n" + k
                list = checklist[k]
                for item in list:
                    cont += "\n- "
                    state = list[item]
                    if state == "complete":
                        cont += "(DONE) "
                    else:
                        cont += "(TODO) "
                    cont += item

        cont = cont + "\n\n\n\n " + id
        event.content = atom.Content(cont)
        return self.calendarService.UpdateEvent(event.GetEditLink().href, event)

    """ Cancella un evento dal calendario di trello """
    def removeEvent(self, event):
        self.calendarService.DeleteEvent(event.GetEditLink().href)

    #def getEvent(self, title='', trelloCode=''):

    """ Ritorna un dizionario con chiave = 'codice di trello' e informazioni sull'evento """
    def getCalendarEvents(self):
        eventlist = {}
        eventfeed = self.calendarService.GetCalendarEventFeed(self.trelloCalendarUri)
        for i, a_event in enumerate(eventfeed.entry):
            if a_event.content.text != None:
                lungh = len(a_event.content.text)
                #eventlist[a_event.content.text[lungh-LUNGHEZZAID:lungh]] = {'title': a_event.title.text, 'description': a_event.content.text[0:lungh-LUNGHEZZAID]}
                eventlist[a_event.content.text[lungh-LUNGHEZZAID:lungh]] = {a_event}
        #print eventlist
        return eventlist;



if __name__ == "__main__":
    googleInstance = Google(config.EMAIL, config.PASS, config.NOME_CALENDARIO)
    #googleInstance.insertSingleEvent("PROVA", content="prova aaaaaaaaaaaaaaaaaaaaaaa3", start_time="2013-06-20", end_time="2013-06-20")

    calendarEvents = googleInstance.getCalendarEvents();

