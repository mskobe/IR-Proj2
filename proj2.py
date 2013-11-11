import subprocess
import requests
from bs4 import BeautifulSoup
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


def stemming(query):
    f = open('stem-classes.lst', 'r')
    f2 = open('requests_url', 'w')
    stemming_list = []
    file_address = ' ~/Dropbox/homework/IR-PROJ2/stem-classes.lst'
    for i in range(0, len(query)):
        for j in range(0, len(query[i])):
            grep_cmd = 'grep -w ' + query[i][j] + file_address
            process = subprocess.Popen(\
                      grep_cmd, stdout=subprocess.PIPE, shell=True)
            temp = process.communicate()[0]
            if temp != '':
                stem = temp.split('|')
                query[i][j] = stem[0].strip()
            else:
                pass
        print query[i]
    return query


def send_request(query):
    f = open('requests_url', 'w')
    f2 = open('parsed_html', 'w')
    for i in range(0, len(query)):
        make_url = 'http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=3&g=p'
        for j in range(1, len(query[i])):
            print query[i][1]
            make_url += '&v=' + query[i][j]
        f.write(make_url)
        f.write('\n')
        r = requests.get(make_url)
        html = r.text
        soup = BeautifulSoup(html)
        parsed_html = soup.body
        f2.writelines(parsed_html)
        f2.write('\n\n')
    f.close()
    f2.close()


queries = get_query()
queries_after_stopping = stopping(queries)
queries_after_stemming = stemming(queries_after_stopping)
send_request(queries_after_stemming)
