print("Welcome to Santo's file utility python script".center(150,'*'))
print()

import glob
import shutil
import os

ext = input('Please provide the file extension to searched and copied:\n')

ipynb = glob.glob(f'**\\*.{ext}',recursive=True)
for i in ipynb:
    print(i)

destination_folder = input('Input the Destination Folder path:\n')

for i, file in enumerate(ipynb,start=1):
    outputfile = (destination_folder+'\\'+str(i)+'_'+(file.split('\\')[-1]))
    print(outputfile)
    shutil.copyfile(file,outputfile)
    
os.chdir(destination_folder)
print('CWD'+os.getcwd())
    
with open('notes.txt','w') as f:
    f.write('COPIED FILES\n'+'\n'.join(ipynb))
print(f" Searched files with extension '.{ext}' and copied files to the input path of folder ".center(150,'='))