#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO Setup bidirectional sync removing old events.

__author__ = 'valentinarho'

import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import time
import config

ID_LENGTH = 24
SERVICE_NAME = 'GCal-python-test'
debug = True


class Google(object):
    def __init__(self, email=config.EMAIL, psw=config.PASS, trelloCalendarName=config.CALENDAR_NAME):
        # init user's fields
        self.email = email
        self.password = psw
        self.trelloCalendarName = trelloCalendarName

        # start google calendar services
        self.calendarService = self.login(email, psw, SERVICE_NAME);

        # get the calendar instance
        self.calendarInstance = self.retrieve_trello_calendar_instance();

        # get the user identifier
        self.calendarUserID = self.calendarInstance.content.src.split('/')[5].replace('%40', '@')

        # prepare the URI of the calendar
        self.trelloCalendarUri = "http://www.google.com/calendar/feeds/" + self.calendarUserID + "/private/full-noattendees"

    def login(self, mail, psw, service_name):
        """
        Log in the user on google calendar
        :param mail: the user email
        :param psw: the user password
        :param service_name: the name of the service
        :return:
        """
        calendar_service = gdata.calendar.service.CalendarService()
        calendar_service.email = mail
        calendar_service.password = psw
        calendar_service.source = service_name
        calendar_service.ProgrammaticLogin()
        return calendar_service

    def retrieve_trello_calendar_instance(self):
        calendarInstance = self.get_calendar(self.trelloCalendarName)

        if calendarInstance == None:
            calendarInstance = self.create_trello_calendar(self.trelloCalendarName)

        return calendarInstance

    def get_calendar(self, calendarName):
        """
        Returns the calendar instance if exists, None otherwise
        :param calendarName: the calendar name
        :return:
        """
        feed = self.calendarService.GetOwnCalendarsFeed()

        for i, a_calendar in enumerate(feed.entry):
            if a_calendar.title.text == calendarName:
                return a_calendar

        return None

    def create_trello_calendar(self, calendarName):
        """
        Creates the Trello calendar on GCal
        :param calendarName: the name of the calendar
        :return:
        """
        # Create the calendar
        calendar = gdata.calendar.CalendarListEntry()
        calendar.title = atom.Title(text=calendarName)
        calendar.summary = atom.Summary(text='Test calendar for Trello2Google')
        calendar.where = gdata.calendar.Where(value_string='Torino')
        calendar.color = gdata.calendar.Color(value='#2952A3')
        calendar.hidden = gdata.calendar.Hidden(value='false')
        trellocalendar = self.calendarService.InsertCalendar(new_calendar=calendar)
        return trellocalendar;

    def print_users_calendars(self, calendar_service):
        """
        Prints the user's calendars
        :param calendar_service: the calendar service
        :return:
        """
        feed = calendar_service.GetOwnCalendarsFeed()
        print feed.title.text
        for i, a_calendar in enumerate(feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text,)

    def insert_single_event(self, title,
                            content='', where='',
                            start_time=None, end_time=None):
        """
        Inserts a new event on the trello calendar on gCal
        :param title: the event title
        :param content: the event content
        :param where: the event place
        :param start_time: the start time
        :param end_time: the end time
        :return:
        """

        # init a new Event
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=content)
        event.where.append(gdata.calendar.Where(value_string=where))

        if start_time is None:
            # Use current time for the start_time and have the event last 1 hour
            start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))

        # insert the event
        new_event = self.calendarService.InsertEvent(event, self.trelloCalendarUri)
        return new_event

    def insert_trello_checklist(self, name, date, id, checklist):
        """
        Insert a checklist in gCal
        :param name: the event name
        :param date: the event date
        :param id: the checklist id
        :param checklist: the checklist
        :return:
        """
        cont = ""
        if checklist != None:
            for k in checklist:
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
        self.insert_single_event(name, content=cont, start_time=date)

    def update_trello_checklist(self, event, name, date, id, checklist):
        """
        Updates a checklist
        :param event: the event to update
        :param name: the name of the event
        :param date: the date of the event
        :param id: the id of the checklist
        :param checklist: the checklist to insert
        :return:
        """
        event.title = atom.Title(text=name)
        event.where.append(gdata.calendar.Where(value_string=date))
        cont = ""

        if checklist != None:
            for k in checklist:
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

    def delete_event(self, event):
        """
        Deletes an event from calendar
        :param event:
        :return:
        """
        self.calendarService.DeleteEvent(event.GetEditLink().href)

    def get_all_events(self):
        """
        Returns a dictionary with trello ids as keys and event information as values
        :return:
        """
        eventlist = {}
        eventfeed = self.calendarService.GetCalendarEventFeed(self.trelloCalendarUri)
        for i, a_event in enumerate(eventfeed.entry):
            if a_event.content.text != None:
                lungh = len(a_event.content.text)
                #eventlist[a_event.content.text[lungh-LUNGHEZZAID:lungh]] = {'title': a_event.title.text,
                # 'description': a_event.content.text[0:lungh-LUNGHEZZAID]}
                eventlist[a_event.content.text[lungh - ID_LENGTH:lungh]] = {a_event}
            #print eventlist
        return eventlist


if __name__ == "__main__":
    google_instance = Google(config.EMAIL, config.PASS, config.CALENDAR_NAME)
    #googleInstance.insertSingleEvent("PROVA", content="prova aaaaaaaaaaaaaaaaaaaaaaa3",
    # start_time="2013-06-20", end_time="2013-06-20")

    calendarEvents = google_instance.get_all_events();

