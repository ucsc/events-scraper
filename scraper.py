from bs4 import BeautifulSoup
import requests


class Writer(object):
    """
    Class to write event(s) to csv with or without column names
    """

    def __init__(self):


class Scraper(object):
    """
    Class to scrape a UCSC event
    """

    def _get_group_items(self, main_content, class_name):
        """

        :param main_content:
        :param class_name:
        :return:
        """
        container = main_content.find('div', {'class': class_name})

        div = container.find('div', {'class': 'field-items'})

        items = div.find_all('div')

        return items

    def get_group_items_str(self, group_items):
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

    def get_title(self, body):
        """

        :param soup:
        :return:
        """
        container = body.find('div', {'class': 'grid_9 push_3'})

        return container.find('h1', {'id': 'title'}).get_text()

    def get_description(self, main_content):
        """
        Scrapes the Description
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content,
                                            'field field-name-body field-type-text-with-summary field-label-above')
        return self.get_group_items_str(group_items)

    def get_location(self, main_content):
        """
        Scrapes the event location
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-event-location '
                                                          'field-type-entityreference field-label-inline clearfix')
        return self.get_group_items_str(group_items)

    def get_location_details(self, main_content):
        """
        Scrapes the event location details
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-event-location-details '
                                                          'field-type-text-long field-label-above')
        return self.get_group_items_str(group_items)

    def get_admission(self, main_content):
        """
        Scrapes the event admission
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-admission field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.get_group_items_str(group_items)

    def get_admission_details(self, main_content):
        """
        Scrapes the event admission details
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-admission-details '
                                                          'field-type-text-long field-label-above')
        return self.get_group_items_str(group_items)

    def get_sponsor(self, main_content):
        """
        Scrapes the event sponor
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-event-affiliation field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.get_group_items_str(group_items)

    def get_related_url(self, main_content):
        """
        Scrapes the event related URL
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-related-url '
                                                          'field-type-link-field field-label-inline clearfix')
        url = ""

        if len(group_items) > 0:
            item = group_items[0].find('a')
            if item is not None:
                url = str(item['href'])

        return url

    def get_invited_audience(self, main_content):
        """
        Scrapes the event invited audience
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-audience field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.get_group_items_str(group_items)

    def get_category(self, main_content):
        """
        Scrapes the event category
        :param main_content:
        :return:
        """
        group_items = self._get_group_items(main_content, 'field field-name-field-event-type field-type-'
                                                          'taxonomy-term-reference field-label-inline clearfix')
        return self.get_group_items_str(group_items)

    def get_image(self, main_content):
        container = main_content.find('div', {'class': 'field field-name-field-event-image field-type-image '
                                                       'field-label-hidden'})

        div = container.find('div', {'class': 'field-items'})

        images = div.find_all('img')

        return str(images[0]['src'])

    def get_dates(self, main_content):
        container = main_content.find('div', {'class': 'field field-name-field-datetime field-type-datestamp '
                                                       'field-label-above'})

        date_spans = container.find_all('span', {'class': 'date-display-single'})

        dates_list = []

        for date_span in date_spans:
            dates_list.append(date_span['content'])

        return dates_list

    def scrape_event(self, body):
        """
        Scrapes an event soup and returns an Event Object
        :param body: a bs4 soup representing the event html page
        :return:
        """

        content = body.find('div', {'id': 'main-content'})

        title = self.get_title(body)
        description = self.get_description(content)
        location = self.get_location(content)
        location_details = self.get_location_details(content)
        admission = self.get_admission(content)
        admission_details = self.get_admission_details(content)
        sponsor = self.get_sponsor(content)
        related_url = self.get_related_url(content)
        invited_audience = self.get_invited_audience(content)
        category = self.get_category(content)
        image = self.get_image(content)
        dates = self.get_dates(content)

        event = Event(title, description, location, location_details, admission,
                      admission_details, sponsor, related_url, invited_audience, category, image, dates)

        return event


class Event(object):
    """
    Object that represents a UCSC format Event
    """

    def __init__(self, title, description, location,
                 location_details, admission, admission_details,
                 sponsor, related_url, invited_audience,
                 category, image, dates):
        """
        Initialize a new Event Object
        """
        self.title = title
        self.description = description
        self.location = location
        self.location_details = location_details
        self.admission = admission
        self.admission_details = admission_details
        self.sponsor = sponsor
        self.related_url = related_url
        self.invited_audience = invited_audience
        self.category = category
        self.image = image
        self.dates = dates

    def __str__(self):
        return "Event:\n  title: %s\n  description: %s\n  location: %s\n  location details: %s\n" \
               "  admission: %s\n  admission details: %s\n  sponsor: %s\n  related url: %s\n" \
               "  invited audience: %s\n  category: %s\n  image: %s\n  dates: %s\n" \
               % (self.title, self.description, self.location, self.location_details, self.admission,
                  self.admission_details, self.sponsor, self.related_url, self.invited_audience,
                  self.category, self.image, str(self.dates))


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
event = scraper.scrape_event(soup)
print event


