# -*- coding: utf-8 -*-

import os
import re
import misc
import MeCab
import codecs

def get_dirs(root_dir):
    for top, dirs, files in os.walk(root_dir):
        yield top
        for f in files:
            yield os.path.join(top, f)

def ret_str_cfile(file, exclude_set):
    f = open(file)
    text = f.read() 
    f.close()
    ary = re.split('[^a-zA-Z0-9]',text)
    line = ""
    for word in ary:
        w = misc.clean_str(word)
        if(len(w) > 1 and w not in exclude_set):
            line = line + w + " "
    return line

def ret_str_htmlfile(file):
    f = open(file)
    text = f.read() 
    f.close()
    text = re.sub(r'<[^>]+>', ' ', text.lower())
    ary = re.split('[^a-zA-Z0-9]',text)
    line = ""
    for word in ary:
        w = misc.clean_str(word)
        if(len(w) > 1):
            line = line + w + " "
    return line

def ret_str_htmlfile_ja(file):
    f = codecs.open(file, 'r', 'euc_jp')
    text = f.read()
    text = re.sub(r'<[^>]+>', ' ', text.lower())
    text = re.sub(r'[\.\,\=\_\|\!\(\)\*\@\[\]\#\;\-\~\\\&\{\}\"\'0-9]', '', text)
    m = MeCab.Tagger()
    utf8_text = text.encode('utf-8')
    node =  m.parseToNode(utf8_text)
    line = ""
    while node:
        line = line + node.surface + " " if len(node.surface) > 3 else line
        node = node.next
    return line

def read_set(file_name):
    ret = set()
    for line in open(file_name, 'r'):
        ret.add(misc.clean_str(line))
    return ret
    
def main():
    c_exclude_set = read_set("exclude.txt")
    for file in get_dirs('../data/postgresql-9.3.4'):
        if re.match(r'.+(html\-ja).+\.(html)$', file):
            # .html ja file
            print file + "\t" + ret_str_htmlfile_ja(file) 
        elif  re.match(r'.+\.(html)$', file):
            # .html file
            print file + "\t" + ret_str_htmlfile(file) 
        elif re.match(r'.+\.(c|h)$', file):
            # .c or .h files 
            print file + "\t" + ret_str_cfile(file, c_exclude_set) 

if __name__=="__main__":
    main()
