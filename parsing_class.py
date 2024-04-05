import re
import parsed_objects as PO
import os

class HeaderParser:
    MACRO_REFLECT_CLASS = "REFLECT_CLASS"
    MACRO_REFLECT_MEMBER = "REFLECT_MEMBER"

    def isReflectClass(self, line):
        return line.startswith(self.MACRO_REFLECT_CLASS)

    def isReflectMember(self, line):
        return line.startswith(self.MACRO_REFLECT_MEMBER)

    def extractArg(self, line):
        return re.search(".*\((.*)\).*", line).group(1)

    def ignoreComment(self, file, curLine):
        regex = re.search("\*/(.*)", curLine)
        while regex is None and not file.atEnd():
            line = file.nextTrimmedLine()
            regex = re.search("\*/(.*)", line)
        if regex is None:
            return ""
        return regex.group(1)

    def removeComment(self, file, line):
        if "//" in line:
            lineRet = re.search("(.*)//", line).group(1)
        elif "/*" in line:
            lineRet = self.ignoreComment(file, line)
        else:
            lineRet = line
        return lineRet


    def getMember(self, file):
        found = False
        while not file.atEnd() and not found:
            line = self.removeComment(file, file.nextTrimmedLine())
            member = re.search("(.*) (.*);.*", line)
            if member is not None:
                self.classList[self.classIndex].members.append(PO.ClassMember(member.group(1), member.group(2)))
                found = True


    def parseClass(self, file, classname):
        self.classList.append(PO.Class(classname))
        self.classIndex += 1
        classBracket = PO.BracketCounter()
        while not file.atEnd() and not classBracket.isFinished():
            line = self.removeComment(file, file.nextTrimmedLine())
            classBracket.count(line)
            if line.startswith(self.MACRO_REFLECT_MEMBER):
                self.getMember(file)
        self.classIndex -= 1

    def processLine(self, file, curLine):
        if self.isReflectClass(curLine):
            classname = self.extractArg(curLine)
            self.parseClass(file, classname)

    def __init__(self, filePath):
        self.filePath = filePath
        self.classList = []
        self.classIndex = -1

    def parse(self):
        file = PO.ParsedFile(self.filePath)
        while not file.atEnd():
            line = file.nextTrimmedLine()
            self.processLine(file, line)

    def print(self):
        print(self.filePath)
        print(os.path.basename(self.filePath))
        for classe in self.classList:
            classe.print()

    def implementLoader(self):
        if len(self.classList) > 0:
            name = os.path.basename(self.filePath)
            name = name[0:len(name) - 1] + "generated.h"
            generatedFile = self.filePath.parent.absolute().__str__() + "\\" + name
            file = open(generatedFile, 'w')
            for classParsed in self.classList:
                classParsed.implement(file)