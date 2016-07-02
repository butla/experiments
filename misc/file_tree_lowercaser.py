# created by Michal Bultrowicz
import os
import shutil

# doesn't change names of elemements that are in changed dirs
for path, dirs, files in os.walk('.'):
    if path[0] == '.': path = path[1:]
    if path and path[0] == os.sep: path = path[1:]
    
    for element in files+dirs:
        try:
            inPath = os.path.join(path, element)
            outPath = os.path.join(path, element.lower())
            #shutil.copy(inPath, outPath)
            os.rename(inPath, outPath)
        except shutil.Error as ex:
            print(ex)