import os
import markdown
import markdown_include.include
from weasyprint import HTML
from datetime import datetime

# OPTIONS:
token = os.environ.get("TOKEN")
output_dir = os.environ.get("DEST")
number = os.environ.get("NUMBER")
title = os.environ.get("TITLE")
body = os.environ.get("BODY")
author = os.environ.get("AUTHOR")
created = os.environ.get("CREATED")
updated = os.environ.get("UPDATED")
repo = os.environ.get("REPO")
css = os.environ.get("CSS")
address = os.environ.get("ADDRESS")

def _html(markdown_input, css_file_name):
    with open(css_file_name, mode="r", encoding="utf-8") as css_file:
        css_input = css_file.read()

        html = markdown.markdown(
            markdown_input, extensions=[markdown_include.include]
        )

        return f"""
        <html>
            <head>
            <style>{css_input}</style>
            </head>
            <body>{html}</body>
        </html>
        """

def _convert(file_name, markdown_input, css_file_name):
    html_string = _html(markdown_input, css_file_name)

    html = HTML(string=html_string)
    html.write_pdf(file_name + ".pdf")

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

# Create the output folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

errors = []
print('\nConverting issue to PDF')
try:
    _convert(markdown_input=body,css_file_name=css)
except:
    log_error(number)

print('Find your exported PDF in ' +output_dir )