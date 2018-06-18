# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

"""
RemoveDuplicates

    Release V1.0

    Based on ccleaner duplicate finding.
        CCleaner -> Tools -> Duplicate Finder
        Find duplicate based on size and content (2 check boxes)
        Add the folder whose subtree you want to analyze and check only it
        Save text file

    1. Parse the txt file
    2. build a list of all duplicates
    3. Build a list of all conflicting duplicates
    3. For each tuple, decide who is the path to be kept
    4. create a BAT file to delete all the other files.
        4.1 In case of a single folder, the files deleted are the newer ones and if datetme equal, the ones with longer file name
            (the file name length is not always optimal)



    NOTE:
        You need to run several times, as in one pass the use case of multiple in one folder AND instance in another folder is not handled
        If there are more then 2 copies in one folder - also has to run several time ccleaner
"""


import sys
import re
import codecs
from datetime import datetime
from QueryToKeep import QueryToKeep
import argparse
import os


class FileInfo(object):

    def __init__(self, listFileData):
        self.Name = listFileData[1]
        self.Path = listFileData[2]
        self.Size = listFileData[3]
        self.Date = datetime.strptime(listFileData[4],'%d/%m/%y %H:%M:%S %p')
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


class TupleInstance(object):

    def __init__(self, dupInst):
        self.Folders = []
        self.exclude = False
        self.DupsInTuple = 0

        for i in range(0, len(dupInst)):
            if not (dupInst[i].Path in self.Folders):  # if already in list, don't add
                self.Folders.append(dupInst[i].Path)
        self.Folders.sort()
        return

    def __eq__(self, other):
        if self.DupsInTuple == other.DupsInTuple and self.exclude == other.exclude and self.Folders == other.Folders:
            return True
        else:
            return False


def DuplicateTuple(dupInst):
    dupsSofar = []
    for i in range(0, len(dupInst)):
        if not (dupInst[i].Path in dupsSofar): # if already in list, don't add
            dupsSofar.append(dupInst[i].Path)

    dupsSofar.sort()
    return dupsSofar

REGEX_START_INSTANCE = ur"^-----+\r$" ## line with only dashes
REGEX_FILE_IN_INSTANCE = \
    ur"^([a-z0-9\~\_\.\-\(\) ]+)\t([a-z0-9\.\-\_\'\+\(\)\\: ]+)\t([0-9\. ]+ [kbm]{2})\t" + \
        ur"([0-9]{2}\/[0-9]{2}\/[0-9]{2} [0-9]{1,2}\:[0-9]{2}\:[0-9]{2} [apm]{2})"

### Usage RemoveDuplicates.py RootFolder -r
parser = argparse.ArgumentParser(description='Create BAT file to Delete duplicates base on DUPFILE')
parser.add_argument('DupFile', metavar='DupFile', type=str,
                    help='the file holding dups based on CCleaner')
parser.add_argument('-B', dest='DoBatFile', action='store_true',  # By default - Dont create BAT
                    help='When set- create the bat file')
parser.add_argument('-D', dest='DoDelete', action='store_true',  # By default - move. when set - delete
                    help='When set- Delete the file, otherwise move it')
parser.add_argument('-s', dest='OnlySingle', action='store_true',  # By default - not only single folder
                    help='Process only within folders dup')
parser.add_argument('-T', dest='Threshold', help='Set Minimal dups in tuple to handle')
parser.add_argument('-x', dest='Exclude', help='Exclude tuples including the text')


