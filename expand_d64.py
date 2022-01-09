#!/usr/bin/env python3

import sys
import os
import re

C1541 = "/usr/local/bin/c1541"
PETCAT = "/usr/local/bin/petcat"
CBM_TOKENIZE = "../cbm_tokenize.py"

for f in [C1541, PETCAT, CBM_TOKENIZE]:
    if not os.path.exists(f):
        print("{} not found".format(f))
        sys.exit()

if (len(sys.argv) != 2):
    print("usage: expand_d64 <d64 image file>")
    sys.exit()

disk = sys.argv[1]

print("\n[Using disk: {}]\n".format(disk))

if not os.path.exists(disk):
    print("{} not found".format(disk))
    sys.exit()

dirlist = os.popen(C1541 + " -attach " + disk + " -list").read()

dirlist = dirlist.split('\n')
header = dirlist.pop(0)

# print header
print("[{}]".format(header))

# header = [0 "X               " YY ZZ] 
# diskname = "X.YY"
diskbasename = header.split('"')[1].strip()
diskdotname = header.split('"')[2].split()[0].strip()
diskname = diskbasename + "." + diskdotname 
diskname.strip()

# Get all file names on disk
files = {} 
for f in dirlist:
    if re.match(".*blocks free.*", f) or f == "":
        continue
    # (), means keep regex match in split
    unpacked = re.split('(".*")', f)
    #print(unpacked)
    for index in range(len(unpacked)):
        unpacked[index] = unpacked[index].strip()
    
        size, filename, ftype = unpacked
        files[filename] = { 'size':size, 'type':ftype }


for k in files.keys():
   print("{:<20} {:<3} blocks {:<3}".format(k, files[k]['size'], files[k]['type']))

print("\n[{}]\n".format(diskname))





while 1:
    print("use \"{}\" as disk name? ".format(diskname),end='')
    y_or_n = input()
    print("")

    if y_or_n != "y":
        print("Input new name: ",end='')
        diskname=input()
        print("")
    else:
        break
    
print("disk name \"{}\"".format(diskname))

if os.path.exists(diskname):
    print("\"{}\" file already exists!".format(diskname))
    print("exiting...")
    sys.exit()

if os.system("mkdir " + "\"" + diskname + "\"") != 0:
    print("couldn't create {} directory!".format(diskname))
    print("exiting...")
    sys.exit()

# Extract disk contents
try:
    os.chdir(diskname)
except FileNotFoundError:
    print("couldn't change to {} directory!".format(diskname))
    print("exiting...")
    sys.exit()

# At this point, script is inside new directory, no more safety checks
newdir = os.popen("pwd").read()
print("Expanding into:", newdir)

EXTRACT_DISK_PRG = C1541 + " -attach ../" + disk + " -read "
EXTRACT_DISK_SEQ = C1541 + " -attach ../" + disk + " -extract "

for k in files.keys():
    if files[k]['type'] == "prg":
        command = EXTRACT_DISK_PRG + k + " " + k + ".prg"
        print(command)
        os.system(command)
    if files[k]['type'] == "seq":
        print("skipping: {}.seq".format(k))
