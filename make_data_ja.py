# -*- coding: utf-8 -*-

import os
import re
import misc
import MeCab
import codecs
import sys
from gensim.models import word2vec
import random

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

def ret_str_htmlfile_ja():
    def ret_str(file):
        f = codecs.open(file, 'r', 'euc_jp')
        text = f.read()
        text = re.sub(r'<[^>]+>', ' ', text.lower())
        text = re.sub(r'[\.\,\=\_\|\!\(\)\*\@\[\]\#\;\-\~\\\&\{\}\"\'0-9]', '', text)
        mecab = MeCab.Tagger()
        utf8_text = text.encode('utf-8')
        node =  mecab.parseToNode(utf8_text)
        line = ""
        while node:
            line = line + node.surface + " " if len(node.surface) > 3 else line
            node = node.next
        return line
    return ret_str

def ret_str_htmlfile_ja_word2vec(datafile):
    data = word2vec.Text8Corpus(datafile)
    model = word2vec.Word2Vec(data, size=100, window=10, min_count=2, workers=2)
    
    def ret_str(file):
        f = codecs.open(file, 'r', 'euc_jp')
        text = f.read()
        text = re.sub(r'<[^>]+>', ' ', text.lower())
        text = re.sub(r'[\.\,\=\_\|\!\(\)\*\@\[\]\#\;\-\~\\\&\{\}\"\'0-9]', '', text)
        mecab = MeCab.Tagger()
        utf8_text = text.encode('utf-8')
        node =  mecab.parseToNode(utf8_text)
        line = ""
        while node:
            if len(node.surface) > 3:
                word = node.surface
                if re.match(r'^[a-zA-Z0-9]+$', word):
                    line = line + word + " "
                else:
                    #jp
                    similars = []
                    sum_score = 0.0
                    if word.decode('utf-8') in model:
                        for w, score in model.most_similar(positive=word.decode('utf-8'), topn=10):
                            if re.match(r'^[a-zA-Z0-9]+$', w):
                                similars.append((w,score))
                                sum_score = sum_score + score
                        
                        rnd = sum_score * random.random()
                        sum_sim_score = 0.0
                        for w, score in similars:
                            sum_sim_score = sum_sim_score + score
                            if(rnd <= sum_sim_score):
                                line = line + w + " "
                                break
            node = node.next
        return line
    return ret_str


def read_set(file_name):
    ret = set()
    for line in open(file_name, 'r'):
        ret.add(misc.clean_str(line))
    return ret
    
def main():
    if (len(sys.argv) != 2 and len(sys.argv) != 3):
        print('Usage: $ python %s data_dir [use_word2vec_file] > outfile' % sys.argv[0])
        quit()
    data_dir = sys.argv[1]
    ret_strja = ret_str_htmlfile_ja()
    if(len(sys.argv) == 3):
        ret_strja = ret_str_htmlfile_ja_word2vec(sys.argv[2])
        
    c_exclude_set = read_set("exclude.txt")
    
    for file in get_dirs(data_dir):
        if re.match(r'.+(html\-ja).+\.(html)$', file):
            # .html ja file
            print file + "\t" + ret_strja(file)
        elif  re.match(r'.+\.(html)$', file):
            # .html file
            print file + "\t" + ret_str_htmlfile(file) 
        elif re.match(r'.+\.(c|h)$', file):
            # .c or .h files 
            print file + "\t" + ret_str_cfile(file, c_exclude_set) 

if __name__=="__main__":
    main()
