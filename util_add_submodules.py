# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import shared_choice
import sys
import git

py_path = os.path.dirname(sys.argv[0]);

    # Find our startup path; by default our path + "../../"
    # This usually corresponds to the main git directory
repo_path = py_path + "/../../"
if len(sys.argv) > 1:
    repo_path = sys.argv[1]
repo_path = os.path.abspath(repo_path);

    # Find our requirements json, by default or by argument
reqJSONPath = os.path.dirname(sys.argv[0]) + "/../requirements.json"
if len(sys.argv) > 2:
    reqJSONPath = sys.argv[2]
    
print("This script would like to pull missing submodules")
print()

print(" Repo: " + repo_path);
print(" JSON: .\\" + os.path.relpath(reqJSONPath, repo_path));
print()

import json

    # Parse JSON and find pipReq
requirements = []
with open(reqJSONPath, 'r') as f:
    requirements = json.load(f)

req_submodules = requirements["submodules"]
missing_submodules = req_submodules.copy()

    # Check which submodules already exist
repo = git.Repo(repo_path, odbt=git.GitCmdObjectDB)
if repo.bare:
    print("The repo is bare!")
    print("Press any key to continue.")
    input()
    sys.exit()
    
for sub in repo.submodules:
    print (sub.path)
    if sub.path in missing_submodules:
        del missing_submodules[sub.path]
    
    # Enumerate missing submodules
for sub, value in req_submodules.items():
    if sub in missing_submodules:
        print(" - " + value["name"] + " *")
    else:
        print(" - " + value["name"])
        
print()
   
if len(missing_submodules) == 0:
    sys.exit()
   
   # Offer user choice
if False == shared_choice.yn("Is adding submodules OK?"):
    sys.exit()
print()

    # Add missing submodules
for sub, value in missing_submodules.items():
    branch = value.get("branch", "public-develop")

    print("                                                        \r", end='')
    print("Adding: " + value["name"] + "\r", end='')
    try:
        repo.create_submodule (name=value["name"], path=sub, url=value["remote"], branch=branch)
        repo.index.add (['.gitmodules'])
        
        print("                                                        \r", end='')
        print("Added: " + value["name"])
    except:
        print("Failed: " + value["name"])
