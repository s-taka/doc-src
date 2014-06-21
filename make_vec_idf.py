import misc
import sys
import re
import math



def main():
    if (len(sys.argv) != 5):
        print('Usage: $ python %s dataset dic dic_alldoc_num out.pickle' % sys.argv[0])
        quit()
    ret = {}
    data_file = sys.argv[1]
    dic_file = sys.argv[2]
    doc_num = float(sys.argv[3])
    out_file = sys.argv[4]

    # read dic
    dic = {}
    for line in open(dic_file, 'r'):
        tmp = line.split('\t')
        dic[tmp[0]] = float(tmp[1])
    
    #make word vec
    for line in open(data_file, 'r'):
        [doc_name, data] = line.split('\t')
        dic_tmp = {}
        count_keys = 0.0
        keys = re.split('\s',data)
        for key in keys:
            if len(key) < 2:
                continue
            count_keys = count_keys + 1
            if key in dic_tmp:
                dic_tmp[key] = dic_tmp[key] + 1
            else:
                dic_tmp[key] = 1
        word_vec = {}
        for key in dic_tmp:
            word_vec[key] = (dic_tmp[key] / count_keys) * ( math.log( doc_num / dic[key] ))
        ret[doc_name] = word_vec

    #write word vec                
    misc.save_data(ret, out_file)
    
        
if __name__=="__main__":
    main()
