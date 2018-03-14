
def printid ():
    return "318949443_208278861"


def addCandidate(fname, lname, party, filetype):
    if filetype == 't':
        file = open("Candidates.txt", 'a+')
        cid=0
        context = reversed(file.readlines())
        for line in context:
            if party == line.strip().split(',')[3]:
                cid = line.strip.split(',')[0]+1
                break
        file.write("%i,%s,%s,%s\n" % (cid,fname,lname,party))
    else:
        file = open("cab.bin", 'ab+')
        cid = 0
        context = reversed(file.readlines())
        for line in context:
            if party == line.strip().split(',')[3]:
                cid = line.strip.split(',')[0] + 1
                break
        file.write("%i,%s,%s,%s"% (cid, fname, lname, party))
    return "fail"


def deleteCandidate(cid,filetype):
    #subprocess.call(['sed','-i','/.*204.*/d','can.txt'])
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

'''
deleteCandidate(0,'')
for line in reversed(open("Candidates.bin").readlines()):
    print line.rstrip()
con = reversed(open("Candidates.txt").readlines())
for line in con:
    print line.strip().split(',')[3]
'''
addCandidate('michael','shvili','Republican','b')