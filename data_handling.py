from pyredictit import pyredictit
import json
import sys, os
sys.path.append(os.path.abspath("../vars"))
from env_vars import *

pyredictit_api = pyredictit()
pyredictit_api.create_authed_session(username=user_name,password=password)
contracts = pyredictit_api.search_for_contracts()
for contract in contracts:
    print(contract)
    print("\n\n\n")
