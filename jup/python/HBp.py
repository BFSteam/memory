#!/usr/bin/python
import csv
import os
import sys
import getopt


from os import listdir
from os.path import isfile, join

#strmatch = ''
#fullpath = '.'
#outname = ''


def setup_options(argv):
    arggg = {
        'inputpath': './',
        'outputpath': './out.csv',
        'strmatch': '',
    }
    functions = []
    try:
        opts, args = getopt.getopt(
            argv, "ahi:no:s:", [
                "ifile=", "ofile=", "strmatch="])
    except getopt.GetoptError:
        print('Invalid options: use -h for help')
        sys.exit(42)
    for opt, arg in opts:
        if opt == '-h':
            print('HBp.py -i <inputfile> -o <outputfile> -s <stringmatch> -a -n')
            print(
                'HBp.py --ifile=<inputfile> \\\n --ofile=<outputfile> \\\n --strmatch=<stringmatch>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            arggg['inputpath'] = arg
        elif opt in ("-o", "--ofile"):
            arggg['outputpath'] = arg
        elif opt in ("-s", "--strmatch"):
            arggg['strmatch'] = arg

        elif opt in '-a':
            functions.append('a')
        elif opt in '-n':
            functions.append('n')
    print('Input file is:', arggg['inputpath'])
    print('Output file is:', arggg['outputpath'])

    return arggg, functions


def path_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def path_writable(path):
    if os.access(os.path.dirname(path), os.W_OK):
        return True
    else:
        return False


def parse_path(inputpath, outputpath):

    if not path_exists(inputpath):
        print("ERROR: input file not found")
        sys.exit(42)

    if not path_exists(outputpath):
        if path_writable(outputpath):
            print("Generating new file at", outputpath)
        else:
            print("WARNING: Seems", outputpath, "is not writeable")
            if outputpath[0] != '.' and outputpath[1] != '/':
                choice = str(
                    input(
                        'Can I use ./' +
                        outputpath +
                        '? (y/n)'))
            if choice == 'y':
                print("Changing the output path to", './' + outputpath)
                outputpath = './' + outputpath
            else:
                sys.exit(42)
    else:
        choice = str(
            input(
                "WARNING: file " +
                outputpath +
                " exists: continue? (y/n)"))
        if choice == 'y':
            pass
        else:
            sys.exit(42)

    return inputpath, outputpath


def data_analysis_on_news(argdict):

    #f_path = '/'.join(fullpath.split('/')[:-1])

    f_path = argdict['inputpath']
    outname = argdict['outputpath']
    strmatch = argdict['strmatch']

    outname = outname[:outname.find(
        "csv") - 1] + '_news' + outname[outname.find('csv') - 1:]

    f_path, outname = parse_path(f_path, outname)
    print("Running analysis on news using file", outname)

    f_name = sorted(set([f[f.find(strmatch):f.find(strmatch) + 19]
                         for f in listdir(f_path) if isfile(join(f_path, f)) and strmatch in f]))
    # print('f_name:',f_name)
    f_dict = {key: {} for key in f_name}
    for fn in f_name:
        f_list = [
            f for f in listdir(f_path) if isfile(
                join(
                    f_path,
                    f)) and fn in f]
        # print(f_list)
        f_dict[fn]['clustering'] = [
            x for x in f_list if 'clustering' in x][0]
        f_dict[fn]['memory'] = [x for x in f_list if 'memory' in x][0]
        f_dict[fn]['connection'] = [
            x for x in f_list if 'connection' in x][0]
        f_dict[fn]['message'] = [x for x in f_list if 'message' in x][0]
        f_dict[fn]['diameter'] = [
            x for x in f_list if 'diameter' in x][0]
        f_dict[fn]['graph'] = [
            x for x in f_list if 'graph' in x and 'graphN' not in x][0]
        # print(f_dict[f_name[5]])

    with open(outname, 'w') as writefile:
        pass
    for fn in f_name:
        print('Working on file:', fn)
        time = 0
        users = 0
        sources = 0
        state = 0
        memory = 0
        newslist = []
        with open(f_path + '/' + f_dict[fn]['memory'], 'r') as readfile:
            csvreader = csv.reader(readfile, delimiter=',')
            for i, row in enumerate(csvreader):
                if 'simulation' in row[0]:
                    time = int(row[1])
                if 'N_USERS' in row[0]:
                    users = int(row[1])
                if 'N_SOURCES' in row[0]:
                    sources = int(row[1])
                if 'dim' in row[0]:
                    state = int(row[1])
                if i > 1 and 'memory' in row[0]:
                    memory = int(row[1])
                if i > 12 and i < 12 + 1 + sources:
                    newslist.append(row[3])
                if i > 12 + 1 + sources:
                    break

        print(time, users, sources, state, memory)
        temp_news_dict = {key: list([0] * time) for key in newslist}
        print(newslist == list(temp_news_dict.keys()))

        with open(f_path + '/' + f_dict[fn]['memory'], 'r') as readfile:
            csvreader = csv.reader(readfile, delimiter=',')
            for i, row in enumerate(csvreader):
                if i < 13:
                    continue
                for new in row[3:]:
                    if new == '0':
                        continue
                    temp_news_dict[new][int(float(row[1])) - 1] += 1
        with open(outname, 'a') as writefile:
            csvwriter = csv.writer(writefile, delimiter=',')
            for key in temp_news_dict:
                csvwriter.writerow(temp_news_dict[key])


def data_analysis_on_agents(argdict):

    #f_path = '/'.join(fullpath.split('/')[:-1])

    f_path = argdict['inputpath']
    outname = argdict['outputpath']
    strmatch = argdict['strmatch']

    outname = outname[:outname.find(
        "csv") - 1] + '_agents' + outname[outname.find('csv') - 1:]

    f_path, outname = parse_path(f_path, outname)

    print("Running Analysis on Agents using file", outname)

    f_name = sorted(set([f[f.find(strmatch):f.find(strmatch) + 19]
                         for f in listdir(f_path) if isfile(join(f_path, f)) and strmatch in f]))
    # print('f_name:',f_name)
    f_dict = {key: {} for key in f_name}
    for fn in f_name:
        print(fn)
        f_list = [
            f for f in listdir(f_path) if isfile(
                join(
                    f_path,
                    f)) and fn in f]
        # print(f_list)
        f_dict[fn]['clustering'] = [
            x for x in f_list if 'clustering' in x][0]
        f_dict[fn]['memory'] = [x for x in f_list if 'memory' in x][0]
        f_dict[fn]['connection'] = [
            x for x in f_list if 'connection' in x][0]
        f_dict[fn]['message'] = [x for x in f_list if 'message' in x][0]
        f_dict[fn]['diameter'] = [
            x for x in f_list if 'diameter' in x][0]
        f_dict[fn]['graph'] = [
            x for x in f_list if 'graph' in x and 'graphN' not in x][0]
        # print(f_dict[f_name[5]])

    with open(outname + '.temp', 'w') as writefile:
        pass
    for fn in f_name:
        print('Working on file:', fn)
        time = 0
        users = 0
        sources = 0
        state = 0
        memory = 0
        newslist = []
        with open(f_path + '/' + f_dict[fn]['memory'], 'r') as readfile:
            csvreader = csv.reader(readfile, delimiter=',')
            for i, row in enumerate(csvreader):
                if 'simulation' in row[0]:
                    time = int(row[1])
                if 'N_USERS' in row[0]:
                    users = int(row[1])
                if 'N_SOURCES' in row[0]:
                    sources = int(row[1])
                if 'dim' in row[0]:
                    state = int(row[1])
                if i > 1 and 'memory' in row[0]:
                    memory = int(row[1])
                if i > 12 and i < 12 + 1 + sources:
                    newslist.append(row[3])
                if i > 12 + 1 + sources:
                    break

        print(time, users, sources, state, memory)
        #temp_news_dict ={ key : list([0]*time) for key in newslist}
        temp_ag_dict = {str(key + sources): [] for key in range(users)}
        #print(newslist == list(temp_news_dict.keys()))

        with open(f_path + '/' + f_dict[fn]['memory'], 'r') as readfile:
            csvreader = csv.reader(readfile, delimiter=',')
            for i, row in enumerate(csvreader):
                if i < 13:
                    continue
                if row[2] == 'x':
                    continue

                if row[2] == 'u':
                    temp_ag_dict[str(int(float(row[0])))].append(1)
                else:
                    temp_ag_dict[str(int(float(row[0])))].append(0)

        with open(outname + '.temp', 'a') as writefile:
            csvwriter = csv.writer(writefile, delimiter=',')
            for key in temp_ag_dict:
                csvwriter.writerow(temp_ag_dict[key])
    #uplist = [0]*time
    #downlist = [0]*time
    temp_time_dict = {'up': [], 'down': []}
    with open(outname + '.temp', 'r') as readfile:
        csvreader = csv.reader(readfile, delimiter=',')
        for row in csvreader:
            isup = False
            isdown = False
            timeup = 0
            timedown = 0
            for i, e in enumerate(row):
                if row[i] == '0':
                    isdown = True
                    timedown += 1
                else:
                    isup = True
                    timeup += 1
                if row[i] != row[i - 1] and i != 0:
                    if row[i] == '0':
                        temp_time_dict['up'].append(timeup)
                        timeup = 0
                        isup = False
                    else:
                        temp_time_dict['down'].append(timedown)
                        timedown = 0
                        isdown = False
    import numpy as np
    upunique, upcounts = np.unique(
        temp_time_dict['up'], return_counts=True)
    downunique, downcounts = np.unique(
        temp_time_dict['down'], return_counts=True)
    with open(outname, 'w') as writefile:
        csvwriter = csv.writer(writefile, delimiter=',')
        csvwriter.writerow(upunique)
        csvwriter.writerow(upcounts)
        csvwriter.writerow(downunique)
        csvwriter.writerow(downcounts)
    os.remove(outname + '.temp')


def main(argv):
    function_map = {'n': data_analysis_on_news,
                    'a': data_analysis_on_agents
                    }
    argdict, functions = setup_options(argv)
    for func in functions:
        function_map[func](argdict)


if __name__ == "__main__":
    main(sys.argv[1:])
