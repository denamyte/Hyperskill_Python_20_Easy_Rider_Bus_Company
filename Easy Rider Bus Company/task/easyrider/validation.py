import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Any, Callable, List

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


@dataclass
class StartFinish:
    start = False
    finish = False


FIELDS_META: Dict[str, MetaInfo] = {
    # 'bus_id': MetaInfo(is_int),
    # 'stop_id': MetaInfo(is_int),
    # 'stop_name': MetaInfo(is_stop_name),
    # 'next_stop': MetaInfo(is_int),
    # 'stop_type': MetaInfo(is_stop_type),
    # 'a_time': MetaInfo(is_time)
}


class Validation:
    NO_START_OR_END = 'There is no start or end stop for the line: {0}.'

    def __init__(self, json_str: str):
        self._json = json.loads(json_str)
        # self._errors: Dict[str, int] = {k: 0 for k in FIELDS_META.keys()}
        # self._bus_lines_counts: Dict[int, int] = defaultdict(lambda: 0)
        self._stop_error_bus_id = 0
        self._start_names: List[str] = []
        self._transfer_names: List[str] = []
        self._finish_names: List[str] = []
        self._check_fields()

    def _is_lines_points_error(self) -> int:
        stop_counter: Dict[int, StartFinish] = defaultdict(lambda: StartFinish())
        for r in self._json:
            bus_id = r.get('bus_id')
            stop_type = r.get('stop_type')
            match stop_type:
                case 'S':
                    if stop_counter[bus_id].start:
                        return bus_id
                    stop_counter[bus_id].start = True
                case 'F':
                    if stop_counter[bus_id].finish:
                        return bus_id
                    stop_counter[bus_id].finish = True
        for bus_id, sf in stop_counter.items():
            if sf.start + sf.finish < 2:
                return bus_id
        return 0

    def _collect_stop_names(self):
        start_set = set()
        finish_set = set()
        transfer_dict = defaultdict(lambda: 0)
        for r in self._json:
            stop_name = r.get('stop_name')
            stop_type = r.get('stop_type')
            match stop_type:
                case 'S': start_set.add(stop_name)
                case 'F': finish_set.add(stop_name)
            transfer_dict[stop_name] += 1

        self._start_names = sorted(start_set)
        self._finish_names = sorted(finish_set)
        self._transfer_names = sorted(k for k, v in transfer_dict.items()
                                      if v > 1)

    def _check_fields(self):
        self._stop_error_bus_id = self._is_lines_points_error()
        if self._stop_error_bus_id:
            return
        self._collect_stop_names()
        # for r in self._json:
        #     pass
        # self._bus_lines_counts[r.get('bus_id')] += 1
        # for name, meta in FIELDS_META.items():
        #    self._errors[name] += not meta.test(r.get(name))

    def __str__(self):
        if self._stop_error_bus_id:
            result = Validation.NO_START_OR_END.format(self._stop_error_bus_id)
        else:
            result = f'''\
Start stops: {len(self._start_names)} {self._start_names}
Transfer stops: {len(self._transfer_names)} {self._transfer_names}
Finish stops: {len(self._finish_names)} {self._finish_names}'''
        return result
        # return 'Line names and number of stops:\n' + \
        #        '\n'.join(f'bus_id: {k}, stops: {v}' for k, v
        #                  in self._bus_lines_counts.items())

        # total = sum(self._errors.values())
        # return f'Type and required field validation: {total} errors\n' + \
        #        '\n'.join(f'{k}: {v}' for k, v, in self._errors.items())
