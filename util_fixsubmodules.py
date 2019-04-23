print("Checking git directories...\r", end='')

import os
import shared_choice
import sys
import git

    # This is the priority of our branch names
    # in descending order
branch_name_priority = [
    "public-master",
    "public-develop",
    "private-master",
    "private-develop",
    "-master",
    "-develop"
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
    
print("This script would like to find the correct branch for:")
for dir in git_dirs:
    print(" * " + os.path.relpath(dir, dir_path))
print()
if False == shared_choice.yn("Is correcting git branches OK?"):
    sys.exit()
print()
    
    # For every git dir, we want to evaluate their current
    # branch and correct it if it is HEAD
for dir in git_dirs:
    print("[" + os.path.relpath(dir, dir_path) + "]")
    
        # Check if the repo is bare
    repo = git.Repo(dir, odbt=git.GitCmdObjectDB)
    if repo.bare:
        print("Was bare!")
        continue
        
        # If the head is not detached, we're done
    if not repo.head.is_detached:
        print("In branch: " + str(repo.head.ref))
        print()
        continue
    
    matchHead       = 0
    matchQuality    = 999
    
        # Compare the hexsha against branches;
        # we favour the main master/develop, and
        # then favour relative master/develop
    hex = repo.head.commit.hexsha
    
    matchNames = []
    for head in repo.heads:
        if head.commit.hexsha != hex:
            continue
        matchNames.append(head.name)
        for num, name in enumerate(branch_name_priority):
            if matchQuality <= num:
                continue
            matchHead = head
            matchQuality = num
        
        # If we found a head, print all; marking the one we selected
    if matchHead != 0:
        print("Detached head matching")
        for matchNm in matchNames:
            if matchNm == matchHead.name:
                print(" - " + matchNm + " *")
            else:
                print(" - " + matchNm)
        repo.head.reference = matchHead
        print()
        continue
        
    print("Detached head with no matching branches, fetching...")
    
        # Fetch from the repo's remotes to see if any repote branches
        # match our pattern
    matchNames = []
    for remote in repo.remotes:
        for fetch_info in remote.fetch():
            if fetch_info.commit.hexsha != hex:
                continue
            matchNames.append(fetch_info.ref.name)
            for num, name in enumerate(branch_name_priority):
                if matchQuality <= num:
                    continue
                matchHead = fetch_info.ref.name
                matchQuality = num
    
        # If we found a match, create a local head with that name;
        # we again print all with the selected one marked
    if matchHead != 0:
        print("Detached head matching")
        
        for matchNm in matchNames:
            if matchNm == matchHead:
                print(" - " + matchNm + " *")
            else:
                print(" - " + matchNm)
                
        branchName = matchHead.split('/', 1)[-1]
                
        for head in repo.heads:
            if head.name != branchName:
                continue
            
            commits_behind  = repo.iter_commits(branchName + '..' + matchHead)
            commits_behind_count = sum(1 for c in commits_behind)
            
            commits_ahead   = repo.iter_commits(matchHead + '..' + branchName)
            commits_ahead_count = sum(1 for c in commits_ahead)
            
            print()
            print("The branch '" + branchName + "' already exists")
            print(" " + str(commits_behind_count) + " commits behind " + str(matchHead))
            print(" " + str(commits_ahead_count) + " commits ahead " + str(matchHead))
            print()
            print("This branch will be moved to the current commit. You probably")
            print("should not want to do this if the branch is ahead.")
            print()
            if False == shared_choice.yn("Is moving this branch OK?"):
                branchName = 0
                break
            repo.delete_head(branchName)            
            
        if branchName == 0:
            break
        
        new_head = repo.create_head(branchName)
        repo.head.set_reference(new_head)
                
        print()
        continue
        
    print()
    print("The current commit cannot be set to any existing branch")
    
    branch_add = 1;
    found = 1
    while found:
        branchName = "temp-" + str(branch_add) + "-develop"
        found = 0
        for head in repo.heads:
            if head.name != branchName:
                continue
            found = 1
            break
        branch_add += 1
        
    print("We can name this HEAD '" + str(branchName) + "'")
    print()
    if False == shared_choice.yn("Is creating this branch OK?"):
        continue
        
    new_head = repo.create_head(branchName)
    repo.head.set_reference(new_head)
    
    print()
    
print("Done.")