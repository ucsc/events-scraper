

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
