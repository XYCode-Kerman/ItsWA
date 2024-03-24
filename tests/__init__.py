import json
import pathlib
import sys

sys.path.append('../')
ccf = pathlib.Path('./tests/environment/ccf.json')
data = json.load(ccf.open())
data['header']['path'] = ccf.parent.absolute().__str__()
json.dump(data, ccf.open('w'), ensure_ascii=False, indent=4)
