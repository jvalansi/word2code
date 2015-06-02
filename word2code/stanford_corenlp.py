'''
Created on Mar 8, 2015

@author: jordan
'''
import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from pprint import pprint


class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def sentence2dependencies(sentence):
    parser = StanfordNLP()
    parse = parser.parse(sentence)
    dependencies = [sentence_parse['indexeddependencies'] for sentence_parse in parse['sentences']]
    return (dependencies)

if __name__ == '__main__':
    sentence = 'hello my friend, how are you?'
    print(sentence2dependencies(sentence))