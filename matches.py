import requests
from bs4 import BeautifulSoup as bs


link_match = []
title_match=[]
def show_current():
    page = requests.get('https://www.cricbuzz.com/cricket-match/live-scores').text

    soup = bs(page, 'html.parser')

    h3s= soup.find_all('h3')

    a_s = []
    for i in range(len(h3s)):
        a_s.append(h3s[i].find_all('a'))

    global link_match
    global title_match
    link_match=[]
    title_match=[]

    for i in range(len(a_s)):
        title_match.append(a_s[i][0]['title'])
        link_match.append(a_s[i][0]['href'])

    i=0
    msg=''
    for it, iit in zip(title_match, link_match):
        print("{}. {}" .format((i+1),(it)))
        print("Link: {}" .format(iit))
        print(" ")
        i+=1
        msg=f'{msg}\n{i}. {it}'
    return msg
        