if __name__ == '__main__':

    print 'Remove Duplicates 2.0'  # update release number

    MyArgs = vars(parser.parse_args())

    # create variables
    locals().update(MyArgs)

    origDir = os.getcwd()

    allDups = []
    dupTuples = []
    if Threshold is None:
        Threshold = 0
    else:
        try:
            Threshold = int(Threshold)
        except:
            print >> sys.stderr, "Threshold value wrong %s" % Threshold
            Threshold = 0


    with codecs.open(DupFile, encoding='utf-16', mode='r') as f:
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

                    dt = TupleInstance(CurrentInstance.Dups)
                    if not (dt in dupTuples):
                        dupTuples.append(dt)

                    CurrentInstance.tupleID = dupTuples.index(dt)
                    allDups.append(CurrentInstance)
                    CurrentInstance = DuplicateInstance() # start new instance
                else:
                    #its an error
                    print >> sys.stderr, "Unexpecetd line %s" % line

        dt = TupleInstance(CurrentInstance.Dups)
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
        # DupsInTuple[allDups[i].tupleID] += 1
        dupTuples[allDups[i].tupleID].DupsInTuple += 1


    fbat = open('./rmdups.bat', 'w+')


    fbat.write('@echo off\ncall :sub 1>rmdups.log 2>&1\nexit /b\n:sub\necho *** start delete\n') # create log file of the batch execution

    print "number of tuples %s" % len(dupTuples)
    # print dupTuples
    for i in range(0, len(dupTuples)):
        #if DupsInTuple[i] > Threshold and(OnlySingle and len(dupTuples[i])==1 or not OnlySingle):
        if dupTuples[i].DupsInTuple > Threshold and (OnlySingle and len(dupTuples[i]) == 1 or not OnlySingle):
            for j in range(0, len(dupTuples[i].Folders)):
                print i, j, dupTuples[i].Folders[j]
                #dupTuples[i].exclude = dupTuples[i].exclude or (Exclude in dupTuples[i][j].lower())
            print "Number of dups in this tuple %s" % dupTuples[i].DupsInTuple

            if DoBatFile:
                sel = QueryToKeep(dupTuples[i])
            else:
                sel = 0
            if sel < 0:
                break
            if sel > 0:
                print "keep  %s" % (dupTuples[i][sel-1])
                if len(dupTuples[i]) == 1:
                    # remove dupes inside the folder
                    for j in range(0, len(allDups)):
                        if allDups[j].tupleID == i:
                            if sel == 1:
                                kDate = datetime(2100, 1, 1, 1, 1, 1)
                                kSel = 0
                                for k in range(0, len(allDups[j].Dups)):
                                    if allDups[j].Dups[k].Date < kDate:
                                        # select oldest name to keep
                                        kDate = allDups[j].Dups[k].Date
                                        kSel = k
                                    elif allDups[j].Dups[k].Date == kDate:
                                        if len(allDups[j].Dups[k].Name) > len(allDups[j].Dups[kSel].Name):
                                            # select longest name to delete
                                            kDate = allDups[j].Dups[k].Date
                                            kSel = k
                                if DoDelete:
                                    fbat.write('del "%s\\%s"\n' % (dupTuples[i][0], allDups[j].Dups[kSel].Name))
                                else:
                                    ToBeDeletedFolder = "\ToBe Deleted" + dupTuples[i][0][2:]
                                    fbat.write('md "%s" 2>nul\n' % ToBeDeletedFolder)
                                    fbat.write('move "%s\\%s" "%s"\n' % (dupTuples[i][0][2:],allDups[j].Dups[kSel].Name, ToBeDeletedFolder))
                            else:
                                print 'Wrong sel'
                elif len(dupTuples[i]) == 2:
                    # remove dupes inside from one folder
                    for j in range(0, len(allDups)):
                        if allDups[j].tupleID == i:
                            seldel = 2 - sel # delete from the other folder
                            for k in range(0, len(allDups[j].Dups)):
                                if dupTuples[i][seldel] == allDups[j].Dups[k].Path:
                                    if DoDelete:
                                        fbat.write('del "%s\\%s"\n' % (dupTuples[i][seldel], allDups[j].Dups[k].Name))
                                    else:
                                        ToBeDeletedFolder = "\ToBe Deleted" + dupTuples[i][seldel][2:]
                                        fbat.write('md "%s" 2>nul\n' % ToBeDeletedFolder)
                                        fbat.write('move "%s\\%s" "%s"\n' % (dupTuples[i][seldel][2:], allDups[j].Dups[k].Name, ToBeDeletedFolder))
                else:
                    # remove dupes inside from two folder
                    for j in range(0, len(allDups)):
                        if allDups[j].tupleID == i:
                            for k in range(0, len(allDups[j].Dups)):
                                for m in range(0, len(dupTuples[i])):
                                    if (sel-1) <> m:
                                        if dupTuples[i][m] == allDups[j].Dups[k].Path:
                                            if DoDelete:
                                                fbat.write('del "%s\\%s"\n' % (dupTuples[i][m], allDups[j].Dups[k].Name))
                                            else:
                                                ToBeDeletedFolder = "\ToBe Deleted" + dupTuples[i][m][2:]
                                                fbat.write('md "%s" 2>nul\n' % ToBeDeletedFolder)
                                                fbat.write('move "%s\\%s" "%s"\n' % (
                                                    dupTuples[i][m][2:], allDups[j].Dups[k].Name, ToBeDeletedFolder))


            else:
                print "keep None"
                print


    fbat.write('echo *** end delete')
    fbat.close()


