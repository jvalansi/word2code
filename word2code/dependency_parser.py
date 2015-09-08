'''
Created on Jul 19, 2015

@author: jordan
'''
import copy
import re
from nltk.parse import stanford
from stanford_corenlp import raw_parse_sents, tokenize_sentences
import astor
from utils import *
import logger
import doctest

class Node:
    def __init__(self, name = '', parent = None, children = None, ntype = None):
        self.name = name
        self.parent = parent
        self.ntype = ntype
        if not children:
            self.children = []
    
    def insert_child(self, node):
        self.children.append(node)
        node.parent = self

    
    def is_loop(self, name):
        node = self
        while node: #prevent loop
            if node.name == name:
                return True
            node = node.parent
        return False
    
#     def deps2tree_(self, deps):
#         
#         for dep in deps:
#             if not dep[-2] == self.name:
#                 continue
#             if self.is_loop(dep[-1]):
#                 continue
#             node = Node(dep[-1],self)
#             if len(dep) > 2:
#                 node.ntype = dep[0]
#             self.children.append(node)
#             node.deps2tree_(deps)
#         return self


    def deps2tree(self, deps):
        deps_ = copy.copy(deps)
        for dep in deps:
            node = None
            if self.name == dep[-2]:
                node = Node(dep[-1],self)
            if self.name == dep[-1]:
                node = Node(dep[-2],self)
            if not node:
                continue                
            if len(dep) > 2:
                node.ntype = dep[0]
            self.children.append(node)
            deps_.remove(dep)
            node.deps2tree(deps_)

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
    
    def ast2tree(self, parse):
        if hasattr(parse, 'func'):
            self.name = parse.func.id
        elif hasattr(parse, 'id'):
            self.name = parse.id
        elif hasattr(parse, 'n'):
            self.name = str(parse.n)
        if hasattr(parse, 'args'):
            for arg in parse.args:
                node = Node(parent=self)
                self.children.append(node)
                node.ast2tree(arg)
#         if isinstance(parse, list):
#             for p in parse:
#                 node = Node(parent=self)
#                 self.children.append(node)
#                 node.ast2tree(p)
#         else: 
#             for k,v in parse.__dict__.items():
#                 if not hasattr(v, '__dict__') and not isinstance(v, list):
#                     continue
#                 node = Node(parent=self, ntype=k)
#                 self.children.append(node)
#                 node.ast2tree(v)
        return self
        
    
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
        
    def safe_remove(self):
        if not self.parent:
            if self.children:
                node = self.children[0]
                self.swap(node)
                node.safe_remove()
            else:
                node = Node('')
                self.swap(node)
        else:
            self.parent.children.remove(self)
            for child in self.children:
                child.parent = self.parent
                self.parent.children.append(child)
        
    def filter_words(self, words):
        '''
        reduce tree to consist of only the given words

        >>> deps = [[None, 'csubsets', 'input_array']]
        >>> root = Node('csubsets')
        >>> root.deps2tree(deps)
        >>> root.filter_words(['input_array'])
        >>> print(root)
        input_array
        
        >>> root = Node('csubsets')
        >>> root.filter_words([])
        >>> print(root)
        <BLANKLINE>

        :param words:
        '''
        children = copy.copy(self.children)
        for child in children:
            child.filter_words(words)
        if self.name not in words:
            self.safe_remove()

    def translate(self,transdict):
        if self.name in transdict:
            self.name = transdict[self.name]
        for child in self.children:
            child.translate(transdict)
        return self

    def clear_ntypes(self):
        self.ntype = None
        for child in self.children:
            child.clear_ntypes()
            
    def clean_ind(self):
        self.name = dep2word(self.name)
        for child in self.children:
            child.clean_ind()

    def swap(self, node):
        self.name, node.name = node.name, self.name
        self.ntype, node.ntype = node.ntype, self.ntype  

    def rearrange(self):
        for child in self.children:
            if not is_func(self.name) and is_func(child.name):
                self.swap(child)
            child.rearrange()
        if not self.children and is_func(self.name):
            node = Node("possibility")
            self.insert_child(node)
        try:
            eval(str(self))
        except TypeError as e:
            logger.logging.debug('TypeError')
            logger.logging.debug(e)
            node = Node("possibility")
            self.insert_child(node)
            return
        except (NameError, SyntaxError, ValueError) as e:
            logger.logging.debug('eval Error')
            logger.logging.debug(e)
            return
            
    def compare(self, tree):
        deps1 = self.tree2deps()
        deps2 = tree.tree2deps()
        return [dep for dep in deps1 if dep not in deps2]

    def fix_type(self):
        '''
        make sure all children have the same type, otherwise, cast
        '''
        for child in self.children:
            child.fix_type()
        try:
