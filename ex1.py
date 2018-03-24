
def File_Type(c):
    dict = {'t':'txt','b':'bin'}
    if dict.has_key(c):
        return dict[c]
    raise NameError('should be "t" or "b"')

def mode(kind,c):
    _type = {'t':{'r':'r','w':'w','r+':'r+','w+':'w+','a':'a','a+':'a+'},'b':{'r':'rb','w':'wb','r+':'rb+','w+':'wb+','a':'ab','a+':'ab+'}}
    if _type.has_key(c):
        return _type[c][kind]
    raise NameError('err')

def printid ():
    return "318949443_208278861"


# Add candidate to the party
def addCandidate(fname, lname, party, filetype):
    if party != "Democratic" and party != "Republican":
        return "fail"
    file = open("can." + File_Type(filetype), mode('a+', filetype))
    cid=0
    #search for the end for the last candidate from 'party'
    context = reversed(file.readlines())
    for line in context:
        if party == line.strip().split(',')[3]:
             cid = int(float(line.strip().split(',')[0]))+1
             break
    file.write("%i,%s,%s,%s\n" % (cid,fname,lname,party))
    file.close()
    return "pass"


def deleteCandidate(cid,filetype):
    return "fail"

#Add state to data
def addState(sid, sname,filetype):
    file = open("copystates." + File_Type(filetype), mode('a+', filetype))
    context = file.readlines()

    # check that sid is not exist because is the key in this database
    for line in context:
        line = line.strip().split(',')[1]
        if sid == line:
            file.close()
            return "fail"
    file.write("%s,%s\n" % (sname, sid))
    file.close()
    return "pass"


def deleteState(sid,filetype):
    return "fail"


def addPoll(pid, party, state, res, filetype):
    if party != "Democratic" and party != "Republican":
        return "fail"

    # precent not above 100
    split = res.split('%')
    split = split[:-1]
    sumPrecent = 0
    for i in split:
        sumPrecent = sumPrecent + int(float(i.split(' ')[-1]))
    if sumPrecent > 100:
        return "fail"


    file = None

    #check candidates to be in the Candidates file
    if filetype == 't':
        file = open('can.txt', 'r+')
    else:
        file = open('can.bin', 'rb+')
    context = file.readlines()
    file.close()

    split = res.replace('%-', '%')
    split = split.split('%')
    split = split[:-1]
    i = 0
    for part in split:
        part = str(part)
        part = part.split(' ')[:2]
        split[i] = part[0] + "," + part[1]+","+party
        candidFound = False
        for line in context:
            line = line.split(',')[1:]
            line = line[0]+","+line[1]+","+line[2]
            line = line.strip()
            if split[i] == line:
                candidFound = True
                break
        if not candidFound:
            return "fail"
        i = i + 1

    # check that state exist in States file
    file = open("copystates." + File_Type(filetype), mode('r+', filetype))
    context = file.readlines()
    file.close()

    existstate = False
    for line in context:
        currstate = line.strip().split(',')[1]
        if state == currstate:
            existstate = True
            break

    if not existstate:
        return "fail"

    #check that pid is not exists because is the key in this file
    if filetype == 't':
        file = open('copypolls.txt', 'a+')
    else:
        file = open('copypolls.bin', 'ab+')
    context = file.readlines()
    for line in context:
        line = line.split(',')[0]
        if pid == line:
            return "fail"
    file.write("%s,%s,%s,%s\n" % (pid, party, state, res))
    file.close()
    return "pass"


def deletePoll(pid,filetype):
    return "fail"


## recordId: id of the record that should be updated, fieldname: field to update, newValue: new value in field name.

