import requests
import argparse
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description="Technologies to be searched for")
parser.add_argument('tech' ,metavar='javscript' ,type=str,nargs='+',help='tech to be searched')
args = parser.parse_args()


to_visit = set()
response = requests.get('https://summerofcode.withgoogle.com/archive/2021/organizations')
soup = BeautifulSoup(response.content, "html.parser")

for a in soup.select('a.organization-card__link'):
    to_visit.add(a.get('href'))

base_url = 'https://summerofcode.withgoogle.com'
print(to_visit)
result_orgs = set()
for org_link in to_visit:
    response = requests.get(base_url+org_link)
    #print(base_url+org_link)
    print(base_url+org_link)
    soup = BeautifulSoup(response.content, "html.parser")
    for tech_used in (soup.select('li.organization__tag--technology')):
        print(tech_used)
        if tech_used.text in args.tech:
            result_orgs.add((soup.find('title').text))


print(result_orgs)
