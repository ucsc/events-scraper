from bs4 import BeautifulSoup
import requests


class Scraper(object):
    """
    Class to scrape a UCSC event
    """


class Event(object):
    """
    Object that represents a UCSC format Event
    """

    def __init__(self, title, description, location,
                 location_details, admission, admission_details,
                 sponsor, related_url, invited_audience,
                 category, images, dates):
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
        self.images = images
        self.dates = dates


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


def get_group_items(main_content, class_name):
    """

    :param main_content:
    :param class_name:
    :return:
    """
    container = main_content.find('div', {'class': class_name})

    div = container.find('div', {'class': 'field-items'})

    items = div.find_all('div')

    items_string = ''

    for item in items:
        for content in item.contents:
            items_string += str(content)

    return items_string


def get_title(body):
    """

    :param soup:
    :return:
    """
    container = body.find('div', {'class': 'grid_9 push_3'})

    return container.find('h1', {'id': 'title'}).get_text()


def get_image(main_content):
    container = main_content.find('div', {'class': 'field field-name-field-event-image field-type-image '
                                                   'field-label-hidden'})

    div = container.find('div', {'class': 'field-items'})

    images = div.find_all('img')

    images_string = ''

    for image in images:
        images_string += str(image['src'])

    return images_string

def get_dates(main_content):
    container = main_content.find('div', {'class': 'field field-name-field-datetime field-type-datestamp '
                                                   'field-label-above'})

    date_spans = container.find_all('span', {'class': 'date-display-single'})

    dates_list = []

    for date_span in date_spans:
        dates_list.append(date_span['content'])

    return dates_list


soup = get_soup_from_url('http://dev-ucscevents.pantheonsite.io/event/3710')

content = soup.find('div', {'id': 'main-content'})

title = get_title(soup)

description = get_group_items(content, 'field field-name-body field-type-text-with-summary field-label-above')

location = get_group_items(content, 'field field-name-field-event-location '
                                    'field-type-entityreference field-label-inline clearfix')

location_details = get_group_items(content, 'field field-name-field-event-location-details '
                                            'field-type-text-long field-label-above')

admission = get_group_items(content, 'field field-name-field-admission field-type-taxonomy-term-reference '
                                     'field-label-inline clearfix')

admission_details = get_group_items(content, 'field field-name-field-admission-details '
                                             'field-type-text-long field-label-above')

sponsor = get_group_items(content, 'field field-name-field-event-affiliation field-type-taxonomy-term-reference '
                                   'field-label-inline clearfix')

related_url = get_group_items(content, 'field field-name-field-related-url '
                                       'field-type-link-field field-label-inline clearfix')

invited_audience = get_group_items(content, 'field field-name-field-audience field-type-taxonomy-term-reference '
                                            'field-label-inline clearfix')

category = get_group_items(content, 'field field-name-field-event-type field-type-taxonomy-term-reference '
                                    'field-label-inline clearfix')

image = get_image(content)

dates = get_dates(content)

"""
print(description)
print('++++++')
print(location)
print('+++++')
print(location_details)
print('+++++')
print(admission)
print('+++++')
print(admission_details)
print('+++++')
print(sponsor)
print('+++++')
print(related_url)
print('+++++')
print(invited_audience)
print('+++++')
print(category)
print('+++++')
print(title)
print('+++++')
print(image)
print('+++++')
print(dates)
"""
