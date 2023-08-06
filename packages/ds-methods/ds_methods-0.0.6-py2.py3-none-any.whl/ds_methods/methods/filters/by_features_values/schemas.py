import re
from datetime import datetime
from numbers import Number
from schema import Schema, And, Or

MATCHERS = {
    'lte': lambda x: re.match(r'[a-z]+__lte$', x),
    'gte': lambda x: re.match(r'[a-z]+__gte$', x),
    'equal': lambda x: re.match(r'[a-z]+__equal$', x),
}

options_schema = Schema(
    {
        And(
            str,
            lambda x: any(matcher(x) for matcher in MATCHERS.values()),
        ): Or(Number, str, datetime, bool),
    },
    ignore_extra_keys=True,
)
