# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import shared_choice
import sys
import git

print("This script would like to check if branches are behind remotes")
if False == shared_choice.yn("Is checking git branches OK?"):
    sys.exit()
print()
    
    # This is the suffix of our branch names
    # in no particular order
branch_name_check = [
    "public-master",
    "public-develop",
    "private-master",
    "private-develop"
]

exclude_dirs = [
    ".vs",
    "node_modules"
]

    # Find our startup path; by default our path + "../../"
    # This usually corresponds to the main git directory
dir_path = os.path.dirname(sys.argv[0]) + "/../../"
if len(sys.argv) > 1:
    dir_path = sys.argv[1]
dir_path = os.path.abspath(dir_path);
    
    # Walk through all directories to find a .git file
    # We do not follow symlinks as we're only really
    # interested in the basic git structure
git_dirs = []
for (root, dirs, files) in os.walk(dir_path, followlinks=False):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for name in files:
        if name == ".git":
            git_dirs.append(os.path.abspath(root))
    
print("                                             \r", end='')

possibly_behind_count = 0
dirty_count = 0

    # For every git dir, we want to evaluate their current
    # branch and see if it is behind an identical remote
for dir in git_dirs:
    print("                                                        \r", end = '')
    print("[" + os.path.relpath(dir, dir_path) + "]\r", end = '')
    
        # Check if the repo is bare
    repo = git.Repo(dir, odbt=git.GitCmdObjectDB)
    if repo.bare:
        print("Was bare!")
        continue
        
        # If the head is detached, we're done
    if repo.head.is_detached:
        print("Is detached!")
        continue
    
    repo_head_name = str(repo.head.ref)
    
        # Fetch from the repo's remotes to see if any
        # remote branches match our name
    remote_branch_names = []
    for remote in repo.remotes:
        for fetch_info in remote.fetch():
            fetch_name = str(fetch_info.ref.name)
                
            if fetch_name.endswith("/" + repo_head_name):
                remote_branch_names.append(fetch_info.ref.name)
                continue
        
            for name in branch_name_check:            
                if (not fetch_name.endswith(name) and
                    not fetch_name.endswith("/" + repo_head_name)
                ):
                    continue
                    
                remote_branch_names.append(fetch_info.ref.name)
                break
    
    any_shown_behind = 0
    
    if repo.is_dirty():
        any_shown_behind = 1;
        dirty_count += 1;
        print()
        print(" Is dirty!")
    
    for branch in remote_branch_names:
        commits_ahead   = repo.iter_commits(branch + '..' + repo_head_name)
        commits_ahead_count = sum(1 for c in commits_ahead)
        
        commits_behind  = repo.iter_commits(repo_head_name + '..' + branch)
        commits_behind_count = sum(1 for c in commits_behind)
        
        if commits_ahead_count >= 0 and commits_behind_count == 0:
            continue
            
        if 0 == any_shown_behind:
            possibly_behind_count += 1
            print()
            
        any_shown_behind = 1
        
        print(" " + str(branch) + ": " + str(commits_behind_count) + " behind, " + str(commits_ahead_count) + " ahead")
    
    if 1 == any_shown_behind:    
        print()
    
if possibly_behind_count > 0 or dirty_count > 0:
    print("                                                        \r", end = '')
    if dirty_count > 0:
        print(" " + str(dirty_count) + " subrepos were found to be dirty.")
    if possibly_behind_count > 0:
        print(" " + str(possibly_behind_count) + " subrepos were found to be behind.")
    print()
    print("Press any key to continue.")
    input()