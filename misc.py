import re
import pickle

def clean_str(str):
    ret = re.sub(r'[^a-zA-Z]', '', str.lower())
    return ret 

def save_data(data, outfile):
    pickle.dump(data, open(outfile, "w"))

def load_data(infile):
    return pickle.load(open(infile))
    
