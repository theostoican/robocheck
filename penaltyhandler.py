"""penaltyhandler.py

    General description:
     This is the module that manages everything regarding penalties;
    starting from configuration, up to adding the informations about
    penalties to the output.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
            last rewiew: 30.10.2013
"""

import os
import sys

def confirmPenaltyConfigurations( penaltyDictionary ):
    os.system('clear')
    print 'Error Type',
    for i in range(15):
        print ' ',
    print 'Mode[S/M] ',
    print 'Occurences ',
    print 'Penalty'
    print ''

    for error in penaltyDictionary:
        print error,
        for i in range( (45-len(error))/2 ):
            print ' ',
        penaltyConfig = penaltyDictionary[error]
        mode = penaltyConfig[0]
        occurence = penaltyConfig[1]
        penalty = penaltyConfig[2]
        if mode == 'S' :
            print 'S',
            for i in range(4):
                print ' ',
            print ' ',
        else:
            print 'M',
            for i in range(4):
                print ' ',
            print occurence,

        for i in range(4):
            print ' ',
        print penalty

    print '\nIs this configuration correct? [Y/n]',
    option = sys.stdin.readline().splitlines()[0]
    if option != 'N' and option != 'n':
        return True
    else:
        return False

def penaltyConfig( errorsToLookFor ):
    penaltyDictionary = dict()
    os.system('clear')
    for error in errorsToLookFor:
        print error
        while True:
            print "\tMode[S/M]:  ",
            mode = sys.stdin.readline().splitlines()[0].upper()
            if mode != "S" and mode != "M":
                print "Invalid option!"
            else:
                break

        if mode == "M":
            while True:
                print "\tOccurences: ",
                occurence = sys.stdin.readline().splitlines()[0]
                if occurence.isdigit():
                    occurence = int(occurence)
                    if occurence <= 0:
                        print "Invalid option! Need a number > 0."
                    else:
                        break
                else:
                    print "Invalid option! Need a number."
        else:
            occurence = None


        while True:
            print "\tPenalty:    ",
            penalty = sys.stdin.readline().splitlines()[0]
            try:
                penalty = float(penalty)
                if penalty < 0:
                    print "Invalid option! Need a float >= 0."
                else :
                    break
            except ValueError:
                print "Invalid option! Need a float number."
        penaltyDictionary[error] = [mode, occurence, penalty]
        print ''

    if confirmPenaltyConfigurations( penaltyDictionary) is True:
        return penaltyDictionary
    else:
        return penaltyConfig( errorsToLookFor )


def getErrorsToLookFor(penaltyDictionary):
    errorsToLookFor = []
    for error in penaltyDictionary:
        errorsToLookFor.append(error)

    return errorsToLookFor