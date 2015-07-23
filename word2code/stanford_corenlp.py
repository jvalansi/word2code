'''
Created on Mar 8, 2015

@author: jordan
'''
import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from pprint import pprint

import os
from nltk.parse import stanford
import re
from dependency_parser import dep2list



class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

# def sentence2dependencies(sentence):
#     parser = StanfordNLP()
#     parse = parser.parse(sentence)
#     dependencies = [sentence_parse['indexeddependencies'] for sentence_parse in parse['sentences']]
#     return (dependencies)

def sentence2dependencies(sentence):
    dependencies = raw_parse_sents([sentence])
    print(dependencies)
    dependencies = [[dep2list(dep) for dep in sentence_dependencies.split('\n')] for sentence_dependencies in dependencies.split('\n\n')]
    return (dependencies)

def tokenize_sentences(sentences):
    parser = StanfordNLP()
    parse = parser.parse(sentences)
    sentences_words = [[word[0] for word in sentence_parse['words']] for sentence_parse in parse['sentences']]
    return sentences_words
    
def raw_parse_sents(sentences, verbose=False, output_format='typedDependencies'):
    """
    Use StanfordParser to parse multiple sentences. Takes multiple sentences as a
    list of strings.
    Each sentence will be automatically tokenized and tagged by the Stanford Parser.

    :param sentences: Input sentences to parse
    :type sentences: list(str)
    :rtype: list(Tree)
    """
#     parser = stanford.StanfordParser('stanford-parser-full-2015-04-20/stanford-parser.jar', 
    parser = stanford.StanfordParser('stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar', 
                                     'stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1-models.jar')
    cmd = [
        'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
        '-model', parser.model_path,
        '-sentences', 'newline',
        '-outputFormat', output_format,
    ]
    trees_output = parser._execute(cmd, '\n'.join(sentences), verbose)
    return trees_output
#     return parser._parse_trees_output(trees_output)


if __name__ == '__main__':
    sentence = 'hello my friend, how are you?'
#     print(sentence2dependencies(sentence))
#     parser = StanfordNLP()
#     parse = parser.parse(sentence)
#     print(tokenize_sentences(sentence))
#     print(sentence2dependencies(sentence))
    
#     os.environ['STANFORD_PARSER'] = 'stanford-parser-full-2015-04-20'
#     os.environ['STANFORD_MODELS'] = 'stanford-parser-full-2015-04-20'
#     
#     parser = stanford.StanfordParser('stanford-parser-full-2015-04-20/stanford-parser.jar', 
#                                      'stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar')
#     sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
#     print sentences
#     
#     # GUI
#     for line in sentences:
#         for sentence in line:
#             sentence.draw()
#     print(raw_parse_sents(('this is the english parser test', 'the parser is from stanford parser')))
    print(sentence2dependencies(sentence))