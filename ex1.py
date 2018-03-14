import subprocess

def printid ():
    return "208278861_318949443"

def addCandidate(fname, lname, party, filetype):
    return "fail"


def deleteCandidate(cid,filetype):
    subprocess.call(['sed','-i','/.*204.*/d','can.txt'])
    return "fail"

def addState(sid, sname,filetype):
    return "fail"


def deleteState(sid,filetype):
    return "fail"

def addPoll(pid,party,state,res,filetype):
    return "fail"


def deletePoll(pid,filetype):
    return "fail"


## recordId: id of the record that should be updated, fieldname: field to update, newValue: new value in field name.
def updateFile(recordId,fieldname,newValue,file,filetype):
    return "fail"


def sort(filename,filetype,fieldname):
    return "fail"


def selectPollsFromStateAndParty(state,party,filetype):
    l = []
    return l


def selectPollsForParty(party,filetype):
    l = []
    return l

def find(filename,filetype,findme):
    return -1


def returnLine(filename,filetype,linenumber):
    return ""


'''

File = open('Candidates.txt', 'r+')
arr=[[]]
for line in File:
     arr.append(line.strip().split(','))
arr.remove(arr[0])


print(arr[1][1])
names = [li[1] for li in (ar for ar in arr)]
print(names)
File.close()
'''

deleteCandidate(0,'')

