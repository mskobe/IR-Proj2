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
    print queries


def parse_query(line):
    query = line.split(' ')
    temp = []
    for i in range(0, len(query)):
        if query[i] == '':
            pass
        elif i == 0:
            query[0] = query[0].rstrip('.')
            temp.append(query[0])
        elif query[i].find('-') != -1:
            query[i] = query[i].rstrip(',')
            remove_hyphen = query[i].split('-')
            for i in remove_hyphen:
                temp.append(i)
        else:
            query[i] = query[i].rstrip(',')
            temp.append(query[i])
    return temp


def stopping(query):
    f = open('stoplist.txt', 'r')
    stop_list = []
    for line in f:
        line = line.rstrip('\n')
        stop_list.append(line)
    f.close()
    print stop_list


def stemming():
    f = open('stem-classes.lst', 'r')


get_query()
#stopping()
