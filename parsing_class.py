import sys
import re
from pathlib import Path
import os.path
from enum import Enum

class ParsedClassMember:
    type = ""
    name = ""
    def debug(self):
        print("Member {}-{}".format(self.type, self.name))

class ParsedClass:
    def __init__(self, new_classname):
        self.classname = new_classname
        self.members = []


#constants definition
KEYWORD_CLASS = "class"
KEYWORD_TEMPLATE = "template"
MACRO_REFLECT_CLASS = "REFLECT_CLASS"
MACRO_REFLECT_MEMBER = "REFLECT_MEMBER"
REGEX_ARG = "\(.+\)$"
REGEX_TEMPLATE = "template<.+>"
REGEX_TEMPLATEARG = "<.+>"

class ParseState (Enum):
    Idle = 0
    Class = 1
    Member = 2

class Brackets:
    def __init__(self):
        self.begin = 0
        self.end = 0

class ParsedFile:
    def __init__(self, filePath):
        self.filePath = filePath
        self.classesStack = []
        self.stateStack = []
        self.bracketCount = []
        self.currentState = ParseState.Idle
        self.bracketCounter = 0
        self.currentIndex = -1

    def countBracket(self, line):
        self.bracketCount[self.currentIndex].begin += len(re.findall("\{", line))
        self.bracketCount[self.currentIndex].end += len(re.findall("\}", line))

    def getArg(self, line):
        arguments = re.findall("\(.+\)$", line)
        if arguments.count == 1:
            arg = arguments[0]
            arg = arg[1 : len(arg) - 1]
            return arg
        else:
            print("Wrong argument count")
            return ""

    def fillMember(self, wordlist, member):
        if len(wordlist) >= 2:
            member.type = wordlist[0]
            member.name = wordlist[1][:len(wordlist[1]) - 1]
            return member

    def findMember(self, file):
        count = 0
        line = file.readline(count)
        member = ParsedClassMember()
        while len(member.type) == 0 and count > 0:
            line = line.strip()
            if line.startswith("/*"):
                while not line.endswith("*/") or count > 0:
                    line = file.readline(count)
            elif not line.startswith("//"):
                self.fillMember(line.split, member)
                self.classesStack[self.currentIndex].members.append(member)


    def parse(self):
        file = open(self.filePath)
        count = 0
        line = file.readline(count)
        while count > 0:
            line = line.strip()
            if line.startswith(MACRO_REFLECT_CLASS):
                arg = self.getArg(line)
                if len(arg) > 0:
                    self.classesStack.append(ParsedClass(self.getArg(line)))
                    self.currentIndex = len(self.classesStack) - 1
                    self.bracketCount.append(Brackets())
            elif line.startswith(MACRO_REFLECT_MEMBER) and self.currentIndex >= 0:
                self.findMember(file)
            if self.currentIndex >= 0:
                countBracket(line)
                if self.bracketCount[self.currentIndex].begin == self.bracketCount[self.currentIndex].end and self.bracketCount[self.currentIndex].begin > 0:
                    self.currentIndex = -1
            line = file.readline(count)



def parseFile(filename):
    parsed = ParsedFile(filename)
    #generate header
    directory = os.path.dirname(filename)

def parseHeaders(directory):
    for filepath in Path(directory).rglob('*.h'):
        print(">Parse headers: {}".format(filepath))
        parseFile(filepath)