# all required packages
import requests 
import argparse
from bs4 import BeautifulSoup
import json

# input from command line
parser = argparse.ArgumentParser(description="Technologies to be searched for")
parser.add_argument('tech' ,metavar='javscript' ,type=str,nargs='+',help='tech to be searched')
args = parser.parse_args()

# access the website to parse
response = requests.get('https://summerofcode.withgoogle.com/archive/2021/organizations') 

# parsing contents of html using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# to store the hrefs that are to be visited later
to_visit = set()

# selecting all organization's links to visit 
for a in soup.select('a.organization-card__link'):
    to_visit.add(a.get('href'))


base_url = 'https://summerofcode.withgoogle.com'


i=1

org_list=[] #list of organizations that have the desired technology
tech_list=[] #list of technologies present in the organization
ispresent=False

for org_link in to_visit:
    tech_list.clear()
    ispresent=False
    org_url=base_url+org_link 
    response = requests.get(org_url) 
    soup = BeautifulSoup(response.content, "html.parser")

    for tech_used in (soup.select('li.organization__tag--technology')):
        tech_list.append(tech_used.text)
        if tech_used.text in args.tech:
            ispresent=True
            print(org_url)
    if(ispresent):
        add_org={"name":(soup.find('title').text),"tech":tech_list,"url":org_url}
        org_list.append(add_org)    
    # print(f"total organizations checked : {i}")
    i+=1
    if(i>=25):
        break

print(f"total organizations checked : {i}")
# print(org_list)

# getting all the organizations in a text file
with open('all_organizations.txt', 'w') as f:
    for item in org_list:
        f.write("%s\n" % item)

# getting all the organizations in a json file
with open("organizations.json", "w") as outfile:
    json.dump(org_list, outfile)           
