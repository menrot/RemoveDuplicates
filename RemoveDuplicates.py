# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

"""
RemoveDuplicates

    Release V1.0

    Based on ccleaner duplicate finding.
        CCleaner -> Tools -> Duplicate Finder
        Find duplicate based on size and content (2 check boxes)
        Add the folder whose subtree you want to analyze and check only it

    1. Parse the txt file
    2. build a list of all duplicates
    3. Build a list of all conflicting duplicates
    3. For each tuple, decide who is the path to be kept
    4. create a BAT file to delete all teh other files.

"""


import sys
import re
import codecs
from QueryToKeep import QueryToKeep


class FileInfo(object):

    def __init__(self, listFileData):
        self.Name = listFileData[1]
        self.Path = listFileData[2]
        self.Size = listFileData[3]
        self.Date = listFileData[4]
        return(None)

    def __str__(self):
        return "File name " + str(self.Name) + " Path: " + str(self.Path) + \
               " Size: " + self.Size + " Date: " + self.Date


##
class DuplicateInstance(object):

    def __init__(self):
        self.Count = 0
        self.Dups = []
        self.tupleID = -1

    def __str__(self):
        # print the description of all the nodes in the graph
        returnStr = "\nCount " + str(self.Count)
        for i in self.Dups:
            returnStr += "\n\t" + str(self.Dupes[i])
        return returnStr

    def __len__(self):
        # returns the number of nodes in the graph
        return len(self.Dups)


    def add(self, newdup):
        # adds newdup to the instance
        self.Dups.append(newdup)
        self.Count += 1
        return

def DuplicateTuple(dupInst):
    dupsSofar = []
    for i in range(0, len(dupInst)):
        if not (dupInst[i].Path in dupsSofar): # if already in list, don't add
            dupsSofar.append(dupInst[i].Path)

    dupsSofar.sort()
    return dupsSofar

REGEX_START_INSTANCE = ur"^-----+\r$" ## line with only dashes
REGEX_FILE_IN_INSTANCE = \
    ur"^([a-z0-9\~\_\.\-\(\) ]+)\t([a-z0-9\.\-\(\)\\: ]+)\t([0-9\. ]+ [kbm]{2})\t" + \
        ur"([0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\:[0-9]{2}\:[0-9]{2} [apm]{2})"

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print "usage: RemoveDuplicates dup_text_file"
        exit()


    allDups = []
    dupTuples = []

    with codecs.open(sys.argv[1], encoding='utf-16', mode='r') as f:
        instance = False
        for line in f:

            if not(instance):
                if re.match(REGEX_START_INSTANCE, line, re.IGNORECASE) is not None:
                    # start a dup instance
                    instance = True
                    CurrentInstance = DuplicateInstance()
            else:
                lineSplitted = re.split(REGEX_FILE_IN_INSTANCE, line, flags=re.IGNORECASE)
                if len(lineSplitted) == 6:
                    # legal dup
                    CurrentInstance.add(FileInfo(lineSplitted))
                elif re.match(REGEX_START_INSTANCE, line, re.IGNORECASE) is not None:
                    # close current dup

                    dt = DuplicateTuple(CurrentInstance.Dups)
                    if not (dt in dupTuples):
                        dupTuples.append(dt)

                    CurrentInstance.tupleID = dupTuples.index(dt)
                    allDups.append(CurrentInstance)
                    CurrentInstance = DuplicateInstance() # start new instance
                else:
                    #its an error
                    print >> sys.stderr, "Unexpecetd line %s" % line

        dt = DuplicateTuple(CurrentInstance.Dups)
        if not (dt in dupTuples):
            dupTuples.append(dt)
        CurrentInstance.tupleID = dupTuples.index(dt)
        allDups.append(CurrentInstance)
        print "Finished processing the duplicates file\n"

    """

    Print results

    """

    print "number of duplicates %s " % len(allDups)

    # DupsInTuple Count how many dups in each tuple
    DupsInTuple = [0] * (len(dupTuples))
    for i in range(0, len(allDups)):
        DupsInTuple[allDups[i].tupleID] += 1

    fbat = open('./rmdups.bat', 'w+')


    fbat.write('@echo off\ncall :sub 1>rmdups.log 2>&1\nexit /b\n:sub\n') # create log file of the batch execution

    print "number of tuples %s" % len(dupTuples)
    # print dupTuples
    for i in range(0, len(dupTuples)):
        for j in range(0, len(dupTuples[i])):
            print i, j, dupTuples[i][j]
        print "Number of dups in this tuple %s" % DupsInTuple[i]

        sel = QueryToKeep(dupTuples[i])
        if sel > 0:
            print "keep  %s" % (dupTuples[i][sel-1])
            if len(dupTuples[i]) == 1:
                # remove dupes inside the folder
                for j in range(0, len(allDups)):
                    if allDups[j].tupleID == i:
                        seldel = sel - 1
                        fbat.write('del "%s\\%s"\n' % (dupTuples[i][seldel],allDups[j].Dups[sel-1].Name))
            elif len(dupTuples[i]) == 2:
                # remove dupes inside from one folder
                for j in range(0, len(allDups)):
                    if allDups[j].tupleID == i:
                        seldel = 2 - sel # delete from the other folder
                        fbat.write('del "%s\\%s"\n' % (dupTuples[i][seldel], allDups[j].Dups[sel - 1].Name))
            else:
                # remove dupes inside from two folder
                for j in range(0, len(allDups)):
                    if allDups[j].tupleID == i:
                        if sel == 1:
                            fbat.write('del "%s\\%s"\n' % (dupTuples[i][1], allDups[j].Dups[sel - 1].Name))
                            fbat.write('del "%s\\%s"\n' % (dupTuples[i][2], allDups[j].Dups[sel - 1].Name))
                        elif sel == 2:
                            fbat.write('del "%s\\%s"\n' % (dupTuples[i][0], allDups[j].Dups[sel - 1].Name))
                            fbat.write('del "%s\\%s"\n' % (dupTuples[i][2], allDups[j].Dups[sel - 1].Name))
                        elif sel ==3:
                            fbat.write('del "%s\\%s"\n' % (dupTuples[i][0], allDups[j].Dups[sel - 1].Name))
                            fbat.write('del "%s\\%s"\n' % (dupTuples[i][1], allDups[j].Dups[sel - 1].Name))
                        else:
                            print "Wrong selection %s" % sel
        else:
            print "keep None"
        print
    fbat.close()


