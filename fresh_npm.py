print("Checking npm...\r", end='')

import os
import shared_choice
import sys
import json
import subprocess

    # Find our requirements json, by default or by argument
reqJSONPath = os.path.dirname(sys.argv[0]) + "/../requirements.json"
if len(sys.argv) > 1:
    reqJSONPath = sys.argv[1]

    # Parse JSON and find npmReq
requirements = []
with open(reqJSONPath, 'r') as f:
    requirements = json.load(f)
npmReq = requirements["npm"]
    
print("This script would like to use npm to install the following items using -g:")
for req in npmReq:
    print(" * " + req["package"])
print()

if False == shared_choice.yn("Is using npm OK?"):
    sys.exit()
   
for req in npmReq:
    pack = req["package"]
    print("[" + pack + "]")
    proc = subprocess.Popen(["npm", "install", "-g", pack], shell=True)
    proc.wait()