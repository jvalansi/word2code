'''
Created on Jan 11, 2015

@author: jordan
'''
import re
import os

WORD = '[\w\-,\=\'\.><\d\+/]+'

class SentenceParser:

    def parse_sentence(self,sentence):
        with open('temp', 'w') as temp_file:
            temp_file.write(sentence)
        parse = self.parse_file('temp')
        os.remove('temp')
        return parse

    def parse_file(self,filename):
        parser_out = os.popen("~/Downloads/stanford-parser-full-2014-08-27/lexparser.sh "+filename).readlines()

        parse_list = self.parse2list(parser_out)
        parses = []
        for parse0,parse1 in parse_list:
            parse0 = re.sub("\s+", " ",parse0)
    #         print(parse0)
            parse_tree = self.parse2tree(parse0)
#             print(parse_tree)
#             parse_lambda = parse2lambda(parse_tree)
    #         print(len(parse_lambda))
            parse1 = parse1.split('\n')
            relations = self.parse2relations(parse1)
#             print(relations)
#             for r in relations:
#                 print(relation2string(r,relations[r]))
            parses.append((parse_tree,relations))
        return parses


    def parse2list(self,parse):
        parse = "".join(parse)
        parse_list = parse.split('\n\n')
        parse_list = [(parse_list[2*i],parse_list[2*i+1]) for i in range(len(parse_list)/2) ]
        return parse_list

    def get_parentheses(self,parse):
        depth = 0
        for i in range(len(parse)):
            if parse[i] == '(':
                depth += 1
            if parse[i] == ')':
                depth -= 1
            if depth == 0:
                return parse[:i+1]
        return None

    def parse2tree(self,parse):
    #     get string surrounded by parenthesis return dictionary
    #    input: (NAME (NAME VALUE) (NAME VALUE))
    #    output: {"NAME": {"NAME": VALUE, "NAME": VALUE}}
    #     print(parse)
        if parse[0] != '(':
            return parse.split(')')[0] #return VALUE
        d = []
        while len(parse) > 0:
            parentheses = self.get_parentheses(parse)
            parse = parse[len(parentheses):].strip()
            parentheses = parentheses[1:-1] #remove parentheses
            name = parentheses.split()[0]
            value = self.parse2tree(parentheses[len(name):].strip())
            d.append((name, value))
        return d


    def parse2lambda(self,parse):
        if not isinstance(parse, dict):
            return parse
        lmbd = ''
        if len(parse) == 1:
            lmbd = parse.keys()[0]
            parse = parse[lmbd]
            result = lmbd+'('+ str(self.parse2lambda(parse)) + ')'
            return result
        if len(parse) >= 2:
            lmbd = parse.keys()
            lmbd1 = lmbd.pop(1)
            parse = parse[lmbd1]
            result = lmbd1+'('+ ','.join(lmbd)+','+str(self.parse2lambda(parse)) + ')'
            return result

    def parse2relations(self,parse):
        relations = []
        for p in parse:
            m  = re.search('('+WORD+')\(('+WORD+')-\d+, ('+WORD+')-\d+\)', p)
            if m == None:
                with open('problems','a') as problems_file:
                    problems_file.write(p)
                continue
            relation = m.group(1)
            head = m.group(2)
            tail = m.group(3)
#             if relation not in relations:
#                 relations[relation] = {}
            relations.append((relation,(head,tail)))
        return relations

    def relation2string(self,relation,args):
        m = re.search('('+WORD+')-\d+', str(relation))
        func = m.group(1)
        s = func +'('
        for a in args:
            argname = str(a)
            m = re.search('('+WORD+')-\d+', str(args[a]))
            argvalue = m.group(1)
            s+=  argname+'='+argvalue+','
        s += ')'
        return s


