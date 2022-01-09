#!/usr/bin/env python3

import sys
import os
import re

# Set programs here (vice includes c1541, petcat)
C1541 = "/usr/local/bin/c1541"
PETCAT = "/usr/local/bin/petcat"
CBM_TOKENIZE = "/home/burin/src/commodore64/cbm_tokenize.py"

for f in [C1541, PETCAT, CBM_TOKENIZE]:
    if not os.path.exists(f):
        print("{} not found".format(f))
        sys.exit()

if (len(sys.argv) != 2):
    print("usage: expand_d64 <d64 image file>")
    sys.exit()

# Read in d64 name from command line
disk = sys.argv[1]

print("\n[Using disk: {}]\n".format(disk))

if not os.path.exists(disk):
    print("{} not found".format(disk))
    sys.exit()

# Get disk directory listing from c1541
dirlist = os.popen(C1541 + " -attach " + disk + " -list").read()

dirlist = dirlist.split('\n')
header = dirlist.pop(0)  # header summary is first line of dir listing
print("[{}]".format(header))


# Create a name for expansion directory based on header info
#
#   header = [0 "X               " YY ZZ]
#   diskname = "X.YY"
#
diskbasename = header.split('"')[1].strip()
diskdotname = header.split('"')[2].split()[0].strip()
diskname = diskbasename + "." + diskdotname 
diskname.strip()

# Gather all file names on disk
files = {} 
for f in dirlist:
    # Skip summary line at end of dir listing
    if re.match(".*blocks free.*", f) or f == "":
        continue

    # Split up entries of form [NN "filename" type]
    #   (), means keep regex match in split
    unpacked = re.split('(".*")', f)

    for index in range(len(unpacked)):
        unpacked[index] = unpacked[index].strip()
    
        size, filename, ftype = unpacked
        files[filename] = { 'size':size, 'type':ftype }


# Summarize all files
for k in files.keys():
   print("{:<20} {:<3} blocks {:<3}".format(k, files[k]['size'], files[k]['type']))

# New disk directory name
print("\n[{}]\n".format(diskname))

# Approve new directory name
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
    
# Summarize directory name again, just because
print("disk name \"{}\"".format(diskname))

# Due dillegence, so we don't bork up filesystem
if os.path.exists(diskname):
    print("\"{}\" file already exists!".format(diskname))
    print("exiting...")
    sys.exit()

if os.system("mkdir " + "\"" + diskname + "\"") != 0:
    print("couldn't create {} directory!".format(diskname))
    print("exiting...")
    sys.exit()

try:
    os.chdir(diskname)
except FileNotFoundError:
    print("couldn't change to {} directory!".format(diskname))
    print("exiting...")
    sys.exit()

# Extract disk contents
#   At this point, script is inside new directory, no more safety checks
newdir = os.popen("pwd").read()
print("Expanding into:", newdir)


# Extract .prg, .seq files into new directory
EXTRACT_DISK_FILE = C1541 + " -attach ../" + disk + " -read "

for k in files.keys():
    if files[k]['type'] == "prg":
        command = EXTRACT_DISK_FILE + k + " " + k + ".prg"
        print(command)
        os.system(command)
    if files[k]['type'] == "seq":
        extract_command = '"' + k.strip('"') + ",s" + '"'
        command = EXTRACT_DISK_FILE + extract_command + " " + k + ".seq"
        print(command)
        os.system(command)

# make "source" directory and populate from "binaries"
if os.system("mkdir source") != 0:
    print("couldn't create \"source\" directory!")
    sys.exit()

EXTRACT_AND_PROCESS_SOURCE = PETCAT + " | " + CBM_TOKENIZE + " > source/"
for k in files.keys():
    if files[k]['type'] == "prg":
        command = "cat " + k + ".prg | " + EXTRACT_AND_PROCESS_SOURCE + k + ".bas"
        print(command)
        os.system(command)
    if files[k]['type'] == "seq":
        print("skipping {}.seq, don't know how to convert".format(k))

