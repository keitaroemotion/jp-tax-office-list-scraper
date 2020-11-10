#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
             for x
             in  html.split('\n') 
             if  kw  in x and
                 kw2 in x
            ]
    return lines

html   = get_content()
prefix = "<td style=\"border-right:none; border-left:none;\"><a href=\""
lines  = get_lines(html, '/about/organization', prefix)

def visit(link):
    driver.get(link) 

root = "https://www.nta.go.jp"

for line in lines:
    link = line.split("\">")[0]
    visit(root + link)
    _lines = get_lines(get_content(), '/about/organization')
    for _line in filter(lambda x: 'pdf' not in x and 'location' in x and '<td><ahref' in x, _lines): 
        lsp = _line.split("\">")
        if(len(lsp) > 1):
            
            print(link.split('/')[-1].replace('.htm', '') + ' ' + lsp[1].replace("</a>", "").replace("</td>", ""))
        else:
            print('ERROR')

input("Press any key:")
driver.close()
