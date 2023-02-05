## Sentence Splitter

The code in sentence_split.py takes a body of text from an input file and 
writes the text with the sentences split with each sentence on new line to
the output file. This file is given the same file name with _split added.

This script makes use of the regular expressions module to find occurrences of periods,
quotation marks and exclamation marks that are not the end of a sentence. Examples are
prefixes and suffices such as Dr. or Jr. and also abbreviations. This script does not
account for occurrences of these at the end of a sentence due to them being unlikely.
In the event that this happens the options are limited to checking the next work and
understanding if it is the start of a sentence i.e. capitalized and not a name.

The script has been set up to run in 2 ways:

1. Command line argument: The script can be ran from the command line in an environemnt that contains Python. python sentence_split.py **<input_filename_here>**. The file will be read in and the filename + _split will be written to the current directory with the output.
2. Manual entry: At the bottom of the file, the filename variable can be changed to the input file you wish to use. If a filename is defined it is used when the script is ran. The output is as before, input filename + _split

Folder contents:

+ [Sentence split - Python file](sentence_split.py)
+ [Sample input](input.txt)
+ [Sample output](input_split.txt)