#             print(map(str, self.children))
            children_types = [type(eval(str(child))).__name__ for child in self.children]
        except (TypeError, NameError, SyntaxError, ValueError) as e:
            logger.logging.debug('eval Error')
            logger.logging.debug(e)
            logger.logging.debug(e.args)
            return
        if 'int' in children_types:
#             children = copy.copy(self.children)
            for child, child_type in zip(self.children, children_types):
                if child_type == 'list':
                    node = Node('len')
                    self.children.remove(child)
                    self.children.append(node)
                    node.parent = self
                    node.children.append(child)
                    child.parent = node
        
    def clean_duplicates(self, nodes=[]):
        for child in self.children:
            child.clean_duplicates(nodes)
        if self.name in nodes:
            self.safe_remove()
        else:
            nodes.append(self.name)


def clean_duplicates(tree):
    deps = tree.tree2deps()
    deps = map(tuple, deps)
    deps = list(set(deps))
    deps = map(list, deps)
    new_tree = Node(tree.name)
    return new_tree.deps2tree(deps)

def dep2list(dep):
    m = re.match('^(.+)\((.+\-\d+)\'?, (.+\-\d+)\'?\)$', dep)
    if not m:
        return []
    return list(m.groups())


def dep2ind(dep):
    return int(dep2dict(dep)['ind'])

def dep2word(dep):
    return dep2dict(dep)['word']

def dep2dict(dep):
    m = re.search('(?P<word>[^-]+)?-?(?P<ind>\d+)?', dep)
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


dependencies_dict = {}
dependencies_path = os.path.join('res', 'dependencies') 

def load_dependencies_dict():
    if not os.path.exists(dependencies_path):
        return
    with open(dependencies_path) as f:
        dependencies_dict.update(json.load(f))

def dump_dependencies_dict():
    with open(dependencies_path, 'w') as f:
        json.dump(dependencies_dict, f)

def sentence2dependencies(sentence):
    load_dependencies_dict()    
    if sentence in dependencies_dict:
        return dependencies_dict[sentence]
    dependencies = raw_parse_sents([sentence])
    dependencies = [[dep2list(dep) for dep in sentence_dependencies.split('\n')] for sentence_dependencies in dependencies.split('\n\n')]
    dependencies_dict[sentence] = dependencies
    dump_dependencies_dict()
    return (dependencies)

def get_features(sentence):
    '''
    extract dependency relations as features for sentence
    
    :param sentence:
    '''
#     sentwords = nltk.word_tokenize(sentence.lower())
    sentwords = tokenize_sentences(sentence)[0]
    dependencies = sentence2dependencies(sentence)[0] #TODO: check if bug
    features = ['O']*len(sentwords)
    for dep in dependencies:
        m0 = dep2dict(dep[-1])
        m1 = dep2dict(dep[-2])
        features[int(m0['ind'])-1] = 'I'
        features[int(m1['ind'])-1] = 'I'
    for dep in dependencies:
        m = dep2dict(dep[-1])
        features[int(m['ind'])-1] = dep[0] 
    return features

def main():
    sentence = 'hello my friend, how are you?'
#     print(sentence2dependencies(sentence))
    
    dep = 'hello-1'
    print(dep2word(dep))
    
    doctest.testmod()

if __name__ == '__main__':
    main()