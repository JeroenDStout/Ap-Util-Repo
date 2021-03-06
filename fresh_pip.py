print("Checking pip...\r", end='')

import os
import shared_choice
import sys
import json

    # Find our requirements json, by default or by argument
reqJSONPath = os.path.dirname(sys.argv[0]) + "/../requirements.json"
if len(sys.argv) > 1:
    reqJSONPath = sys.argv[1]

    # Parse JSON and find pipReq
requirements = []
with open(reqJSONPath, 'r') as f:
    requirements = json.load(f)
pipReq = requirements["pip"]
    
print("This script would like to use pip to install the following items:")
for req in pipReq:
    print(" * " + req["package"])
print()
if False == shared_choice.yn("Is using pip OK?"):
    sys.exit()
print()

from pip._internal import main as pipmain

    # For every pip req, we ask and install it from pip
for req in pipReq:
    package = req["package"]
    print("[" + package + "]")
    pipmain(['install', package])