# -*- coding: utf-8 -*-
"""The data structures (items) that we want to get from scraping."""

from datetime import datetime

import scrapy


def _serialize_date(date_string):
    """Reads the date string in format MM/DD/YYYY and serializes it as ISODate object."""
    date = datetime.strptime(date_string, '%m/%d/%Y')
    # TODO right now I'm just appending the 'Z' as if it was UTC time. Need to check what it is.
    # Also, if I'd add timezone to the date object, it would dump it with a +00:00 instead of the Z
    return f'ISODate("{date.isoformat()}Z")'


class ForeignPrincipalItem(scrapy.Item):
    """
    A Foreign Principal from FARA.
    """
    url = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    reg_num = scrapy.Field()
    address = scrapy.Field()
    foreign_principal = scrapy.Field()
    # Foreign Principal Registration Date
    date = scrapy.Field(serializer=_serialize_date)
    registrant = scrapy.Field()
    exhibit_url = scrapy.Field()
