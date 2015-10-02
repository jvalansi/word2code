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
import ast

class Node:
    def __init__(self, name='', parent=None, children=None, ntype=None, code=None):
        self.name = name
        self.parent = parent
        self.ntype = ntype
        if not children:
            self.children = []
        if code:
            self.code2tree(code)
    
    def insert_child(self, node, ind=-1):
        if ind==-1:
            self.children.append(node)
        else:
            self.children.insert(ind, node)            
        node.parent = self

    def move_child(self, child, target):
        self.children.remove(child)
        target.insert_child(child)

    def remove_child(self, child):
        self.children.remove(child)
        for child_ in child.children:
            child_.parent = self
            self.children.append(child_)
        
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
        return self

    def tree2deps(self):
        deps = []
        for child in self.children:
            deps.append([child.ntype, self.name, child.name])
            deps.extend(child.tree2deps())
        return deps
    
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
        
    
    def code2tree_(self, code):
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
        args = split_args(args)
        for arg in args:
            func_node.code2tree_(arg)
        
    def code2tree(self, code):
        try:
            parse = ast.parse(code.strip())
        except SyntaxError as e:
            logger.logging.debug(e)
            return
        if not parse.body:
            return
        if not hasattr(parse.body[0], 'value'):
            logger.logging.debug('no value node')
            return
        self.ast2tree(parse.body[0].value)

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
        if a func is a child of a non-func - swap

        >>> root = Node(code = 'len(set(possibility))')
        >>> root.fix_type()
        >>> print(root)
        len(set(possibility))

        >>> root = Node(code = 'len(possibility(set))')
        >>> root.fix_type()
        >>> print(root)
        len(set(possibility))
        
        if a func is a comparison, the children must be of same type
        >>> root = Node(code = 'eq(1, diff(possibility, input_array))')
        >>> root.fix_type()
        >>> print(root)
        eq(1, len(diff(possibility, input_array)))
                
        >> if the number of arguments is too small, add possibility argument
        >>> root = Node(code = 'sub(max(possibility), min)')
        >>> root.fix_type()
        >>> print(root)
        sub(max(possibility), min(possibility))

        >>> root = Node(code = 'indexOf(min(possibility))')
        >>> root.fix_type()
        >>> print(root)
        indexOf(possibility, min(possibility))
        
        >>> root = Node(code = 'not_(startswith(0))')
        >>> root.fix_type()
        >>> print(root)
        not_(startswith(possibility, 0))

        if a var is a child of another var, it should move up to the parent
        >>> root = Node(code = 'subsets(input_array(input_int2))')
        >>> root.fix_type()
        >>> print(root)
        subsets(input_array, input_int2)

        '''
        for child in self.children:
            child.fix_type()
        if self.parent and not is_func(self.parent.name) and is_func(self.name):
            self.swap(self.parent)
        children_types = get_types(self.children)
        if is_comparison(self.name) and len(children_types) == 2 and ne(* children_types):
            self = cast_to_similar(self)
        self.children = insert_possibility(self)
        if not is_func(self.name) and self.children and not is_func(self.children[0].name):
            self.move_child(self.children[0], self.parent)
        
    def mark_duplicates(self, nodes=None):
        if nodes == None:
            nodes = [self.name]
        for child in self.children:
            if child.name in nodes:
                child.name = '#DUPLICATE'
            else:
                nodes.append(child.name)
            nodes = child.mark_duplicates(nodes)
        return nodes

    def eval_node(self):
        try:
            eval(str(self))
        except (TypeError,NameError, SyntaxError, ValueError) as e:
            return e
        return None

def insert_possibility(node):
    if is_func(node.name) and not node.children:
        new_node = Node('possibility')
        return [new_node]
    if not node.eval_node():
        return node.children
    for i in range(len(node.children)+1):
        tmp_node = copy.deepcopy(node)
        new_node = Node('possibility')
        tmp_node.insert_child(new_node, i)
        if tmp_node.eval_node():
            continue
        else:
            return tmp_node.children
    return node.children
    

def cast_to_similar(parent):
    node_types = get_types(parent.children)
    if 'int' in node_types:
        for child in parent.children:
            if hasattr(eval(str(child)), '__getitem__'):
                new_node = Node('len')
                parent.insert_child(new_node)
                parent.move_child(child, new_node)
    return parent

                

def clean_duplicates(tree):
    '''
    clean duplicated nodes

    >>> root = Node()
    >>> root.code2tree('len(set(possibility))')
    >>> root = clean_duplicates(root)
    >>> print(root)
    len(set(possibility))
            
    >>> root = Node()
    >>> root.code2tree('len(len(possibility))')
    >>> root = clean_duplicates(root)
    >>> print(root)
    len(possibility)

    >>> root = Node()
    >>> root.code2tree('zip(zip(input_array1, zip, input_array1), zip, input_array1)')
    >>> root = clean_duplicates(root)
    >>> print(root)
    zip(input_array1)
    
    :param tree:
    '''
    words = tree.get_nodes()
    tree.mark_duplicates()
    tree.filter_words(words)
    return tree

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
    '''
    transform a dependency syntax to word
    >>> print(dep2dict('well-known-4'))
    {'ind': 4, 'word': 'well-known'}
    
    :param dep:
    '''
    dep_split = dep.split('-')
    try:
        d = {}
        d['ind'] = int(dep_split[-1])
        d['word'] = '-'.join(dep_split[:-1])
        return d
    except ValueError:
        return {'word': dep, 'ind':None}
        
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
        json.dump(dependencies_dict, f, indent=4)

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


def split_args(args):
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

def translate_code(type_codeline, codedict):
    return str(Node(code=type_codeline).translate(codedict))

def main():
    sentence = 'hello my friend, how are you?'
#     print(sentence2dependencies(sentence))
    
    dep = 'hello-1'
    print(dep2word(dep))
    
    doctest.testmod()

if __name__ == '__main__':
    main()