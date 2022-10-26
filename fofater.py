# -*- coding: utf-8 -*-
import os
import sys
import csv
import time
import fofa
from colors import ColorOutput as Color


# Please use your accounts & token
config = {
        'email': '', 
        'token': ''
        }

banner = '''
 ______     __      _            
|  ____|   / _|    | |           
| |__ ___ | |_ __ _| |_ ___ _ __ 
|  __/ _ \|  _/ _` | __/ _ \ '__|
| | | (_) | || (_| | ||  __/ |   
|_|  \___/|_| \__,_|\__\___|_|  by forbis.

'''


init = fofa.Client(config['email'], config['token'])
colorprint = Color()
print(banner)

try:
    colorprint.writeln('Login success!', 'b_green')

except:
    exit(colorprint.writeln('Email or token error!', 'b_red'))


# Get user info
def printInfo():
    userinfo = init.get_userinfo()
    colorprint.writeln('+===================================+', 'b_yellow')
    colorprint.write('username: ', 'b_cyan')
    colorprint.writeln(f'{userinfo["username"]}')
    colorprint.write('coin: ', 'b_cyan')
    colorprint.writeln(f'{userinfo["fcoin"]}')
    colorprint.write('email: ', 'b_cyan')
    colorprint.writeln(f'{userinfo["email"]}')
    colorprint.writeln('+===================================+', 'b_yellow')


# Get fofa results
def parseResult(query, maxresults):
    results = []
    pages = init.get_data(query)['size'] // 100 + 1
    print(f'pages: {pages}')
    for page in range(1, pages + 1):
        try:
            results += init.get_data(query, page, 'host,ip,port,title')['results']
        except:
            pass

        if len(results) >= maxresults:
            break
    
    return results


# Check current path has 'results' folder
def checkFolder():
    ls = os.listdir()
    if 'results' not in ls:
        os.makedirs('results')


# Save results to file with specific file type.
def saveResults(name, results, filetype='txt'):
    if filetype in ['txt', 'html']:
        with open('./results/' + name + 
                  '.' + filetype, 'w+', encoding='UTF-8') as file:
            for res in results:
                if filetype == 'txt':
                    file.write(f'{res[0]}\n')

                elif filetype == 'html':
                    file.write(f'<a href="http://{res[0]}" target="_blank">{res[3]}</a><p>IP: {res[1]}  Port: {res[2]}</p></br>')

        file.close()
    
    else:
        cols = ['URL', 'IP', 'PORT', 'Title']
        with open('./results/' + name + 
                  '.' + filetype, 'w+', encoding='utf_8_sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(cols)
            for res in results:
                writer.writerow(res)

        file.close()


def checkArg(arg):
    index = sys.argv.index(arg) + 1
    if index < len(sys.argv):
        return sys.argv[index]

    else:
        exit(f'{arg} no value')


def Help():
    print(f'''
        Usage: python {sys.argv[0]} -q <search query> [argvs]\n
        argvs:\n
        \t-q : Search query.\n
        \t-f : Output file type. Support txt, html, csv. Default is txt. 'all' is save output with all file type\n
        \t-o : Output file name. Default is "query + current time".\n
        \t-p : Print user infomation.\n
        \t-n : Get the max results in this search. Default is 10000.\n
        example:\n
        \tpython {sys.argv[0]} -q header="thinkphp" -f csv -o test
        ''')

# TODO: progress bar & refect fofa model.
if __name__ == '__main__':
    filetype = 'txt'
    filename = ''
    maxresults = 10000
    if '-p' in sys.argv:
        printInfo()
        exit()

    if ('-h' in sys.argv) or ('-q' not in sys.argv):
        Help()
        exit()
    
    if '-f' in sys.argv:
        filetype = checkArg('-f')
    
    if '-o' in sys.argv:
        filename = checkArg('-o')

    if '-n' in sys.argv:
        maxresults = int(checkArg('-n'))

    query = checkArg('-q')
    filename = filename if filename else query + '_' + time.strftime('%Y%m%d%H%M', time.localtime())
    res = parseResult(query, maxresults)
    checkFolder()
    if filetype == 'all':
        for t in ['txt', 'html', 'csv']:
            saveResults(filename, res, t)

    else:
        saveResults(filename, res, filetype)

    colorprint.writeln(f'Finish. save file in ./results/{filename}', 'b_green')
