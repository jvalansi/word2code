'''
Created on Jul 19, 2015

@author: jordan
'''
import copy
import re
from nltk.parse import stanford
from stanford_corenlp import raw_parse_sents
class Node:
    def __init__(self, name = '', parent = None, children = None, ntype = None):
        self.name = name
        self.parent = parent
        self.ntype = ntype
        if not children:
            self.children = []
    
    def is_loop(self, name):
        node = self
        while node: #prevent loop
            if node.name == name:
                return True
            node = node.parent
        return False
    
    def deps2tree(self, deps):
        for dep in deps:
#             print(dep)
#             if dep[-2] == dep[-1]: #prevent loop
#                 continue
            if not dep[-2] == self.name:
                continue
            if self.is_loop(dep[-1]):
                continue
            node = Node(dep[-1],self)
            if len(dep) > 2:
                node.ntype = dep[0]
            self.children.append(node)
            node.deps2tree(deps)
        return self

    def tree2deps(self):
        deps = []
        for child in self.children:
            deps.append([child.ntype, self.name, child.name])
            deps.extend(child.tree2deps())
        return deps

    def split_args(self, args):
        level = 0
        s = 0
        args_ = []
        for i,c in enumerate(args):
            if c == '(' or c == '[':
                level += 1
            if c == ')' or c == ']':
                level -= 1
            if level == 0 and c in [',',' ']:
                args_.append(args[s:i])
                s = i+1
        args_.append(args[s:])
        return args_                
    
    def code2tree(self, code):
    #     return(min([mapping(possibility, input_array) for possibility in possibilities]))
    #     ROOT, return
    #     return, min
    #     min, mapping
    #     min, possibility
    #     mapping, possibility
    #     min, possibilities
    #     
    #     each recursive step:
    #         add function to tree
    #         split args
    #         for each arg:
    #             repeat
        print(code)
        m = re.match('\s*(?:(?P<ntype>\w+)=)?(?P<func>\w+)?(?:[\(\[](?P<args>.+)[\)\]])?\s*', code)
        ntype = m.group('ntype')
        print(ntype)
        func = m.group('func')
#         print('func: '+str(func)+' ntype: '+str(ntype))
        if func:
            func_node = Node(func)
            func_node.parent = self
            if ntype:
                func_node.ntype = ntype
            self.children.append(func_node)
        else:
            func_node = self
        args = m.group('args')
        if not args:
            return
        args = func_node.split_args(args)
        for arg in args:
            func_node.code2tree(arg)
        
    def __str__(self):
        s = ''
        if self.ntype:
            s = self.ntype + '='
        s += self.name
        if self.children:
            s += '('
            s += ', '.join([str(child) for child in self.children])
            s += ')'
        return s
        
    def get_nodes(self):
        nodes = []
        nodes.append(self.name)
        for child in self.children:
            nodes.extend(child.get_nodes())
        return nodes
        


def dep2list(dep):
    m = re.match('^(\w+)\((.+\-\d+)\'?, (.+\-\d+)\'?\)$', dep)
    if not m:
        return []
    return list(m.groups())


def dep2ind(dep):
    return int(re.search('(?:.+)?-(\d+)\'?', dep).group(1))

def dep2word(dep):
    return re.search('(.+)?-(?:\d+)\'?', dep).group(1)

def dep2dict(dep):
    m = re.search('(?P<word>[\w\-\+\=]+)?-(?P<ind>\d+)', dep)
    return m.groupdict()

# filter dependencies according to words
#     unimportant words should be contracted to their parents
def filter_dep(dependencies, words):
    mappings = {}
#     print(dependencies)
#     print(words)
    new_dependencies = copy.copy(dependencies)
    while True:
        change = False
        for dep in dependencies:
            if dep not in new_dependencies:
                continue
#             child = re.search('(\w+)-\d+', dep[2]).group(1)
            child = dep[2]
#             parent = re.search('(\w+)-\d+', dep[1]).group(1)
            parent = dep[1]
    #         if the child is unimportant add mapping of child to parent
            if dep2word(child) not in words:
#                 print('dep: ' + str(dep))
#                 print('child: ' + str(child))
                mappings[child] = parent
                new_dependencies.remove(dep)
                change = True
    #         if parent is in mapping, do mapping (switch)
            elif parent in mappings:
#                 print('dep: ' + str(dep))
#                 print('parent: ' + str(parent))
#                 print('mapping: ' + str(mappings[parent]))
                new_dependencies.remove(dep)
#                 dep[1] = re.sub('^\w+',mappings[parent],dep[1])
                dep[1] = mappings[parent]
                new_dependencies.append(dep)
                change = True
        if not change:
            break
    return new_dependencies

def clean_dependencies(dependencies):
    clean_deps = []
    for dep in dependencies:
#         print(dep)
#         child = dep2word(dep[2])
        child = dep[2]
#         parent = dep2word(dep[1])
        parent = dep[1]
        clean_deps.append([parent,child])
    return clean_deps


def sentence2dependencies(sentence):
    dependencies = raw_parse_sents([sentence])
    dependencies = [[dep2list(dep) for dep in sentence_dependencies.split('\n')] for sentence_dependencies in dependencies.split('\n\n')]
    return (dependencies)

if __name__ == '__main__':
    sentence = 'hello my friend, how are you?'
    print(sentence2dependencies(sentence))
