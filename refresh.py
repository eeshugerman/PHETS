import sys
import os
import subprocess
from utilities import remove_files_by_type
from config import find_landmarks_c_compile_str



# remove all .pyc
for subdir, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            fname = os.path.join(subdir, file)
            os.remove(fname)
            print 'removed {}'.format(fname)



remove_files_by_type('embed/frames/', '.txt')
remove_files_by_type('embed/temp_data/', '.txt')
remove_files_by_type('phomology/temp/', '.txt')
remove_files_by_type('phomology/frames/', '.png')
remove_files_by_type('phomology/perseus/', '.txt')



print 'recompiling find_landmarks.c...'
os.chdir('phomology')
if sys.platform == "linux" or sys.platform == "linux2":
    compile_str = find_landmarks_c_compile_str['linux']
elif sys.platform == 'darwin':
    compile_str = find_landmarks_c_compile_str['macOS']
else:
    print 'Sorry, PHETS requires linux or macOS.'
    sys.exit()
subprocess.call(compile_str, shell=True)
os.chdir('..')
print 'recompilation attempt complete'

