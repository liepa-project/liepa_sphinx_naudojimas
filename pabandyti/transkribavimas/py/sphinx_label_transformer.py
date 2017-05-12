#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import sys
import re

sphinxEntryOldRe = re.compile("^\d+: (.+)$")
sphinxEntryRe = re.compile("^([ąčęėįšųūž\w\s]+)$")
sphinxSegmentRe = re.compile("^(.+) ([\d\.]+) ([\d\.]+) [\d\.]+$")

class SphinxEntry:

    def __init__(self, name):
        self.name = name
        self.segments = []
        
    def __str__(self):
       if len(self.segments) == 0:
           return "" 
       start =self.segments[0].start
       end = self.segments[-1].end
       return start + " " + end + " " + self.name
       
class SphinxSegment:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        
    def __str__(self):
        return self.start + " " + self.end + " " + self.name

class SphinxLabelTransformer:
     
    sphinxEntry = SphinxEntry(None)
    
    def feed(self, line):
        line = line.strip()
        #print ">>>" + line
        if not line:
           return 
    
        if sphinxEntryRe.search(line) :
            previousSphinxEntry = self.sphinxEntry
            sphinxEntryMatch = sphinxEntryRe.match(line)
            self.sphinxEntry = SphinxEntry(sphinxEntryMatch.group(1))
            
            previouseStr = str(previousSphinxEntry)
            if previouseStr:
                print previouseStr
                for segment in previousSphinxEntry.segments:
                    print segment
            
        elif sphinxSegmentRe.search(line) :
           sphinxSegmentMatch = sphinxSegmentRe.match(line)
           sphinxSegment = SphinxSegment(sphinxSegmentMatch.group(1),sphinxSegmentMatch.group(2),sphinxSegmentMatch.group(3) )
           self.sphinxEntry.segments.append(sphinxSegment)
        else:
           raise Exception("\'" + line + "\' not parsed" );
         

    
def mainFile(aFile):
    inputFile = open(aFile)
    transformer = SphinxLabelTransformer()
    for line in inputFile:
        transformer.feed(line)
    transformer.feed("flush") 
    
def mainStream(aStreamLines):
    transformer = SphinxLabelTransformer()
    for line in aStreamLines:
        transformer.feed(line)
    transformer.feed("flush") 

    
if __name__ == "__main__":
    if len(sys.argv[1:]) == 1:
        if sys.argv[1] == '-':
            mainStream(sys.stdin.readlines())
        else:
            mainFile(sys.argv[1])
    else:
        print "Error. should be more params"
