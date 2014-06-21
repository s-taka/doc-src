#import misc
import sys
import re

def main():
    if (len(sys.argv) != 2):
        print('Usage: $ python %s datafile > outfile' % sys.argv[0])
        quit()
    file_name = sys.argv[1]
    dic = {}
    for line in open(file_name, 'r'):
        [doc_name, data] = line.split('\t')
        dic_tmp = {}
        keys = re.split('\s',data)
        for key in keys:
#            key = misc.clean_str(k)
            if(len(key) > 1):
                dic_tmp[key] = 1
        for key in dic_tmp:
            if key in dic:
                dic[key] = dic[key] + 1
            else:
                dic[key] = 1
    for key in dic:
        print("%s\t%d\t" % (key, dic[key]))        
        
if __name__=="__main__":
    main()
