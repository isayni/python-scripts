#!/usr/bin/env python
'''
    script to fix srt subtitle files.

    delaying the timestamps, adjusting the length
    to a stretched out movie length.
'''
import os
import sys

def printHelp():
    print('''script to fix srt subtitle files.

delaying the timestamps, adjusting the length
to a stretched out movie length.

Usage: srtfixer.py <file> [-d delay] [-e encoding] [-r ratio] [-o]

-h, --help:  print this help message
-d delay:    how much the subtitles should be delayed e.g. 3 or -2.5
-e encoding: encoding of the given file e.g. utf-8
-o:          whether to overwrite the given file
-r ratio:    length ratio between the original video and your video e.g. 1:1 or 3600:3620''')
    exit()

DELAY           = 0
ENCODING        = 'utf-8'
ORIGINAL_LENGTH = 1
LENGTH          = 1
OVERWRITE       = False

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '-h' or arg == '--help':
        printHelp()
    elif   arg == '-d': # delay in seconds
        i+=1
        DELAY = float(sys.argv[i])
    elif arg == '-e': # encoding
        i+=1
        ENCODING = sys.argv[i]
    elif arg == '-o': # overwrite file
        OVERWRITE = True
    elif arg == '-r': # length ratio
        i+=1
        t = sys.argv[i].split(':')
        ORIGINAL_LENGTH = float(t[0])
        LENGTH = float(t[1])
    elif os.path.isfile(arg):
        SRTPATH = arg
    i+=1

try:
    SRTPATH
except:
    printHelp()

FACTOR = LENGTH/ORIGINAL_LENGTH

with open(SRTPATH, 'r', encoding=ENCODING, errors='ignore') as srt:
    lines = srt.readlines()

for i in range(len(lines)):
    if "-->" in lines[i]:
        # print(lines[i])
        # 00:00:00,000 --> 00:00:00,000
        # 01234567890123456789012345678
        stseconds = float((lines[i])[0:2])*3600 + float((lines[i])[3:5]) * \
            60 + float((lines[i])[6:8]) + float((lines[i])[9:12]) * 0.001
        enseconds = float((lines[i])[17:19])*3600 + float((lines[i])[20:22]) * \
            60 + float((lines[i])[23:25]) + float((lines[i])[26:29]) * 0.001
        stseconds*=FACTOR
        stseconds+=DELAY
        enseconds*=FACTOR
        enseconds+=DELAY
        lines[i] = ("0" if int(stseconds/3600)<10 else "") + str(int(stseconds/3600)) + ":"
        stseconds -= int(stseconds/3600) * 3600
        lines[i] += ("0" if int(stseconds/60) < 10 else "") + str(int(stseconds/60)) + ":"
        stseconds -= int(stseconds/60) * 60
        lines[i] += ("0" if int(stseconds) < 10 else "") + str(int(stseconds)) + ","
        stseconds -= int(stseconds)
        lines[i] += ("00" if int(stseconds*1000) < 10 else "0" if int(stseconds*1000) < 100 else "") + str(int(stseconds*1000))
        lines[i] += " --> "
        lines[i] += ("0" if int(enseconds/3600) < 10 else "") + str(int(enseconds/3600)) + ":"
        enseconds -= int(enseconds/3600) * 3600
        lines[i] += ("0" if int(enseconds/60) < 10 else "") + str(int(enseconds/60)) + ":"
        enseconds -= int(enseconds/60) * 60
        lines[i] += ("0" if int(enseconds) < 10 else "") + str(int(enseconds)) + ","
        enseconds -= int(enseconds)
        lines[i] += ("00" if int(enseconds*1000) < 10 else "0" if int(enseconds*1000) < 100 else "") + str(int(enseconds*1000)) + "\n"

with open(SRTPATH + (".new" if not OVERWRITE else ""), 'w', encoding="utf8") as f:
    f.writelines(lines)
