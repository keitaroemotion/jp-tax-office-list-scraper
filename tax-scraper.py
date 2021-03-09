#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

url    = "https://www.nta.go.jp/about/organization/access/map.htm#ichiran"
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
driver.get(url)

def get_content():
    html = driver.find_element_by_tag_name('html') \
                 .get_attribute('innerHTML')
    return html

def get_lines(html, kw, kw2=''):
    tail  = "</a></td>"
    lines = [x.replace(kw2, '')
              .replace(tail, '')
              .replace(' ', '')
              .replace('\t', '') 
              .split("\">")
             for x
             in  html.split('\n') 
             if  kw  in x  and
                 'location' in x and
                 ('県' in x or '都' in x or '府' in x or '道' in x) and
                 'ページ' not in x
            ]
    return [list(filter(lambda x: 'tds' not in x, line)) for line in lines]

def get_lines2(html, kw, kw2=''):
    tail  = "</a></td>"
    lines = [x.replace(kw2, '')
              .replace(tail, '')
              .replace(' ', '')
              .replace('\t', '') 
             for x
             in  html.split('\n') 
            ]
    return lines

html   = get_content()
prefix = "<td style=\"border-right:none; border-left:none;\"><a href=\""
lines  = get_lines(html, '', prefix)

def visit(link):
    driver.get(link) 

root = "https://www.nta.go.jp"

i = 1
for line in lines:
    link = line[0].replace("<ahref=\"", "")
    visit(root + link)
    _lines = get_lines2(get_content(), '/about/organization')
    for _line in filter(lambda x: 'pdf' not in x and 'location' in x and '<td><ahref' in x, _lines): 
        lsp = _line.split("\">")
        if(len(lsp) > 1):
            print(f"P{i}" + '\t' + line[1] + '\t' + lsp[1].replace("</a>", "").replace("</td>", ""))
        else:
            print('ERROR')
    i = i + 1

input("Press any key:")
driver.close()
