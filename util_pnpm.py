print("Checking pnpm...\r", end='')

import os
import shared_choice
import sys
import json
import subprocess

    # Find our requirements json, by default or by argument
reqJSONPath = os.path.dirname(sys.argv[0]) + "/../requirements.json"
if len(sys.argv) > 1:
    reqJSONPath = sys.argv[1]

    # Find our base path, by default or by argument
basePath = os.path.dirname(sys.argv[0]) + "/../../"
if len(sys.argv) > 2:
    reqJSONPath = sys.argv[2]

    # Parse JSON and find pipReq
requirements = []
with open(reqJSONPath, 'r') as f:
    requirements = json.load(f)
    
if requirements.get("pnpm", 0) == 0:
    print("No pnpm requirements found       ")
    sys.exit()
pnpmReq = requirements["pnpm"]
    
print("This script would like to use pnpm to install in:")
for req in pnpmReq:
    print(" * " + req["install"])
print()

if False == shared_choice.yn("Is using pnpm OK?"):
    sys.exit()
print()
   
for req in pnpmReq:
    path = basePath + req["install"];
    print("[" + req["install"] + "]")
    proc = subprocess.Popen(["pnpm", "install", "-D"], cwd=path, shell=True)
    proc.wait()