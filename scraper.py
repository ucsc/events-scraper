from bs4 import BeautifulSoup
import requests
import re


class Writer(object):
    """
    Class to write event(s) to csv with or without column names
    """

    def __init__(self, columns):
        self.columns = columns

    def write(self, event_dict):
        """

        :param event_dict:
        :return:
        """
        event_string = ""
        for column in self.columns:
            if column in event_dict:
                event_string += event_dict[column] + ','
            else:
                event_string += ','

        print event_string

class Scraper(object):
    """
    Class to scrape a UCSC event
    """

    def __init__(self):
        self.date_regex = re.compile(r'(^\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}).*')

    def _scrape_group_items(self, main_content, class_name):
        """

        :param main_content:
        :param class_name:
        :return:
        """
        container = main_content.find('div', {'class': class_name})

        div = container.find('div', {'class': 'field-items'})

        items = div.find_all('div')

        return items

    def scrape_group_items_str(self, group_items):
        """
        Converts group items to a string
        :param group_items:
        :return:
        """
        items_string = ''

        for item in group_items:
            for content in item.contents:
                items_string += str(content)

        return items_string

    def scrape_group_items_text(self, group_items):
        """
        Extracts text from group items html
        :param group_items:
        :return:
        """
        items_string = ''

        for item in group_items:
            for content in item.contents:
                items_string += content.text + "\n"

        return items_string

    def scrape_title(self, body):
        """

        :param soup:
        :return:
        """
        container = body.find('div', {'class': 'grid_9 push_3'})

        return container.find('h1', {'id': 'title'}).get_text()

    def scrape_description(self, main_content):
        """
        Scrapes the Description
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content,
                                            'field field-name-body field-type-text-with-summary field-label-above')
        return self.scrape_group_items_str(group_items)

    def scrape_location(self, main_content):
        """
        Scrapes the event location
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-event-location '
                                                          'field-type-entityreference field-label-inline clearfix')
        return self.scrape_group_items_str(group_items)

    def scrape_location_details(self, main_content):
        """
        Scrapes the event location details
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-event-location-details '
                                                          'field-type-text-long field-label-above')
        return self.scrape_group_items_str(group_items)

    def scrape_admission(self, main_content):
        """
        Scrapes the event admission
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-admission field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.scrape_group_items_str(group_items)

    def scrape_admission_details(self, main_content):
        """
        Scrapes the event admission details
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-admission-details '
                                                          'field-type-text-long field-label-above')
        return self.scrape_group_items_str(group_items)

    def scrape_sponsor(self, main_content):
        """
        Scrapes the event sponor
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-event-affiliation field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.scrape_group_items_text(group_items)

    def scrape_related_url(self, main_content):
        """
        Scrapes the event related URL
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-related-url '
                                                          'field-type-link-field field-label-inline clearfix')
        url = ""

        if len(group_items) > 0:
            item = group_items[0].find('a')
            if item is not None:
                url = str(item['href'])

        return url

    def scrape_invited_audience(self, main_content):
        """
        Scrapes the event invited audience
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-audience field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.scrape_group_items_text(group_items)

    def scrape_category(self, main_content):
        """
        Scrapes the event category
        :param main_content:
        :return:
        """
        group_items = self._scrape_group_items(main_content, 'field field-name-field-event-type field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.scrape_group_items_str(group_items)

    def scrape_image(self, main_content):
        container = main_content.find('div', {'class': 'field field-name-field-event-image field-type-image '
                                                       'field-label-hidden'})

        div = container.find('div', {'class': 'field-items'})

        images = div.find_all('img')

        return str(images[0]['src'])

    def scrape_dates(self, main_content):
        container = main_content.find('div', {'class': 'field field-name-field-datetime field-type-datestamp '
                                                       'field-label-above'})

        date_spans = container.find_all('span', {'class': 'date-display-single'})

        dates_list = []

        for date_span in date_spans:
            dates_list.append(date_span['content'])

        return dates_list

    def date_time_to_tuple(self, date_time):
        """
        Converts a date time iso8601 string from a ucsc event to a tuple of the start time and date with
        the form 2016-06-04T11:00:00-07:00
        :param date_time:
        :return:
        """
        result = self.date_regex.findall(date_time)
        return result[0]

    def combine_description(self, description, location_details, admission_details):
        """
        Combines the description, location details, and admission details into one string
        :param description:
        :param location_details:
        :param admission_details:
        :return:
        """

        return_string = description

        return_string += "<h2>Location Details</h2>"

        return_string += location_details

        return_string += '<h2>Admission Details</h2>'

        return_string += admission_details

        return return_string

    def scrape_event(self, body):
        """
        Scrapes an event soup and returns an Event Object
        :param body: a bs4 soup representing the event html page
        :return:
        """

        content = body.find('div', {'id': 'main-content'})

        title = self.scrape_title(body)
        description = self.scrape_description(content)
        location = self.scrape_location(content)
        location_details = self.scrape_location_details(content)
        admission = self.scrape_admission(content)
        admission_details = self.scrape_admission_details(content)
        sponsor = self.scrape_sponsor(content)
        related_url = self.scrape_related_url(content)
        invited_audience = self.scrape_invited_audience(content)
        category = self.scrape_category(content)
        image = self.scrape_image(content)
        date_times = self.scrape_dates(content)

        event_list = []

        for date_time in date_times:
            date, time = self.date_time_to_tuple(date_time)
            full_description = self.combine_description(description, location_details, admission_details)
            event_dict = {
                'Title': title,
                "Description": full_description,
                'Date From': date,
                'Start Time': time,
                'Location': location,
                'Cost': admission,
                'Event Website': related_url,
                'Photo URL': image,
                "Sponsored": sponsor,
                "Invited Audience": invited_audience
            }
            event_list.append(event_dict)
        return event_list



def get_soup_from_url(page_url):
        """
        Takes the url of a web page and returns a BeautifulSoup Soup object representation
        :param page_url: the url of the page to be parsed
        :param article_url: the url of the web page
        :raises: r.raise_for_status: if the url doesn't return an HTTP 200 response
        :return: A Soup object representing the page html
        """
        r = requests.get(page_url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        return BeautifulSoup(r.content, 'lxml')



soup = get_soup_from_url('http://dev-ucscevents.pantheonsite.io/event/3710')
body_content = soup.find('div', {'id': 'main-content'})
scraper = Scraper()
events = scraper.scrape_event(soup)

column_titles = ['Title','Description','Date From','Date To','Recurrence','Start Time','End Time',
           'Location','Address','City','State','Event Website','Room','Keywords','Tags',
           'Photo URL','Ticket URL','Cost','Hashtag','Facebook URL','Group','Department',
           'Allow User Activity','Allow User Attendance','Visibility','Featured Tabs',
           'Sponsored','Venue Page Only','Exclude From Trending','Event Types','Invited Audience']

writer = Writer(column_titles)

import pprint
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(events[0])

writer.write(events[0])


