import csv,operator

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

def addCandidate(fname, lname, party, filetype):
    return "fail"


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
    return "fail"


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
    """
    The function delete a poll from the polls file if the deletion is valid
    :param cid: the key of the record we want to delete
    :param filetype: the type of file we want to delete from
    :return: if the deletion is valid and we succeeded to delete
    """
    return delete_from('Polls',pid,filetype)


## recordId: id of the record that should be updated, fieldname: field to update, newValue: new value in field name.
def updateFile(recordId,fieldname,newValue,file,filetype):
    return "fail"


def sort(filename,filetype,fieldname):
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


def selectPollsFromStateAndParty(state,party,filetype):
    l = []
    return l


def selectPollsForParty(party,filetype):
    l = []
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


print sort('Polls','t','party')





'''
import csv,operator

#FileToWrite = open('newFile','w+')
File = open('can.'+File_Type('t'), mode("r+",'b'))
Title=File.readline()
File.seek(0)
#FileToWrite.write(Title)
File.seek(File.readline().__len__())
data = csv.reader(File,delimiter=',')
sorted = sorted(data,key=operator.itemgetter(0))

print sorted[0]
File = open('can.'+File_Type('t'), mode("w+",'t'))
print sorted[0]
fileWriter = csv.writer(File,delimiter=',')
fileWriter.writerow(sorted[0])
'''





'''
#File.seek(File.readline().__len__()+1)
print File.readlines()
fileWriter = csv.writer(File,delimiter=',')

File.close()
File = open('can.'+File_Type('t'), mode("r+",'t'))
#File.seek(File.readline().__len__()+1)
File.seek(0)
#FileToWrite = open('newFile','r+')
after = File.readlines()
#print after

for i in range(after.__len__()):
    File.write(after[i].strip())
print after


File.close()
'''
