import json
from collections import defaultdict
from typing import List, Set


class Validation:
    def __init__(self, json_str: str):
        self._json = json.loads(json_str)
        self._illegal_names: List[str] = []
        self._on_demand_test()

    def _on_demand_test(self):
        st_f_tr_names: Set[str] = set()  # start, finish and transfer names
        on_demand_names: Set[str] = set()
        transfer_dict = defaultdict(lambda: 0)
        for r in self._json:
            stop_name = r.get('stop_name')
            stop_type = r.get('stop_type')

            transfer_dict[stop_name] += 1

            match stop_type:
                case 'S' | 'F':
                    st_f_tr_names.add(stop_name)
                case 'O':
                    on_demand_names.add(stop_name)

        st_f_tr_names.update(k for k, v in transfer_dict.items() if v > 1)
        self._illegal_names = sorted(st_f_tr_names & on_demand_names)

    def __str__(self):
        return 'On demand stops test:\n' + (
            f'Wrong stop type: {self._illegal_names}' if self._illegal_names
            else 'OK')
