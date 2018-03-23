
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


def addCandidate(fname, lname, party, filetype):
    if party != "Democratic" or party != "Republican":
        return "fail"
    file = open("can." + File_Type(filetype), mode('a+', filetype))
    cid=0
    context = reversed(file.readlines())
    for line in context:
        if party == line.strip().split(',')[3]:
             cid = int(float(line.strip().split(',')[0]))+1
             break
    file.write("%i,%s,%s,%s\n" % (cid,fname,lname,party))
    file.close()

    ######################################
    ###check what to return###############
    ######################################
    return "pass"


def deleteCandidate(cid,filetype):
    return "fail"

def addState(sid, sname,filetype):
    file = open("copystates." + File_Type(filetype), mode('a+', filetype))

    context = file.readlines()
    for line in context:
        line = line.strip().split(',')[1]
        if sid == line:
            print "fail"
            file.close()
            return "fail state already exist"
    file.write("%s,%s\n" % (sname, sid))
    file.close()
    return "fail"


def deleteState(sid,filetype):
    return "fail"


def addPoll(pid, party, state, res, filetype):
    if party != "Democratic" and party != "Republican":
        print "fail party in poll"
        return "fail"

    # precent not above 100
    split = res.split('%')
    split = split[:-1]
    sumPrecent = 0
    for i in split:
        sumPrecent = sumPrecent + int(float(i.split(' ')[-1]))
    if sumPrecent > 100:
        print "fail precents above 100"
        return "fail"


    file = None

    #check candidates
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
            print "fail candidate did not found"
            return "fail"
        i = i + 1

    # exist state
    if filetype == 't':
        file = open('copystates.txt', 'r+')
    else:
        file = open('copystates.bin', 'rb+')

    context = file.readlines()
    file.close()

    existstate = False
    for line in context:
        currstate = line.strip().split(',')[1]
        if state == currstate:
            existstate = True
            break

    if not existstate:
        print "fail state did not exist in add poll"
        return "fail"

    #check poll id
    if filetype == 't':
        file = open('Polls.txt', 'a+')
    else:
        file = open('copypolls.bin', 'ab+')
    context = file.readlines()
    for line in context:
        line = line.split(',')[0]
        if pid == line:
            print "fail poll already exist"
            return "fail"
    file.write("%s,%s,%s,%s\n" % (pid, party, state, res))
    file.close()
    return "fail"


def deletePoll(pid,filetype):
    return "fail"


## recordId: id of the record that should be updated, fieldname: field to update, newValue: new value in field name.
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
    col_s = 0
    col_e = 0
    if fieldname == "CID":
        return "fail"
    elif str(fieldname) == "fname":
        files = open("copypolls." + File_Type(filetype), mode('r', filetype))
        file = files.readlines()
        files.close()
        i = 0
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
        col_s = indexof(temp,',',1)+1
        col_e = str(temp).__len__()
        newValue = newValue+"\n"
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
        return "fail"
    else:
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
                print "fail candidate did not found"
                return "fail"
            i = i + 1
        col_s = indexof(temp, ',', 3) + 1
        col_e = str(temp).__len__()
        newValue = newValue + "\n"
    temp = temp.replace(temp[col_s:col_e], newValue)
    lines[recordId] = temp
    out = open("copystates." + File_Type(filetype), mode('w', filetype))
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


def selectPollsFromStateAndParty(state,party,filetype):
    l = []
    file = None
    if filetype == 't':
        file = open('copypolls.txt', 'r+')
    else:
        file = open('copypolls.bin', 'rb+')
    context = file.readlines()
    search = party+","+state
    for line in context:
        split = line.split(',')
        stateAndParty = split[1]+","+split[2]
        if search == stateAndParty:
            l.append(line.strip())
    file.close()
    return l


def selectPollsForParty(party,filetype):
    l = []
    file = None
    if filetype == 't':
        file = open('copypolls.txt', 'r+')
    else:
        file = open('copypolls.bin', 'rb+')
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
#addCandidate('eran','shvili','Democratic','t')
#addState('IS', 'ISRAEL', 'b')
#addPoll(12,'asd','ALL','ewq','t')

'''
line = "TB1,Republican,AR,Ted Cruz 27%-Marco Rubio 23%-Donald Trump 23%-Ben Carson 11%"
line = line.strip()
print line
split = line.split(',')[3]
print split
split = split.replace('-', '')
split = split.split('%')
split = split[:-1]
print "-----------------"
print split
i=0
for a in split:
    a = str(a)
    a = a.split(' ')[:2]
    split[i]=a[0]+","+a[1]+",Democratic"
    i=i+1
    print a
print split
split = split[1:]
print split
'''
#addPoll("SH2","Republican","IS","Ted Cruz 27%-Marco Rubio 23%-michael shvili 23%-Ben Carson 11%","t")

#print updateFile(10, 'party', "Democratic", "Candidates",'b')