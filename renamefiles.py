import os
import shutil

files = os.listdir()

for file in files:
    if '_' in file:
        src = file
        dst = file.split('_')[-1]
        shutil.move(src,dst)