# RemoveDuplicate
A utility to analyze and remove duplicates based on ccleaner

Documentation can be seen using PYDOC

## Note 

## Release History
	2018-05-26    Release 0.1   Analysis complete
	2018-06-02 ** Release 1.0** Working release
	2019-07-26	  Release 3.0   Moved to Python 3 (and support Hebrew in CMD)
	2020-06-06    Release 3.2   Fixed logic of keeping the oldest release in a folder. Added -P to command line.

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
6. In case of a single folder, the files deleted are the newer ones and if datetime equal, the ones with longer file name (the file name length is not always optimal)
	this logic was bugged and fixed in 3.2. Also added -P to remove only files with '(nn)' in their name. 
7. Following move to Python 3:
       3.1 Convert file to UTF-8 to support CMD Hebrew
       3.2 May require to NEW COURIER to registry to support Hebrew fonts


### Usage Note
**** The need to run several times was fixed in 3.2

### Final removal
The utility creates `rmdup.bat`, which creates log file as `rmdup.log`
Review the `BAT` file, and then run it.

## Environment ###

