# -*- coding: utf-8 -*-
'''
Created on Wed Jun 24 14:57:40 2020

Scrape Websites for links based on keywords

'''

import requests
from bs4 import BeautifulSoup

# List of target URLs
Domain = 'https://forums.hardwarezone.com.sg'
Subdomain = ['/forums/it-garage-sales.18/',
             '/forums/electronics-bazaar.259/',
             '/forums/graphics-display-bazaar.200/',
             '/forums/notebooks-bazaar.260/',
             '/forums/gaming-bazaar.258/']

Target = []
for sub in Subdomain:
    
    # Setup 3 pages for each subdomain
    Target.append(Domain + sub)
    Target.append(Domain + sub + 'page-2')
    Target.append(Domain + sub + 'page-3')

# List of keywords
Keywords = ['2060','2070','2080','oculus','vive']


# Start scraping
listing = []

for url in Target:
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    page = requests.get(url, headers=headers)
    
    if page.status_code != 200:
        
        print('Error accessing url {}\nPage Status Code {}'.format(url,page.status_code))
        
    else:
        
        print('Searching {}'.format(url))
        soup = BeautifulSoup(page.content, 'html.parser')
                
        for key in Keywords:
            
            rawlisting = soup.find_all('a', href=True)
            
            for raw in rawlisting:
                
                if key.lower() in raw.text.lower():
                    
                    listing.append(raw)

    
# Prepare to output shortlisted links to a html file
html = '<html>\n'

for url in listing:
    
    link = url.get('href')
    text = url.text
    html += '<p> <a href=' + Domain + link + '>' + text + '</a> </p>\n'
    
        
html += '</html>'

# Write html to file
with open('test.html', 'w') as f:
    f.write(html)
