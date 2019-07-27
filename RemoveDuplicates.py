# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility
# -*- coding: utf-8 -*-

"""
RemoveDuplicates

    Release V3.1

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



    NOTES:
        1. You need to run several times, as in one pass the use case of multiple in one folder AND instance in another folder is not handled
        2. If there are more then 2 copies in one folder - also has to run several time ccleaner
        3. Following move to Python 3:
            3.1 Convert file to UTF-8 to support CMD hebrew
            3.2 May require to NEW COURIER to registry to support Hebrew fonts


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
        self.Date = datetime.strptime(listFileData[4],'%m/%d/%Y %H:%M:%S %p')
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
        if self.Folders == other.Folders:
            return True
        else:
            return False

    def checkExclude(self, exclude_string):
        if (not self.exclude) and not(exclude_string is None): ### CHECK HERE ####
            for i in range(0, len(self.Folders)):
                for w in exclude_string.split():
                    if w.lower() in self.Folders[i].lower():
                        self.exclude = True
                        break
        return

def DuplicateTuple(dupInst):
    dupsSofar = []
    for i in range(0, len(dupInst)):
        if not (dupInst[i].Path in dupsSofar): # if already in list, don't add
            dupsSofar.append(dupInst[i].Path)

    dupsSofar.sort()
    return dupsSofar

REGEX_START_INSTANCE = r"^-----+\r$" ## line with only dashes
REGEX_FILE_IN_INSTANCE = r"^([\u0020-\u9fff]+)\t([\u0020-\u9fff]+)\t([0-9\. ]+ [kbmg]{2})\t([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4} [0-9]{1,2}\:[0-9]{2}\:[0-9]{2} [apm]{2})"

#    ur"^([a-zA-Z0-9\u0590-\u05FF\u0020-\u9fff\,\'\~\$\_\.\-\(\)\]\[\+ ]+)\t([a-zA-Z0-9\u0590-\u05FF\u0020-\u9fff\.\-\$\_\'\+\(\)\\: ]+)\t([0-9\. ]+ [kbm]{2})\t" + \
#        ur"([0-9]{2}\/[0-9]{2}\/[0-9]{2} [0-9]{1,2}\:[0-9]{2}\:[0-9]{2} [apm]{2})"


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
parser.add_argument('-x', dest='Exclude', help='Exclude tuples including any word in the text')


if __name__ == '__main__':

    print ('Remove Duplicates 3.0')  # update release number

    MyArgs = vars(parser.parse_args())

    # Code changed to handle str that are not binary
    # removed for all str - .encode('UTF-8')
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
        exit(1)

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
            print ("Threshold value wrong %s" % Threshold, file=sys.stderr)
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
                        dt.checkExclude(Exclude)
                        dupTuples.append(dt)

                    CurrentInstance.tupleID = dupTuples.index(dt)
                    allDups.append(CurrentInstance)
                    CurrentInstance = DuplicateInstance() # start new instance
                else:
                    #its an error
                    try:
                        print ("Unexpecetd line %s" % line, file=sys.stderr)
                    except Exception as e:
                        print ('Exception %s %s', (e.message, e.args), file=sys.stderr)

        dt = TupleInstance(CurrentInstance.Dups)
        if not (dt in dupTuples):
            dt.checkExclude(Exclude)
            dupTuples.append(dt)
        CurrentInstance.tupleID = dupTuples.index(dt)
        allDups.append(CurrentInstance)
        print ("Finished processing the duplicates file\n")

    """

    Print results

    """

    print ("number of duplicates %s " % len(allDups))

    # DupsInTuple Count how many dups in each tuple
    DupsInTuple = [0] * (len(dupTuples))
    for i in range(0, len(allDups)):
        # DupsInTuple[allDups[i].tupleID] += 1
        dupTuples[allDups[i].tupleID].DupsInTuple += 1

    bat_file = './rmdups.bat'
    fbat = open(bat_file, 'w+')


    fbat.write('@echo off\ncall :sub 1>rmdups.log 2>&1\nexit /b\n:sub\n@echo on\nCHCP 65001\necho *** start delete\n') # create log file of the batch execution

    print ("number of tuples %s" % len(dupTuples))
    # print dupTuples
    for i in range(0, len(dupTuples)):
        #if DupsInTuple[i] > Threshold and(OnlySingle and len(dupTuples[i])==1 or not OnlySingle):
        if dupTuples[i].DupsInTuple > Threshold and (OnlySingle and len(dupTuples[i].Folders) == 1 or not OnlySingle) and  not(dupTuples[i].exclude):
            for j in range(0, len(dupTuples[i].Folders)):
                print(i, j, dupTuples[i].Folders[j])
            print ("Number of dups in this tuple %s and exclude is %s" % (dupTuples[i].DupsInTuple,dupTuples[i].exclude))

            if DoBatFile:
                sel = QueryToKeep(dupTuples[i].Folders)
            else:
                sel = 0
            if sel < 0:
                break
            if sel > 0:
                print ("keep  %s" % (dupTuples[i].Folders[sel-1]))
                if len(dupTuples[i].Folders) == 1:
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
                                    fbat.write('del "%s\\%s"\n' % (dupTuples[i].Folders[0], allDups[j].Dups[kSel].Name))
                                else:
                                    ToBeDeletedFolder = "\ToBe Deleted" + dupTuples[i].Folders[0][2:]
                                    fbat.write('md "%s" 2>nul\n' % ToBeDeletedFolder)
                                    fbat.write('move "%s\\%s" "%s"\n' % (dupTuples[i].Folders[0][2:],allDups[j].Dups[kSel].Name, ToBeDeletedFolder))
                            else:
                                print ('Wrong sel')
                elif len(dupTuples[i].Folders) == 2:
                    # remove dupes inside from one folder
                    for j in range(0, len(allDups)):
                        if allDups[j].tupleID == i:
                            seldel = 2 - sel # delete from the other folder
                            for k in range(0, len(allDups[j].Dups)):
                                if dupTuples[i].Folders[seldel] == allDups[j].Dups[k].Path:
                                    if DoDelete:
                                        fbat.write('del "%s\\%s"\n' % (dupTuples[i].Folders[seldel], allDups[j].Dups[k].Name))
                                    else:
                                        ToBeDeletedFolder = "\ToBe Deleted" + dupTuples[i].Folders[seldel][2:]
                                        fbat.write('md "%s" 2>nul\n' % ToBeDeletedFolder)
                                        fbat.write('move "%s\\%s" "%s"\n' % (dupTuples[i].Folders[seldel][2:], allDups[j].Dups[k].Name, ToBeDeletedFolder))
                else:
                    # remove dupes inside from two folder
                    for j in range(0, len(allDups)):
                        if allDups[j].tupleID == i:
                            for k in range(0, len(allDups[j].Dups)):
                                for m in range(0, len(dupTuples[i].Folders)):
                                    if (sel-1) != m:
                                        if dupTuples[i].Folders[m] == allDups[j].Dups[k].Path:
                                            if DoDelete:
                                                fbat.write('del "%s\\%s"\n' % (dupTuples[i].Folders[m], allDups[j].Dups[k].Name))
                                            else:
                                                ToBeDeletedFolder = "\ToBe Deleted" + dupTuples[i].Folders[m][2:]
                                                try: ## To overcomey ASCII issues
                                                    fbat.write('md "%s" 2>nul\n' % ToBeDeletedFolder)
                                                    fbat.write('move "%s\\%s" "%s"\n' % (
                                                        dupTuples[i].Folders[m][2:], allDups[j].Dups[k].Name, ToBeDeletedFolder))
                                                except Exception as e:
                                                    print ('Exception %s %s', e.message, e.args, file=sys.stderr)


            else:
                print ("Skip - nothing deleted")
            print()


    fbat.write('echo *** end delete')
    fbat.close()

    # Convert file to UTF-8 to support CMD hebrew
    # May require to NEW COURIER to registry to support Hebrew fonts
    with codecs.open(bat_file, 'r', encoding='ansi') as file:
        lines = file.read()

    # write output file
    with codecs.open(bat_file, 'w', encoding='utf8') as file:
        file.write(lines)


