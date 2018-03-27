import operator

def File_Type(filetype):
    dict = {'t':'txt','b':'bin'}
    if dict.has_key(filetype):
        return dict[filetype]
    raise NameError('should be "t" or "b"')

def mode(kind, filetype):
    _type = {'t':{'r':'r','w':'w','r+':'r+','w+':'w+','a':'a','a+':'a+'},
             'b':{'r':'rb','w':'wb','r+':'rb+','w+':'wb+','a':'ab','a+':'ab+'}}
    if _type.has_key(filetype):
        return _type[filetype][kind]
    raise NameError('err in mode')

def printid ():
    return "208278861_318949443"


# Add candidate to the party
def addCandidate(fname, lname, party, filetype):
    '''

    :param fname: first name of the new candidate
    :param lname: last name of the new candidate
    :param party: The party the candidate belong to
    :param filetype: the file we want to work with
    :return: return pass if the candidate added to the file
    '''
    if party != "Democratic" and party != "Republican":
        return "fail"
    file = open("Candidates." + File_Type(filetype), mode('a+', filetype))
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

def delete_from(fileName, key, filetype):
    """

    :param fileName: the name of the file we want to delete from
    :param key: the key of the record we want to delete
    :param filetype: the type of the file we want to delete from
    :return: if the deletion is valid and we succeeded to delete
    """

    File = open(fileName+'.'+File_Type(filetype), mode("r+",filetype))
    Lines = File.readlines()
    File.seek(0)
    column = 0 + (fileName == 'States')
    flag=False
    for line in Lines:
        splitted = line.strip().split(',')
        if str(key) == splitted[column]:
            flag=True
            continue
        File.write(line)
    File.truncate()
    File.close()
    return "pass" if flag else 'fail'

def deleteCandidate(cid,filetype):
    """
    The function delete a candidate from the candidates file if the deletion is valid
    :param cid: the key of the record we want to delete
    :param filetype: the type of file we want to delete from
    :return: if the deletion is valid and we succeeded to delete
    """

    File = open('Polls.' + File_Type(filetype), 'r+')
    arr = [[]]
    for line in File:
        arr.append(line.strip().split(','))
    File.close()
    arr.remove(arr[0])
    candidates = [li[3] for li in (ar for ar in arr)][1:]
    for i in range(candidates.__len__()):
        candidates[i] = candidates[i].replace('%-', '%')
        candidates[i] = candidates[i].split('%')[:-1]
        for j in range(candidates[i].__len__()):
            candidates[i][j] = candidates[i][j].split(' ')[:-1]

    candidates = [candidates[i][j] for i in range(candidates.__len__()) for j in range(candidates[i].__len__())]
    File = open('Candidates.' + File_Type(filetype), 'r+')
    all_candidates = [[]]
    for line in File:
        all_candidates.append(line.strip().split(',')[0:3])
    all_candidates = all_candidates[2:]
    File.close()


    for i in range(all_candidates.__len__()):
        if all_candidates[i][0]==str(cid):
            if all_candidates[i][1:] in candidates:
                return 'fail'
    return delete_from('Candidates',cid,filetype)

def addState(sid, sname,filetype):
    '''

    :param sid: The key of the table, the ID of state
    :param sname:  name of the state
    :param filetype: the filr we work with him
    :return: pass if succeed. else "fail"
    '''
    file = open("States." + File_Type(filetype), mode('a+', filetype))
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
    """
        The function delete a state from the states file if the deletion is valid
        :param sid: the key of the record we want to delete
        :param filetype: the type of file we want to delete from
        :return: if the deletion is valid and we succeeded to delete
        """

    File = open('Polls.'+File_Type(filetype), 'r+')
    arr = [[]]
    for line in File:
        arr.append(line.strip().split(','))
    arr.remove(arr[0])
    states = [li[2] for li in (ar for ar in arr)]
    File.close()
    if str(sid) in states:
        return 'fail'
    return delete_from('States',sid,filetype)

def addPoll(pid, party, state, res, filetype):
    '''

    :param pid: the key of the table, ID of poll
    :param party: the praty the poll belong to
    :param state: the state where the poll conducted
    :param res: the result of the poll
    :param filetype: the file we work with him
    :return: pass if the addition succeed. else "fail"
    '''
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
        file = open('Candidates.txt', 'r+')
    else:
        file = open('Candidates.bin', 'rb+')
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
    file = open("States." + File_Type(filetype), mode('r+', filetype))
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
        file = open('Polls.txt', 'a+')
    else:
        file = open('Polls.bin', 'ab+')
    context = file.readlines()
    for line in context:
        line = line.split(',')[0]
        if pid == line:
            return "fail"
    file.write("%s,%s,%s,%s\n" % (pid, party, state, res))
    file.close()
    return "pass"


def deletePoll(pid,filetype):
    """
    The function delete a poll from the polls file if the deletion is valid
    :param cid: the key of the record we want to delete
    :param filetype: the type of file we want to delete from
    :return: if the deletion is valid and we succeeded to delete
    """
    return delete_from('Polls',pid,filetype)


## recordId: id of the record that should be updated, fieldname: field to update, newValue: new value in field name.

