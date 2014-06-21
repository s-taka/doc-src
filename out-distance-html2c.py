import misc
import sys
import re
import math
import pprint

def inproduct_vec(lhs, rhs):
    keys = set(lhs.keys())
    keys.union(rhs.keys())
    lhs_sq = 0
    rhs_sq = 0
    lhsrhs = 0
    for key in keys:
        lhs_val = lhs[key] if key in lhs else 0.0
        rhs_val = rhs[key] if key in rhs else 0.0
        lhs_sq = lhs_sq + lhs_val * lhs_val
        rhs_sq = rhs_sq + rhs_val * rhs_val
        lhsrhs = lhsrhs + lhs_val * rhs_val
    
    return (lhsrhs / (math.sqrt(lhs_sq) * math.sqrt(rhs_sq))) if (lhs_sq * rhs_sq) > 0 else 0 

def get_neighbor_c(html_vec, c_dataset, maxnum):
    scores = {}
    ret = []
    for c_doc in c_dataset:
        scores[c_doc] = inproduct_vec(html_vec, c_dataset[c_doc])
    for dat in sorted(scores.items(), key=lambda x:x[1], reverse=True):
        ret.append(dat)
        if(len(ret) >= maxnum):
            break
    return ret

def main():
    if (len(sys.argv) != 3):
        print('Usage: $ python %s in.pickle outmax' % sys.argv[0])
        quit()
    data_file = sys.argv[1]
    outmax = int(sys.argv[2])

    all_dataset = misc.load_data(data_file)
    html_dataset = {}
    c_dataset = {}
    for doc in all_dataset:
        if re.match(r'.+\.(c|h)$', doc):
            c_dataset[doc] = all_dataset[doc]
        elif  re.match(r'.+\.(html)$', doc):
            html_dataset[doc] = all_dataset[doc]
    
    pp = pprint.PrettyPrinter(indent=4)

    
    for doc,val in sorted(html_dataset.items(), key=lambda x:(x[0])[::-1], reverse=True):
        neighbor = get_neighbor_c(html_dataset[doc], c_dataset, outmax)
        print '--%s--' % doc
        pp.pprint(neighbor)
        print ''
    
if __name__=="__main__":
    main()
