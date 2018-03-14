
def File_Type(c):
    dict = {'t':'txt','b':'bin'}
    if dict.has_key(c):
        return dict[c]
    raise NameError('should be "t" or "b"')


def printid ():
    return "318949443_208278861"


def addCandidate(fname, lname, party, filetype):
    file = None
    if filetype == 't':
        file = open("can.txt", 'a+')
    else:
        file = open("can.txt", 'a+b')
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
    return "fail"


def deleteCandidate(cid,filetype):
    return "fail"

def addState(sid, sname,filetype):
    file = None
    if filetype == 't':
        file = open('copystates.txt', 'a+')
    else:
        file = open('copystatesbin.bin', 'ab+')
    context = file.readlines()
    existstate = False
    for line in context:
        li = line.strip().split(',')[1]
        if sid == li:
            print "fail"
            file.close()
            return "fail"
    file.write("%s,%s\n" % (sname, sid))
    file.close()
    return "fail"


def deleteState(sid,filetype):
    return "fail"


#check if the state is exists
def addPoll(pid,party,state,res,filetype):
    file = None
    if filetype == 't':
        file = open('copystates.txt', 'a+')
    else:
        file = open('copystates.bin', 'ab+')
    context = file.readlines()
    existstate = False
    for line in context:
        li = line.strip().split(',')[1]
        if state == li:
            existstate = True
            break
    file.close()
    if not existstate:
        print "fail"
        return "fail"


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
#addCandidate('eran','shvili','Democratic','t')
#addState('IS', 'ISRAEL', 'b')
#addPoll(12,'asd','ALL','ewq','t')
line = "TB1,Republican,AR,Ted Cruz 27%-Marco Rubio 23%-Donald Trump 23%-Ben Carson 11%"
line = line.strip()
split = line.split('%')
for i in split:
    print i.split(' ')[-1]