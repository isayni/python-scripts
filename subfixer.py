#!/usr/bin/env python
import os
import sys

if len(sys.argv) == 1:
    print("no subtitles file path given")
    exit()
srtpath = os.getcwd() + '/' + sys.argv[1]
orlength = float(input('original movie length'))
length = float(input('your movie version length'))
delay = float(input('delay: '))
encoding = input("encoding: ")
factor = length/orlength
print("\n")

srt = open(srtpath, encoding=encoding, errors='ignore')
lines = srt.readlines()
srt.close()

for i in range(lines.__len__()):
    if "-->" in lines[i]:
        # print(lines[i])
        # 00:00:00,000 --> 00:00:00,000
        # 01234567890123456789012345678
        stseconds = float((lines[i])[0:2])*3600 + float((lines[i])[3:5]) * \
            60 + float((lines[i])[6:8]) + float((lines[i])[9:12]) * 0.001
        enseconds = float((lines[i])[17:19])*3600 + float((lines[i])[20:22]) * \
            60 + float((lines[i])[23:25]) + float((lines[i])[26:29]) * 0.001
        stseconds*=factor
        stseconds+=delay
        enseconds*=factor
        enseconds+=delay
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

with open(srtpath + ".new", 'w', encoding="utf8") as f:
    f.writelines(lines)
print("done")
