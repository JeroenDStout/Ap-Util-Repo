import os
import sys
import git

    # Find our startup path; by default our path + "../../"
    # This usually corresponds to the main git directory
dir_path = os.path.dirname(sys.argv[0]) + "/../../"
if len(sys.argv) > 1:
    dir_path = sys.argv[1]
dir_path = os.path.abspath(dir_path);

print()
print("~*~*~ Looking for directories ~*~*~")
print()
    
    # Walk through all directories to find a .git file
git_dirs = []
for (root, dirs, files) in os.walk(dir_path):
    for name in files:
        if name == ".git":
            git_dirs.append(os.path.abspath(root))
    
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
    
    match = 0
    matchMaster = 0
    matchMasterDet = 0
    matchDevelop = 0
    matchDevelopDet = 0
    matchNames = []
    
        # Compare the hexsha against branches;
        # we favour the main master/develop, and
        # then favour relative master/develop
    hex = repo.head.commit.hexsha
    
    for head in repo.heads:
        if head.commit.hexsha != hex:
            continue
        matchNames.append(head.name)
        if head.name == "public-master":
            matchMaster = head
        if head.name == "public-develop":
            matchDevelop = head
        if head.name.endswith("-master"):
            matchMasterDet = head
        if head.name.endswith("-develop"):
            matchDevelopDet = head
        
    match = matchMaster
    if not match:
        match = matchDevelop
    if not match:
        match = matchMasterDet
    if not match:
        match = matchDevelopDet
        
        # Print heads and correct, or complain we have no branch
    if len(matchNames) > 0:
        print("Detached head matching")
        for matchNm in matchNames:
            if matchNm == match.name:
                print(" - " + matchNm + " *")
            else:
                print(" - " + matchNm)
        repo.head.reference = match
    else:
        print("Detached head with no matching branches - no changes")
    
    print()
    
print("Done.")