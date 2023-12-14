### This script scrapes the issues for a github project, and saves each one as a PDF.

import pdfkit
import requests
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

# OPTIONS:
# Personal Access Token with Repo access
token = os.environ.get("TOKEN")
# Output directory to save PDFs
output_dir = os.environ.get("DEST")
# Issue URL to use as source for PDF
url = os.environ.get("URL")

def log_error(error):   
    if not os.path.isfile(output_dir + "error_log.txt"):
        # Log file does not exist, so write explanatory header  
        with open(output_dir + "error_log.txt", "a") as myfile:
            myfile.write("Errors reported for the following URLs, please check to ensure the generated PDFs are correct.")
    with open(output_dir + "error_log.txt", "a") as myfile:
        myfile.write("\n\n" + str(datetime.now()) + "\n" + error)
        myfile.close()
    return

print("starting...")

options = {
    'dpi':'300' # This zooms in to make the PDFs more readable (recommended) 
}

# Create the output folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

errors = []
headers = {"Authorization": "Bearer " + token}
r = requests.get(url=url,headers=headers)
if r.status_code == 200:
    print('\nConverting page to PDF: ' + url)
    c = r.text
    # Strip versioning number from <link> paths (e.g. example.css?1234 -> example.css)
    # This is needed to avoid an error with wkpdftohtml
    # see thread at https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2051
    html = re.sub('#(\.css|\.js)\?[^"]+#', '$1', c)
    soup = BeautifulSoup(html, "lxml")
    html_head = str(soup.head)
    html_body = str(soup.find(class_='repohead'))
    html_body = str(html_body) + str(soup.find(id='show_issue'))

    full_html = html_head + html_body + tags

    try:
        if soup.find(id='show_issue'):
            pdfkit.from_string(full_html, output_dir +str(i) +'.pdf', options=options)
        else:
            print('\nIssue does not exist:' + url)
    except:
        log_error(url)

elif r.status_code == 404:
    print('\n404 not found: ' + url)

print('Find your exported PDF in ' +output_dir )