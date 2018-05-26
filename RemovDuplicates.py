# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import sys
import re
import codecs


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


REGEX_START_INSTANCE = ur"^-----+\r$" ## line with only dashes
REGEX_FILE_IN_INSTANCE = \
    ur"^([a-z0-9\~\_\.\-\(\) ]+)\t([a-z0-9\.\-\(\)\\: ]+)\t([0-9\. ]+ [kbm]{2})\t" + \
        ur"([0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{1,2}\:[0-9]{2}\:[0-9]{2} [apm]{2})"

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print "usage: RemoveDuplicates dup_text_file"
        exit()


    allDups = []

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
                    allDups.append(CurrentInstance)
                    CurrentInstance = DuplicateInstance() # start new instance
                else:
                    #its an error
                    print >> sys.stderr, "Unexpecetd line %s" % line
        allDups.append(CurrentInstance)
        print "End of File"

    print "number of duplicates %s " % len(allDups)








#
#
#Read duplicates file and return structure as follows:
#
# File count
# [Files] File name, path]
#
#present folders and allow to select which one to keep
#
#process duplicates structure..:
