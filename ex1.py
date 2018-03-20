
def File_Type(c):
    dict = {'t':'txt','b':'bin'}
    if dict.has_key(c):
        return dict[c]
    raise NameError('should be "t" or "b"')

def mode(kind,c):
    _type = {'t':{'r':'r','w':'w','r+':'r+','w+':'w+','a':'a+'},'b':{'r':'rb','w':'wb','r+':'rb+','w+':'wb+','a':'ab+'}}
    if dict.has_key(c):
        return dict[c][kind]
    raise NameError('err')

def printid ():
    return "208278861_318949443"

def addCandidate(fname, lname, party, filetype):
    return "fail"

def delete_from(fileName,content):
    File = open(fileName, "r+")
    Lines = File.readlines()
    File.seek(0)
    for line in Lines:
        splitted = line.strip().split(',')
        print(splitted[0])
        if str(content) == splitted[0]:
            continue
        File.write(line)
    File.truncate()
    File.close()
    return "success"

def deleteCandidate(cid,filetype):
    File = open('Polls.' + File_Type(filetype), 'r+')
    arr = [[]]
    for line in File:
        arr.append(line.strip().split(','))
    arr.remove(arr[0])
    states = [li[3] for li in (ar for ar in arr)]
    print(states)
    File.close()
    if str(cid) in states:
        return 'fail'
    return delete_from('Candidates.'+File_Type(filetype),cid)

def addState(sid, sname,filetype):
    return "fail"


def deleteState(sid,filetype):
    File = open('Polls'+File_Type(filetype), 'r+')
    arr = [[]]
    for line in File:
        arr.append(line.strip().split(','))
    arr.remove(arr[0])
    states = [li[1] for li in (ar for ar in arr)]
    File.close()
    if str(sid) in states:
        return 'fail'
    return delete_from('States'+File_Type(filetype),sid)

def addPoll(pid,party,state,res,filetype):
    return "fail"


def deletePoll(pid,filetype):
    return delete_from('Polls'+File_Type(filetype),pid)


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


deleteCandidate(204,'t')
'''
File = open('Candidates.txt', 'r+')
arr=[[]]
for line in File:
     arr.append(line.strip().split(','))
arr.remove(arr[0])
names = [li[1] for li in (ar for ar in arr)]
File.close()
'''
