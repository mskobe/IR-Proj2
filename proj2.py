import subprocess
import requests
import re
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
    for i in range(1, len(query)):
        if query[i] == '' or query[i] == 'Document':
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
    query_length = 0
    #file_address = ' ~/Dropbox/homework/IR-PROJ2/stem-classes.lst'
    file_address = 'stem-classes.lst'
    for i in range(0, len(query)):
        query_length += len(query[i])
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
    avg_query_len = float(query_length) / 25
    print avg_query_len
    return query, avg_query_len


def send_request(query, avg_query_len):
    f = open('requests_url', 'w')
    avg_doclen = get_avg_doclen(3)
    for i in range(0, len(query)):
        score = {}
        query_length = len(query[i])
        for j in range(1, len(query[i])):
            #make_url = 'http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=3&g=p'
            make_url = 'http://10.0.0.176/~zerg/lemurcgi/lemur.cgi?d=3&g=p'
            make_url += '&v=' + query[i][j]
            f.write(make_url)
            f.write('\n')
            r = requests.get(make_url)
            html = r.text
            parsed_html = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(html).group(1)
            numbers = re.compile(r'(\d+)', re.DOTALL).findall(parsed_html)
            #numbers = parse_html(html)
            ctf, df = float(numbers[0]), float(numbers[1])
            inverted_list = map(lambda i: (int(numbers[2 + 3*i]), \
                                           float(numbers[3 + 3*i]),\
                                           float(numbers[4 + 3*i]))\
                                ,range(0, (len(numbers) - 2)/3))
            #print "ctf= %(ctf)f df= %(df)f" % {'ctf': ctf, 'df':df}
            for (docid,doclen,tf) in inverted_list:
                if docid in score:
                    score[docid] += cal_socre(doclen, tf, avg_doclen) * \
                                    cal_query_oktf(query_length, tf, avg_query_len)
                else:
                    score[docid] = cal_socre(doclen, tf, avg_doclen) * \
                                   cal_query_oktf(query_length, tf, avg_query_len)
        sorted_score = sorted(score.iteritems(), key=lambda d:d[1], reverse=True)
        print sorted_score
    f.close()


#def parse_html(html):
    #parsed_html = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(html).group(1)
    #numbers = re.compile(r'(\d+)', re.DOTALL).findall(parsed_html)
    #return numbers


def get_avg_doclen(database_num):
    url = 'http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=?'
    r = requests.get(url)
    html = r.text
    parsed_html = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(html).group(1)
    numbers = re.compile(r'(\d+)', re.DOTALL).findall(parsed_html)
    #numbers = parse_html(html)
    avg_doclen = numbers[5*(database_num-1)+4]
    return avg_doclen


def cal_socre(doclen, tf, avg_doclen):
    score = float(tf) / (tf+ 0.5 + 1.5*doclen/avg_doclen)
    return score


def cal_query_oktf(query_length, tf, avg_query_len):
    query_oktf = float(tf) / (tf + 0.5 + 1.5*query_length/avg_query_len)
    return query_oktf


queries = get_query()
queries_after_stopping = stopping(queries)
queries_after_stemming, avg_query_len = stemming(queries_after_stopping)
send_request(queries_after_stemming, avg_query_len)
