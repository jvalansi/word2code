'''
Created on Jan 20, 2015

@author: jordan
'''
import os
import re
import word_count

'''
transform: return len( set(way for way in ways if valid(way) ))

return(len(set(foreach(height,ways,valid))))

to:     
    args(return,len)
    args(len,set)
    args(set, ways)
    elt(ways,way)
    map(way,way)
    ifs(way,valid)

    value(return,len)
    args(len,set)
    args(set,ListComp)
    elt(ListComp,way)
    iter(ways,way)
    ifs(way,valid)
    args(valid,way)
             
    value(return,len)
    args(len,set)
    args(set,ListComp)

    value(return,len)
    args(len,set)
    args(set,ListComp)
    elt(ListComp,map)
    args(map,way)
    gen

via: 
"Module(
    body=[
        Return(
            value=Call(
                func=Name(id='len', ctx=Load()), 
                args=[
                    Call(
                        func=Name(id='set', ctx=Load()), 
                        args=[
                            ListComp(
                                elt=Call(
                                    func=Name(id='map', ctx=Load()), 
                                    args=[Name(id='way', ctx=Load())], 
                                    keywords=[], 
                                    starargs=None, 
                                    kwargs=None
                                ), 
                                generators=[
                                    comprehension(
                                        target=Name(id='way', ctx=Store()), 
                                        iter=Name(id='ways', ctx=Load()), 
                                        ifs=[
                                            Call(
                                                func=Name(id='valid', ctx=Load()), 
                                                args=[Name(id='way', ctx=Load())], 
                                                keywords=[], 
                                                starargs=None, 
                                                kwargs=None
                                            )
                                        ]
                                    )
                                ]
                            )
                        ], 
                        keywords=[], 
                        starargs=None, 
                        kwargs=None
                    )
                ], 
                keywords=[], 
                starargs=None, 
                kwargs=None
            )
        )
    ]
)"
'''

def clean_code(s):
    marks = '\+\-=/\*\.,\''
    s = re.sub('(['+marks+']+)',' \\1 ', s)
    s = re.sub('\s+', ' ', s)
    s += '\n'
    return s

#     count code words
def count_code(dir):
#     input: dir
#     output: word count of code
    code_data = ""
#     go through all files in directory
    for fn in os.listdir(dir):
#         go through all lines in file            
        f = open(dir+fn,'r')
        for line in f.readlines():
#             stop when reaching main
            if re.search("if __name__ == '__main__':", line):
                break 
#            if comment (starts with '#') continue
            if re.search('^(\s+)?#.*', line) or \
                re.search("class\s.+:", line) or \
                re.search("def\s.+:", line) or \
                re.search('input_array\d?\s=', line) or \
                re.search('input_int\d?\s=', line):
                continue
            if not re.search('valid\s*=', line):
                continue
#             else add to code data
            code_data += clean_code(line)
    wc = word_count.WordCount()
    wc.count_words(code_data, "code_data")
    print(code_data)
            
            
if __name__ == '__main__':
    count_code('res/text&code2/')