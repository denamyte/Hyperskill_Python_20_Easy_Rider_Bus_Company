import re
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Any, Callable

PREDICATE = Callable[[Any], bool]

# STOP_NAME_REGEXP = re.compile('^[A-Z].* (Road|Street|Boulevard|Avenue)$')
# STOP_TYPE_REGEXP = re.compile('^[SOF]?$')
# TIME_REGEXP = re.compile('^([01][0-9]|2[0-3]):([0-5][0-9])$')

# is_str: PREDICATE = lambda v: type(v).__name__ == 'str'
# is_int: PREDICATE = lambda v: type(v).__name__ == 'int'

# is_not_empty_str: PREDICATE = lambda v: is_str(v) and v
# is_stop_name: PREDICATE = lambda v: is_str(v) and STOP_NAME_REGEXP.match(v)
# is_stop_type: PREDICATE = lambda v: is_str(v) and STOP_TYPE_REGEXP.match(v)
# is_time: PREDICATE = lambda v: is_str(v) and TIME_REGEXP.match(v)


@dataclass
class MetaInfo:
    test: PREDICATE


FIELDS_META: Dict[str, MetaInfo] = {
    # 'bus_id': MetaInfo(is_int),
    # 'stop_id': MetaInfo(is_int),
    # 'stop_name': MetaInfo(is_stop_name),
    # 'next_stop': MetaInfo(is_int),
    # 'stop_type': MetaInfo(is_stop_type),
    # 'a_time': MetaInfo(is_time)
}


class Validation:
    def __init__(self, json_str: str):
        self._json = json.loads(json_str)
        # self._errors: Dict[str, int] = {k: 0 for k in FIELDS_META.keys()}
        self._bus_lines: Dict[int, int] = defaultdict(lambda: 0)
        self._check_fields()

    def _check_fields(self):
        for r in self._json:
            self._bus_lines[r.get('bus_id')] += 1
            # for name, meta in FIELDS_META.items():
            #    self._errors[name] += not meta.test(r.get(name))

    def __str__(self):
        return 'Line names and number of stops:\n' + \
               '\n'.join(f'bus_id: {k}, stops: {v}' for k, v
                         in self._bus_lines.items())
        # total = sum(self._errors.values())
        # return f'Type and required field validation: {total} errors\n' + \
        #        '\n'.join(f'{k}: {v}' for k, v, in self._errors.items())