# return the n'th occurency of needle in haystack
def indexof(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start


def updateCandidates(recordId, fieldname,newValue,filetype):
    '''
    :param recordId: number of line we want to update
    :param fieldname: the field we want to change
    :param newValue: the new Value to be replace
    :param filetype: the file we want to work with him
    :return: pass if the update succeed
    '''
    mainFile = open("Candidates."+File_Type(filetype), mode('r',filetype))
    lines = mainFile.readlines()
    mainFile.close()
    temp = lines[recordId]
    # those indexes are the start and end indexes of the new value in the line
    col_s = 0
    col_e = 0
    if fieldname == "CID":
        return "fail"
    elif str(fieldname) == "fname":
        files = open("Polls." + File_Type(filetype), mode('r', filetype))
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

        files = open("Polls." + File_Type(filetype), mode('r', filetype))
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
        files = open("Polls." + File_Type(filetype), mode('r', filetype))
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
    out = open("Candidates."+File_Type(filetype), mode('w',filetype))
    out.writelines(lines)
    out.close()
    return "pass"


def updateStates(recordId, fieldname,newValue,filetype):
    '''

    :param recordId: number of line we want to update
    :param fieldname: the field we want to change
    :param newValue: the new Value to be replace
    :param filetype: the file we want to work with him
    :return: pass if the update succeed
    '''
    file = open("States." + File_Type(filetype), mode('r', filetype))
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
    out = open("States." + File_Type(filetype), mode('w', filetype))
    out.writelines(lines)
    out.close()
    return "pass"


def updatePolls(recordId, fieldname, newValue, filetype):
    '''

    :param recordId: number of line we want to update
    :param fieldname: the field we want to change
    :param newValue: the new Value to be replace
    :param filetype: the file we want to work with him
    :return: pass if the update succeed
    '''
    file = open("Polls." + File_Type(filetype), mode('r', filetype))
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
        fileState = open("States." + File_Type(filetype), mode('r', filetype))
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
        fileCand = open("Candidates." + File_Type(filetype), mode('r', filetype))
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
    out = open("Polls." + File_Type(filetype), mode('w', filetype))
    out.writelines(lines)
    out.close()
    return "pass"


def updateFile(recordId,fieldname,newValue,file,filetype):
    '''
    we splitted the function for 3 function. each one to work according to the file we want to update
    :param recordId: number of line we want to update
    :param fieldname: the field we want to change
    :param newValue: the new Value to be replace
    :param file: the file witch be updated
    :param filetype: the file we want to work with him
    :return: pass if the update succeed
    '''
    res = ""
    if file=='Candidates':
         res = updateCandidates(int(recordId),fieldname,newValue,filetype)
    elif file=='States':
        res = updateStates(int(recordId),fieldname,newValue,filetype)
    else:
        res = updatePolls(int(recordId), fieldname, newValue, filetype)
    return res


def sort(filename,filetype,fieldname):
    '''

    :param filename: the file we work with
    :param filetype: the kind of file
    :param fieldname:the column we sort according to
    :return: passs if secceed. else fail if column not exists
    '''
    File = open(filename + '.' + File_Type(filetype), mode("r+", filetype))
    Title = File.readline()
    splittedTitle = Title.strip().split(',')
    dict = {}
    for i in range(splittedTitle.__len__()):
        dict[splittedTitle[i]] = i
    if not dict.has_key(fieldname):
        File.close()
        return 'fail'
    File.seek(0)
    File.seek(File.readline().__len__() + (filetype=='t'))
    lines = [line.split(',') for line in File]
    File.close()
    File = open(filename + '.' + File_Type(filetype), mode("w", filetype))
    File.write(Title)

    SOSO = sorted(lines, key=operator.itemgetter(dict[fieldname]))
    for line in SOSO:
        File.write(','.join(line))
    File.close()
    return "pass"



# return all polls that belongs to 'party' and conducted at 'state'
def selectPollsFromStateAndParty(state,party,filetype):
    '''

    :param state: the state that we want the polls that conducted there
    :param party: the party that we want the polls that conducted for her
    :param filetype: the file we work with
    :return: list of the polls that appropriate
    '''
    l = []
    file = open("Polls." + File_Type(filetype), mode('r+', filetype))
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
    '''

    :param party: the party that we want the polls that conducted for her
    :param filetype: the file we work with
    :return: list of polls that appropriate
    '''
    l = []
    file = open("Polls." + File_Type(filetype), mode('r+', filetype))
    context = file.readlines()
    for line in context:
        split = line.split(',')
        if party == split[1]:
            l.append(line.strip())
    file.close()
    return l

def find(filename,filetype,findme):
    """

    :param filename: the name of the file we want to search in
    :param filetype: the type of the file we want to search in
    :param findme: the content we search in the file
    :return: the number of the line the variable 'findme' appears
    """
    File = open(filename+'.'+File_Type(filetype), mode("r+",filetype))
    Lines = File.readlines()
    File.close()
    for i in range(Lines.__len__()):
        if str(findme) in Lines[i]:
            return i
    return -1


def returnLine(filename,filetype,linenumber):
    """

    :param filename: the name of the file we want to search in
    :param filetype: the type of the file we want to search in
    :param linenumber: the number of the line we want to have its key
    if the number is negative the number of the line will be counted from the end
    :return: the key of the requested line
    """

    File = open(filename+ '.' + File_Type(filetype), mode("r+", filetype))
    Lines = File.readlines()
    File.close()
    if int(linenumber) >= Lines.__len__():
        return "fail"
    column = 0+ (filename=='States')
    row = int(linenumber) if linenumber>=0 else int(linenumber)+Lines.__len__()
    return str(Lines[row]).strip().split(',')[column]


print sort('Candidates','b','CID')
