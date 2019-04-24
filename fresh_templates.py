print("Checking templates...\r", end='')

import os
import sys
import shutil
import shared_choice

    # Find our startup path; by default our path + "../../"
    # This usually corresponds to the main git directory
dir_path = os.path.dirname(sys.argv[0]) + "/../../"
if len(sys.argv) > 1:
    dir_path = sys.argv[1]

exclude_dirs = [
    ".vs",
    "node_modules"
]

    # Walk through all the folders; templates must be stored
    # in a "Fresh" folder and have the suffix ".ftemplate"
    # f.i., /VS/Fresh/settings.user.ftemplate becomes
    #       /VS/settings.user
fresh_folders = []
for (root, dirs, files) in os.walk(dir_path):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for name in dirs:
        if name != "Fresh":
            continue
        fresh_folders.append(os.path.abspath(os.path.join(root, name)))
    
    # Walk through the files
fresh_files = []
for folder in fresh_folders:
    for (root, dirs, files) in os.walk(folder):
        for name in files:
            if not name.endswith(".ftemplate"):
                continue
            fresh_files.append([os.path.abspath(os.path.join(root, name)), os.path.abspath(os.path.join(root + "/../", name.rstrip(".ftemplate")))])
    
print("This script would like to copy the following templates:")
for [input, output] in fresh_files:
    print(" * " + os.path.relpath(output, dir_path))
print()
    
if False == shared_choice.yn("Is copying OK?"):
    sys.exit()
print()
    
print("Copying .ftemplate files...")
 
    # Copy the files, removing the suffix
def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)
for [input, output] in fresh_files:
    copyFile(input, output)