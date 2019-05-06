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

print("Looking for [custom_build_tool.xml]...        \r", end='')

    # Walk through all the folders; any file that is called
    # custom_build_tool.xml be used
cb_files = []
for (root, dirs, files) in os.walk(dir_path):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for name in files:
        if name != "custom_build_tool.xml":
            continue
        for (_root, _dirs, _files) in os.walk(root):
            for _name in _files:
                if not _name.endswith("vcxproj"):
                    continue
                cb_files.append( ( os.path.abspath(os.path.join(root, name)), os.path.abspath(os.path.join(_root, _name)) ) );
        break;
    
print("This script would like to modify the following projects:")
for [input, output] in cb_files:
    print(" * " + os.path.relpath(output, dir_path))
print()
    
if False == shared_choice.yn("Is modifying OK?"):
    sys.exit()
print()
    
print("Modifying files...")
        
import xml.etree.ElementTree as ET
import re

for [input, output] in cb_files:
    print("                                        \r", end='')
    print(os.path.relpath(output, dir_path) + "\r", end='')
    
    tool_setup = ET.parse(input)
    vs_project = ET.parse(output)

    prefix_replacement = []

    for search in tool_setup.getroot():
        name = search.attrib["path"]
        prefix_replacement += [( name.replace("\\", "\\\\").replace(".", "\\.").replace("*", ".*"), list(search) )]
        
    ET.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
        
    for group in vs_project.getroot().findall("{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup"):
        for item in ( group.findall("{http://schemas.microsoft.com/developer/msbuild/2003}None")
                      + group.findall("{http://schemas.microsoft.com/developer/msbuild/2003}CustomBuild") ):
            att = item.attrib["Include"];
            for search, replacement in prefix_replacement:
                if not re.search(search, att):
                    continue;
                item.clear()
                item.attrib["Include"] = att;
                item.tag = "CustomBuild"
                item.extend(replacement)
        
    vs_project.write(output, encoding='utf-8', method='xml')
    
print("Done.                                                    \r", end='')