#!/usr/bin/env python3

#Part 2 of the template summary script.
#Requires the file generated by part 1 as an input
#File format is newline-delimited strings of interesting named-entity/verb pairs.
#Warning: loads full file into memory.

inFile = "templateProcessOutput.txt"
namedEntityFile = "namedEntityResults.txt"

import re

def entity(str):
    return str.split('|')[1]

def subject(str):
    return str.split('|')[0]

def mergeEnt(str):
    temp = str.split('|')
    return temp[0]+" "+temp[1]

def look(strings, searchStr):
    list = []
    for s in strings:
        if searchStr in s:
            list.append(s)
    return list

def lookMulti(strings, searchList):
    list = []
    first = True
    for searchItem in searchList:
        if first:
            first = False
            list = look(strings, searchItem)
        else:
            list = look(list, searchItem) #search only in previous good results
    return list

def most_common(lst):
    return max(set(lst), key=lst.count)

def intelliGrab(strings, searchList, regex, getEntity):
    list = lookMulti(strings, searchList)
    if getEntity is "entity":
        list = [entity(x) for x in list]
    elif getEntity is "subject":
        list = [subject(x) for x in list]
    else: #both
        list = [mergeEnt(x) for x in list]
    #sort on len smallest first (smaller results are more releveant, will be picked up by regex first)
    list.sort(key = len)

    #match based on regex
    return re.search(regex, str(list)).group()


if __name__ == "__main__":
    strings = []
    sentences = [] #list of sentences, where periods mean new sentence
    wordTypes = [] #word:type tuple list

    with open(inFile) as f:
        for line in f:
            strings.append(line[:-1].lower())
    with open(namedEntityFile) as f:
        #load file as sentences only and as word:type pairs
        sentence = ""
        for line in f:
            word = line.split(" ")
            if len(word) is 2:
                sentence = sentence + word[0]
                if word[0] is ".":
                    sentences.append(sentence)
                    sentence=""
                wordTypes.append((word[0],word[1]))

    print(lookMulti(strings, ["deaths", "michael"]))
    windspeed = intelliGrab(strings, ["winds", "mph"], "\d+ mph", "entity")
    deaths = intelliGrab(strings, ["deaths"], "\d+ deaths", "entity")
    damage = intelliGrab(strings, ["damage"], ".+", "merge")
    #for damage, try running through intelligrab results and pick one with a gpe (run thru spacy again)

    print("The wind speeds were measured to be "+windspeed+".")
    print("The hurricane caused "+deaths+".")
    print("An extensive source of damage was "+damage+".")
