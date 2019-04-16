import os
import sys
import json
from pip._internal import main as pipmain

    # Find our requirements json, by default or by argument
reqJSONPath = os.path.dirname(sys.argv[0]) + "/../requirements.json"
if len(sys.argv) > 1:
    reqJSONPath = sys.argv[1]

    # Parse JSON and find pipReq
requirements = []
with open(reqJSONPath, 'r') as f:
    requirements = json.load(f)
pipReq = requirements["pip"]

    # For every pip req, we ask and install it from pip
for req in pipReq:
    package = req["package"]
    print("Checking " + package)
    pipmain(['install', package])