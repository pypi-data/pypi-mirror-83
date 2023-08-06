import re
from datetime import date
from .results import Success, Failure

class StringToObjectParser:
    def __init__(self, parse_fn):
        self.parse_fn = parse_fn

    def parse_from(self, val):
        return self.parse_fn(val)

def _date_from_iso_format(date_string):
    if not date_string:
        return Failure(message='date is missing')
    try:
      return Success(date=date.fromisoformat(date_string))
    except ValueError as e:
      return Failure(message=str(e))

def _int_from_string(attr):
    def parse(int_string):
        try:
            return Success(**{attr: int(int_string)})
        except ValueError as e:
            return Failure(message="'{}' is not a valid integer".format(int_string))
    return parse

date_from_iso = StringToObjectParser(parse_fn=_date_from_iso_format)

def int_from_string(attr='int_val'):
    return StringToObjectParser(parse_fn=_int_from_string(attr=attr))
