#!/usr/bin/env python3
#convert bunch of json objects to json list
import sys
data = ""
for line in sys.stdin:
    data += line
print("[")
objs = data.split("\n")
for obj in objs[0:len(objs)-2]:
    print(obj+",")
print(objs[len(objs)-2])
print("]")
