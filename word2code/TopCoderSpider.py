'''
Created on Dec 23, 2014

@author: jordan
'''
from bs4 import BeautifulSoup
import urllib2
import re
import requests
from requests.auth import HTTPBasicAuth
import sys
import os
import json
import pickle
import problem


class TopCoderSpider:
    def __init__(self):
        self.base_url = 'http://community.topcoder.com'

    def auth(self,link):
        print(link)
        payload = {
        'nextpage':self.base_url+link,
        'module':"Login",
        'username':"jvalansi",
        'password':"X3mUPIOKA"
        }
        html_page = requests.post(self.base_url+link, data=payload)
        soup = BeautifulSoup(html_page.text)
        return soup

#     root url: http://community.topcoder.com/tc?module=ProblemArchive&sr=1&er=100&sc=&sd=&class=&cat=Brute+Force&div1l=&div2l=1&mind1s=&mind2s=&maxd1s=&maxd2s=&wr=
    def link2soup(self,link):
        html_page = urllib2.urlopen(self.base_url+link)
        soup = BeautifulSoup(html_page)
        return soup

    def get_links(self,soup,pattern):
#     extract problems:
#         extract all http://community.topcoder.com/stat?c=problem_statement&pm=<number>
        problem_links = []
        for link in soup.findAll('a'):
            href = link.get('href')
            if re.match(pattern, href):
                problem_links.append(href)
        return problem_links

    def get_problems(self, path, root):
        pattern = r'/stat\?c=problem_statement&pm=(\d+)'
        rootsoup = self.link2soup(root)
        problem_links = self.get_links(rootsoup,pattern)
        if not os.path.exists(path):
            os.mkdir(path)
        print(len(problem_links))
        for link in problem_links:
            soup = self.link2soup(link)
            m = re.search(pattern, link)
            name = m.group(1)
            fname = os.path.join(path, name)
            print(name)
            if os.path.isfile(fname):
                continue
            with open(fname, 'w') as f:
                f.write(soup.prettify('utf-8'))

    def parse_problem(self,fname):
        with open(fname, 'r') as f:
            html = f.read()
        soup = BeautifulSoup(html)
        problem_name = soup.find(class_ = 'statTextBig')
        problem_name = problem_name.get_text().split()[-1]
        problem_soup = soup.find(class_ = 'problemText')
#         problem_text = problem_soup.get_text()
#         print(problem_text)
        parts = problem_soup.table.children
        problem_dict =  {}
        header = None
        for part in parts:
            h3 = part.find('h3')
            if h3 > 0:
                header = h3.get_text().strip()
                problem_dict[header] = []
            else:
                try:
                    problem_dict[header].append(part)
                except:
                    pass
#         print(problem_dict['Definition'])
        problem_dict['Definition'] = self.parse_definitions(problem_dict['Definition'])
        problem_dict['Problem Statement'] = self.parse_statement(problem_dict['Problem Statement'])
        problem_dict['Constraints'] = self.parse_constraints(problem_dict['Constraints'])
        problem_dict['Examples'] = self.parse_examples(problem_dict['Examples'])
        if 'Notes' in problem_dict:
            problem_dict['Notes'] = self.parse_statement(problem_dict['Notes'])
#         print(problem_dict)
        with open(fname+'.json', 'w') as f:
            json.dump(problem_dict, f, indent=4)
#         with open(fname+'.pkl', 'w') as f:
#             pickle.dump(problem,f)
#         return(problem)

#     extract solutions /tc?module=ProblemDetail&rd=\d+&pm=\d+
    def parse_solution(self,soup):
        solution = soup.find(class_ = 'problemText')
        if not solution:
            return
        solution = solution.get_text()
        solution = solution.replace(u'\xa0', u' ').replace(u'\xc2', u' ')
        solution_name = re.findall(r'class\s+(\w+)',solution.encode('utf-8'))[0]
        print(solution_name)
        f = open('res/brute_force_easy/'+solution_name+'.sol', 'w')
        f.write(solution.encode('utf-8'))

    def parse_constraints(self,constraints):
        constraints_dict = {}
        for part in constraints:
            try:
                var = part.find('b').get_text()
                explanation = part.find('b').next_sibling
                constraints_dict[var] = explanation
            except:
                pass
        return constraints_dict

    def parse_statement(self,statement):
        s = ""
        for part in statement:
            try:
                s += part.get_text()
            except:
                pass
        return s

    def parse_definitions(self,definitions):
        for definition in definitions:
            try:
                definition_text = definition.get_text()
#                 print(definition_text)
                definition_dict = {}
                pattern = "\s+Class:\s+(?P<class_name>[^\n]+)"+\
                          "\s+Method:\s+(?P<method_name>[^\n]+)"+\
                          "\s+Parameters:\s+(?P<parameters>[^\n]+)"+\
                          "\s+Returns:\s+(?P<returns>[^\n]+)"+\
                          "\s+Method signature:\s+(?P<method_signature>[^\n]+)"
                m = re.match(pattern, definition_text)
                definition_dict['class_name'] = m.group('class_name')
                definition_dict['method_name'] = m.group('method_name')
                definition_dict['parameters'] = m.group('parameters')
                definition_dict['returns'] = m.group('returns')
                definition_dict['method_signature'] = m.group('method_signature')
                return(definition_dict)
            except:
                pass

    def parse_examples(self, examples):
        examples_list = []
        for example in examples:
            if examples.index(example)%4 != 3:
                continue
            example_dict = {}
            children = list(example.table.children)
            for child in children:
                if children.index(child)%6 == 1:
                    inputs = list(child.table.children)
                    example_dict['inputs'] = [input.get_text().strip() for input in inputs if inputs.index(input)%2 == 1]
                if children.index(child)%6 == 3:
                    example_dict['output'] = child.get_text().strip()[9:]
            examples_list.append(example_dict)
        return examples_list





if __name__ == '__main__':
    tcs = TopCoderSpider()
    root = "/tc?module=ProblemArchive&sr=1&er=100&sc=&sd=&class=&cat=Brute+Force&div1l=&div2l=1&mind1s=&mind2s=&maxd1s=&maxd2s=&wr="
#     rootsoup = tcs.link2soup(root)

    path = 'res/brute_force_easy/'
#     tcs.get_problems(path, root)
#     fname = '10152'
#     tcs.parse_problem(os.path.join(dir,fname))
    for fname in sorted(os.listdir(path)):
        if not re.match('^\d+$', fname):
            continue
        print(fname)
#         soup = tcs.link2soup(link)
        tcs.parse_problem(os.path.join(path, fname))

#     detail_links = tcs.getLinks(rootsoup,r'/tc\?module=ProblemDetail&rd=\d+&pm=\d+')
#     for link in detail_links:
#         soup = tcs.link2soup(link)
#         sol_links = tcs.getLinks(soup,r'/stat\?c=problem_solution&cr=(\d+)?&rd=(\d+)?&pm=(\d+)?')
#         soup = tcs.auth(sol_links[0]) # 0 = Java
#         tcs.parseSolution(soup)
