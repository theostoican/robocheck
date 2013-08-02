"""robocheck-core.py
   
   General description:
    This is the core of the program. It loads the modules, runs them, 
   receives a list of errors from each module and creates a json
   file with all the errors. 
   (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 26.07.2013
"""
import os
import sys
import json
import subprocess
import time

class Error:
    def __init__(self, code, sourceFile, function, line):
        self.code = code
        self.sourceFile = sourceFile
        self.function = function
        self.line = line

    def __eq__(self, other):
        if isinstance(other, Error):
            result = False
            if self.code == other.code \
                and self.sourceFile == other.sourceFile \
                and self.function == other.function \
                and self.line == other.line:
                
                result = True
            return result
        return NotImplemented

    def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result 
    

sources = []

def getFileFunctionLine( outputLine ):
    details = []
    if ": " not in outputLine:
        return None
    if "at " not in outputLine and "by " not in outputLine:
        return None
    if "exit" in outputLine:
        return None

    fflNotSplited = outputLine.split(": ")[1]

    sourceFile = fflNotSplited.split(" (")[1].split(":")[0]
    if sourceFile not in sources:
        return None

    function = fflNotSplited.split(" (")[0]
    line = fflNotSplited.split(":")[1].split(")")[0]
    
    details.append(sourceFile)
    details.append(function)
    details.append(line)
    return details
      

def getErrors(toolOutput):
    errorList = []
    nrLinesOutput = len(toolOutput)
    for i in range( nrLinesOutput ):
        error = None
        if "bytes in" and "are definitely lost in loss record" in toolOutput[i]:
            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j]) 
                if ffl is not None:
                    error = Error("MEMORY LEAK", ffl[0], ffl[1], ffl[2])
                    break
                        
        if "Invalid write" in toolOutput[i] or "Invalid read" in toolOutput[i]:
            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("INVALID ACCESS", ffl[0], ffl[1], ffl[2])
                    break

        if "Uninitialised value was created" in toolOutput[i]:
            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("UNITIALIZED VARIABLE USAGE", ffl[0], ffl[1], ffl[2])
                    break

        if "Invalid free" in toolOutput[i]:
            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("INVALID FREE", ffl[0], ffl[1], ffl[2])
                    break

        if "Open file descriptor" in toolOutput[i] \
            and "<inherited from parent>" not in toolOutput[i+1]:

            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("OPENED, BUT NOT CLOSED FILE DESCRIPTOR", ffl[0], ffl[1], ffl[2])
                    break

        if error is not None and error not in errorList:
            errorList.append(error)

    return errorList   

def main():
    global sources
    extractCmd = []
    extractCmd.append('unzip')
    extractCmd.append('-q')
    extractCmd.append('-d')
    extractCmd.append('current-test/')
    extractCmd.append(sys.argv[1])
    x = subprocess.Popen(extractCmd)
    time.sleep(0.5)

    sources = os.listdir('./current-test/src')
    exes = os.listdir('./current-test/bins')
    exesPath = "./current-test/bins/"
    returnPath = os.getcwd()
    process = []
    process.append('valgrind')
    process.append('--leak-check=full')
    process.append('--track-origins=yes')
    process.append('--track-fds=yes')
    
    errorJsonList = []    
    os.chdir(exesPath)
    for exe in exes:
        exe = "./" + exe
        process.append(exe)
        print process
        x = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        x.wait()
        process.remove(exe)
        if x.returncode != 0:
            continue
        toolOutput = x.communicate()[1].splitlines()
        """for i in toolOutput:
            print i """
        errors = getErrors(toolOutput)
        for err in errors:
            errorJsonList.append( {
                'code': err.code,
                'sourceFile': err.sourceFile,
                'function': err.function,
                'line': err.line,
                })
        print json.dumps(errorJsonList, indent=2)
    os.chdir(returnPath)

if __name__ == '__main__':
    main()
