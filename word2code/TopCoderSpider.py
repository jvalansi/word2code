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
        
    def getLinks(self,soup,pattern):
#     extract problems:
#         extract all http://community.topcoder.com/stat?c=problem_statement&pm=<number>
        problem_links = []
        for link in soup.findAll('a'):
            href = link.get('href')
            if re.match(pattern, href):
                problem_links.append(href)
        return problem_links
    
        
    def parseProblem(self,soup):
        problem_name = soup.find(class_ = 'statTextBig')
        problem_name = problem_name.get_text().split()[-1]
        print(problem_name)
        problem = soup.find(class_ = 'problemText')
        problem = problem.table.children 
        problem = [pt.get_text().encode('utf-8') for pt in problem]
        f = open('res/brute_force_easy/'+problem_name+'.prb', 'w')
        f.write('\n'.join(problem[:2])) #TODO: add rest

#     extract solutions /tc?module=ProblemDetail&rd=\d+&pm=\d+
    def parseSolution(self,soup):
        
        solution = soup.find(class_ = 'problemText')
        if not solution:
            return
        solution = solution.get_text()
        solution = solution.replace(u'\xa0', u' ').replace(u'\xc2', u' ')
        solution_name = re.findall(r'class\s+(\w+)',solution.encode('utf-8'))[0]
        print(solution_name)
        f = open('res/brute_force_easy/'+solution_name+'.sol', 'w')
        f.write(solution.encode('utf-8'))
        

if __name__ == '__main__':
    tcs = TopCoderSpider()
    root = "/tc?module=ProblemArchive&sr=1&er=100&sc=&sd=&class=&cat=Brute+Force&div1l=&div2l=1&mind1s=&mind2s=&maxd1s=&maxd2s=&wr="
    rootsoup = tcs.link2soup(root)
#     problem_links = tcs.getLinks(rootsoup,r'/stat\?c=problem_statement&pm=\d+')
#     print(len(problem_links))
#     for link in problem_links:
#         soup = tcs.link2soup(link)
#         tcs.parseProblem(soup)
        
    detail_links = tcs.getLinks(rootsoup,r'/tc\?module=ProblemDetail&rd=\d+&pm=\d+')
    for link in detail_links:
        soup = tcs.link2soup(link)
        sol_links = tcs.getLinks(soup,r'/stat\?c=problem_solution&cr=(\d+)?&rd=(\d+)?&pm=(\d+)?')
        soup = tcs.auth(sol_links[0]) # 0 = Java
        tcs.parseSolution(soup)
