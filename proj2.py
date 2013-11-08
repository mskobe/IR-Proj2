import subprocess
global queries


def get_query():
    f = open('desc.51-100.short', 'r')
    queries = []
    for line in f:
        line = line.strip(' .\n')
        if line == '':
            pass
        else:
            query = parse_query(line)
            queries.append(query)
    f.close()
    return queries


def parse_query(line):
    query = line.split(' ')
    temp = []
    for i in range(0, len(query)):
        if query[i] == '':
            pass
        elif query[i].find('-') != -1:
            query[i] = parse_helper(query[i])
            remove_hyphen = query[i].split('-')
            for i in remove_hyphen:
                i = i.lower()
                temp.append(i)
        elif query[i].find('\'') != -1:
            query[i] = parse_helper(query[i])
            remove_quote = query[i].split('\'')
            for i in remove_quote:
                i = i.lower()
                temp.append(i)
        else:
            query[i] = parse_helper(query[i])
            query[i] = query[i].lower()
            temp.append(query[i])
    return temp


def parse_helper(ele):
    ele = ele.strip(',""()')
    ele = ele.replace('.', '')
    return ele


def stopping(query):
    f = open('stoplist.txt', 'r')
    stop_list = []
    for line in f:
        line = line.rstrip('\n')
        stop_list.append(line)
    for i in stop_list:
        for j in range(0, len(query)):
            temp_query = []
            for k in range(0, len(query[j])):
                if i == query[j][k]:
                    pass
                else:
                    temp_query.append(query[j][k])
            query[j] = temp_query
    f.close()
    return query


def stemming():
    f = open('stem-classes.lst', 'r')
    cmd_list = []
    stemming_list = []
    grep_cmd = 'grep -i -w' + ' dofesfet' + \
               ' ~/Dropbox/homework/IR-PROJ2/stem-classes.lst'
    process = subprocess.Popen(grep_cmd, stdout=subprocess.PIPE, shell=True)
    temp = process.communicate()[0]
    cmd_list.append(temp)
    print cmd_list
    #for line in f:
        #line = line.rstrip('\n')
        #line = line.split('|')
        #temp = []
        #for ele in line:
            #ele = ele.strip()
            #temp.append(ele)
        #stemming_list.append(temp)
    print stemming_list


queries = get_query()
queries_after_stopping = stopping(queries)
stemming()