# return the n'th occurency of needle in haystack
def indexof(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start


def updateCandidates(recordId, fieldname,newValue,filetype):
    mainFile = open("can."+File_Type(filetype), mode('r',filetype))
    lines = mainFile.readlines()
    mainFile.close()
    temp = lines[recordId]
    # those indexes are the start and end indexes of the new value in the line
    col_s = 0
    col_e = 0
    if fieldname == "CID":
        return "fail"
    elif str(fieldname) == "fname":
        files = open("copypolls." + File_Type(filetype), mode('r', filetype))
        file = files.readlines()
        files.close()
        i = 0
        # check if the candidate exists in any poll
        for line in file:
            l = temp.split(',')[1] + ' ' + temp.split(',')[2]
            if line.split(',')[1] == str(temp).split(',')[3].strip() and (l in line):
                return "fail"
            i = i + 1
        col_s = indexof(temp, ',', 1) + 1
        col_e = indexof(temp, ',', 2)
    elif str(fieldname) == "lname":

        files = open("copypolls." + File_Type(filetype), mode('r', filetype))
        file = files.readlines()
        files.close()
        i = 0
        # check if the candidate exists in any poll
        for line in file:
            if line.split(',')[1] == str(temp).split(',')[3].strip() and (temp.split(',')[1] + ' ' + temp.split(',')[2]) in line:
                return "fail"
            i = i + 1
        col_s = indexof(temp, ',', 2) + 1
        col_e = indexof(temp, ',', 3)
    else:
        canChange = True
        files = open("copypolls." + File_Type(filetype), mode('r', filetype))
        file = files.readlines()
        files.close()
        # check if the candidate exists in any poll
        for line in file:
            if str(temp).split(',')[3].strip() in line and (temp.split(',')[1] + ' ' + temp.split(',')[2]) in line:
                canChange = False
        if not canChange:
            return "fail"
        col_s = indexof(temp, ',', 3) + 1
        col_e = str(temp).__len__()
        newValue = newValue + "\n"
    temp = temp.replace(temp[col_s:col_e], newValue)
    lines[recordId] = temp
    out = open("can."+File_Type(filetype), mode('w',filetype))
    out.writelines(lines)
    out.close()
    return "pass"


def updateStates(recordId, fieldname,newValue,filetype):
    file = open("copystates." + File_Type(filetype), mode('r', filetype))
    lines = file.readlines()
    temp = lines[recordId]
    file.close()
    col_s = 0
    col_e = 0
    if fieldname == "sname":
        col_e = indexof(temp, ',', 1)
    else:
        return "fail"
    temp = temp.replace(temp[col_s:col_e], newValue)
    lines[recordId] = temp
    out = open("copystates." + File_Type(filetype), mode('w', filetype))
    out.writelines(lines)
    out.close()
    return "pass"


def updatePolls(recordId, fieldname, newValue, filetype):
    file = open("copypolls." + File_Type(filetype), mode('r', filetype))
    lines = file.readlines()
    temp = lines[recordId]
    file.close()
    col_s = 0
    col_e = 0
    if fieldname == "pid":
        return "fail"
    elif fieldname == "party":
        return "fail"
    elif fieldname == "state":
        fileState = open("copystates." + File_Type(filetype), mode('r', filetype))
        sids = fileState.readlines()
        fileState.close()
        stateExist = False
        # check if there are a state with the new value (sid)
        for line in sids:
            if newValue == line.strip().split(',')[1]:
                stateExist = True
                break
        if not stateExist:
            return "fail"
        col_s = indexof(temp, ',', 2) + 1
        col_e = indexof(temp, ',', 3)
    else:
        # check validation like in addPols ( precents<=100 ; candidates in the party)
        split = newValue.split('%')
        split = split[:-1]
        sumPrecent = 0
        for i in split:
            sumPrecent = sumPrecent + int(float(i.split(' ')[-1]))
        if sumPrecent > 100:
            return "fail"
        fileCand = open("can." + File_Type(filetype), mode('r', filetype))
        context = fileCand.readlines()
        fileCand.close()
        split = newValue.replace('%-', '%')
        split = split.split('%')
        split = split[:-1]
        i = 0
        for part in split:
            part = str(part)
            part = part.split(' ')[:2]
            split[i] = part[0] + "," + part[1] + "," + lines[recordId].split(',')[1]
            candidFound = False
            for line in context:
                line = line.split(',')[1:]
                line = line[0] + "," + line[1] + "," + line[2]
                line = line.strip()
                if split[i] == line:
                    candidFound = True
                    break
            if not candidFound:
                return "fail"
            i = i + 1
        col_s = indexof(temp, ',', 3) + 1
        col_e = str(temp).__len__()
        newValue = newValue + "\n"
    temp = temp.replace(temp[col_s:col_e], newValue)
    lines[recordId] = temp
    out = open("copypolls." + File_Type(filetype), mode('w', filetype))
    out.writelines(lines)
    out.close()
    return "pass"


def updateFile(recordId,fieldname,newValue,file,filetype):
    res = ""
    if file=='Candidates':
         res = updateCandidates(int(recordId),fieldname,newValue,filetype)
    elif file=='States':
        res = updateStates(int(recordId),fieldname,newValue,filetype)
    else:
        res = updatePolls(int(recordId), fieldname, newValue, filetype)
    return res


def sort(filename,filetype,fieldname):
    return "fail"


# return all polls that belongs to 'party' and conducted at 'state'
def selectPollsFromStateAndParty(state,party,filetype):
    l = []
    file = open("copypolls." + File_Type(filetype), mode('r+', filetype))
    context = file.readlines()
    search = party+","+state
    for line in context:
        split = line.split(',')
        stateAndParty = split[1]+","+split[2]
        if search == stateAndParty:
            l.append(line.strip())
    file.close()
    return l

# return all polls that belongs to 'party'
def selectPollsForParty(party,filetype):
    l = []
    file = open("copypolls." + File_Type(filetype), mode('r+', filetype))
    context = file.readlines()
    for line in context:
        split = line.split(',')
        if party == split[1]:
            l.append(line.strip())
    file.close()
    return l

def find(filename,filetype,findme):
    return -1


def returnLine(filename,filetype,linenumber):
    return ""

