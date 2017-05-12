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

class SphinxPraatTransformer:
     
    sphinxEntry = SphinxEntry(None)
    phrases = []
    lrtList = []
    sizeInSec = 0.0
    frame_rate = .01
    
    def feed(self, line):
        line = line.strip()
        #print ">>>" + line
        
        if not line:
           return 
        if line.find(">>>lrt: ") == 0:
            self.lrtList.append(line.replace(">>>lrt: ",""))
            return
        if line.find(">>>sizeInSec: ") == 0:
            self.sizeInSec = float(line.replace(">>>sizeInSec: ",""))
            return

    
        if sphinxEntryRe.search(line) :
            previousSphinxEntry = self.sphinxEntry
            self.phrases.append(previousSphinxEntry)
            sphinxEntryMatch = sphinxEntryRe.match(line)
            self.sphinxEntry = SphinxEntry(sphinxEntryMatch.group(1))

            
#            previouseStr = str(previousSphinxEntry)
#            if previouseStr:
#                print previouseStr
#                for segment in previousSphinxEntry.segments:
#                    print segment
            
        elif sphinxSegmentRe.search(line) :
            sphinxSegmentMatch = sphinxSegmentRe.match(line)
            sphinxSegment = SphinxSegment(sphinxSegmentMatch.group(1),sphinxSegmentMatch.group(2),sphinxSegmentMatch.group(3) )
            self.sphinxEntry.segments.append(sphinxSegment)
        else:
            raise Exception("\'" + line + "\' not parsed" );
         
    def toPraat(self):
        print """File type = "ooTextFile"
Object class = "TextGrid"
"""

        print """xmin = {xmin} 
xmax = {xmax} 
tiers? <exists> 
size = 2
item []: """.format(xmin=0, xmax=self.sizeInSec)

        segment_out = ""

        segment_index = 1
        segment_last_time=0
        for phrase in self.phrases:
            if not phrase.segments:
                continue
            for segment in phrase.segments:
                segment_out += """        intervals [{index}]:
                xmin = {xmin} 
                xmax = {xmax} 
                text = "{phrase_text}"\n""".format(index=segment_index,xmin=segment_last_time, xmax=segment.start, phrase_text="") 
                segment_index += 1
                
                segment_name = segment.name.replace("<sil>","")
                segment_out += """        intervals [{index}]:
                xmin = {xmin} 
                xmax = {xmax} 
                text = "{segment_name}"\n""".format(index=segment_index,xmin=segment.start, xmax=segment.end, segment_name=segment_name ) 
                segment_index += 1
                segment_last_time= segment.end
        segment_out += """        intervals [{index}]:
                xmin = {xmin} 
                xmax = {xmax} 
                text = "{phrase_text}"\n""".format(index=segment_index,xmin=segment_last_time, xmax=self.sizeInSec, phrase_text="") 
        segment_index += 1
                
        segment_out = """    item [1]:
        class = "IntervalTier" 
        name = "Word" 
        xmin = 0 
        xmax =  {xmax}
        intervals: size = {segment_index}\n""".format(xmin=0,xmax=self.sizeInSec, segment_index=segment_index-1) + segment_out

        print segment_out

        phrase_out = ""
        
        phrase_index = 1
        phrase_last_time=0
        for phrase in self.phrases:
            if not phrase.segments:
                continue            
            phrase_out += """        intervals [{index}]:
            xmin = {xmin} 
            xmax = {xmax} 
            text = "{phrase_text}"\n""".format(index=phrase_index,xmin=phrase_last_time, xmax=phrase.segments[0].start, phrase_text="") 
            phrase_index += 1

            phrase_out += """        intervals [{index}]:
            xmin = {xmin} 
            xmax = {xmax} 
            text = "{phrase_text}"\n""".format(index=phrase_index,xmin=phrase.segments[0].start, xmax=phrase.segments[-1].end, phrase_text=phrase.name) 
            phrase_index += 1
            phrase_last_time= phrase.segments[-1].end
        
        phrase_out += """        intervals [{index}]:
            xmin = {xmin} 
            xmax = {xmax} 
            text = "{phrase_text}"\n""".format(index=phrase_index,xmin=phrase_last_time, xmax=self.sizeInSec, phrase_text="") 
        phrase_index += 1
        
        phrase_out = """    item [2]:
        class = "IntervalTier" 
        name = "Phrase" 
        xmin = 0 
        xmax =  {xmax}
        intervals: size = {phrase_len}\n""".format(xmin=0,xmax=self.sizeInSec, phrase_len=phrase_index-1) +phrase_out

        print phrase_out
        
    def printVad(self):
        with open("/tmp/vad.txt", "w") as file:
            message="""File type = "ooTextFile"
Object class = "Sound 2"

0
{sec_len}
{lrt_len}
{frame_rate:.2e}
3.125e-05
1
1
1
1
1
""".format(sec_len=self.sizeInSec,lrt_len=len(self.lrtList), frame_rate=self.frame_rate)
            file.write(message)
            for lrt in self.lrtList:
                file.write("{lrt}\n".format(lrt=lrt))
        
        
def mainFile(aFile):
    inputFile = open(aFile)
    transformer = SphinxPraatTransformer()
    for line in inputFile:
        transformer.feed(line)
    transformer.feed("flush") 
    transformer.toPraat()
    transformer.printVad()
    
def mainStream(aStreamLines):
    transformer = SphinxPraatTransformer()
    for line in aStreamLines:
        transformer.feed(line)
    transformer.feed("flush")
    transformer.toPraat()
    transformer.printVad()

    
if __name__ == "__main__":
    if len(sys.argv[1:]) == 1:
        if sys.argv[1] == '-':
            mainStream(sys.stdin.readlines())
        else:
            mainFile(sys.argv[1])
    else:
        print "Error. should be more params"
