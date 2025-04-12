
# (init) Take user information from linkedin for instance
# Ask user place & dates
# Fetch events & propose some of them
# User select some & ask info -> repeat 

from enum import StrEnum, auto


class Actions(StrEnum):

    FETCH_INFO = auto()
    FEEDBACK   = auto()

