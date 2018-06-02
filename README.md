# RemoveDuplicate
A utility to analyze and remove duplicates based on ccleaner

Documentation can be seen using PYDOC

## Note 

## Release History
	2018-05-26    Release 0.1   Analysis complete
	2018-06-02 ** Release 1.0** Working release

## Usage ##



### Based on CCleaner duplicate finding.
In CCleaner do the following:

- CCleaner -> Tools -> Duplicate Finder
- Find duplicate based on size and content (2 check boxes)
- Add the folder whose subtree you want to analyze and check only it
- Save text file (`duplicate.txt`)

### Utility logic 

1. Parse the txt file received from CCleaner
2. build a list of all duplicates
3. Build a list of all conflicting duplicates
4. For each tuple, decide who is the path to be kept
5. create a BAT file to delete all the other files.
6. In case of a single folder, the files deleted are the newer ones and if datetןme equal, the ones with longer file name (the file name length is not always optimal)


### Usage Note
1. You need to run several times, as in one pass the use case of multiple in one folder AND instance in another folder is not handled
1. If there are more then 2 copies in one folder - also has to run several time ccleaner

### Final removal
The utility creates `rmdup.bat`, which creates log file as `rmdup.log`
Review the `BAT` file, and then run it.

## Environment ###

