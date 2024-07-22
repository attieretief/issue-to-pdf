import os
import markdown
from markdown_include.include import MarkdownInclude
from weasyprint import HTML
from datetime import datetime
import requests

# OPTIONS:
token = os.environ.get("TOKEN")
output_dir = os.environ.get("DEST")
number = os.environ.get("NUMBER")
title = os.environ.get("TITLE")
subtitle = os.environ.get("SUBTITLE")
labels = os.environ.get("LABELS")
author = os.environ.get("AUTHOR")
created = os.environ.get("CREATED").replace('T',' ').replace('Z','')
updated = os.environ.get("UPDATED").replace('T',' ').replace('Z','')
repo = os.environ.get("REPO")
css = os.environ.get("CSS")
address = os.environ.get("ADDRESS")
body = open("body.md", mode="r", encoding="utf-8").read()

def _html_render(markdown_file_name, css_file_name):
   with open(markdown_file_name, mode="r", encoding="utf-8") as markdown_file, open(css_file_name, mode="r", encoding="utf-8") as css_file:
        markdown_input = markdown_file.read()
        css_input = css_file.read()
        response = requests.post(
            "https://api.github.com/markdown",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            json={
                "text": markdown_input,
                "mode": "gfm",
                "context": f"lincza/{repo}",
            },
        )
        html = response.text

        return f"""
            <html>
              <head>
                <style>{css_input}</style>
              </head>
              <body>
                {_html_input()}
                {html}
            </body>
            </html>
            """

def _html(markdown_file_name, css_file_name):
    with open(markdown_file_name, mode="r", encoding="utf-8") as markdown_file:
        with open(css_file_name, mode="r", encoding="utf-8") as css_file:
            markdown_input = markdown_file.read()
            css_input = css_file.read()

            markdown_path = os.path.dirname(markdown_file_name)
            markdown_include = MarkdownInclude(configs={"base_path": markdown_path})
            html = markdown.markdown(
                markdown_input, extensions=["extra", markdown_include, "meta", "tables"]
            )

            return f"""
            <html>
              <head>
                <style>{css_input}</style>
              </head>
              <body>{html}</body>
            </html>
            """

def _convert(markdown_file_name, css_file_name):
    file_name = os.path.splitext(markdown_file_name)[0]
    # html_string = _html(markdown_file_name, css_file_name)
    html_string = _html_render(markdown_file_name, css_file_name)

    with open(
        file_name + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace"
    ) as output_file:
        output_file.write(html_string)

    markdown_path = os.path.dirname(markdown_file_name)
    html = HTML(string=html_string, base_url=markdown_path)
    html.write_pdf(file_name + ".pdf")

def _client():
    for l in labels.split(','):
        if "client:" in l:
            return(l.split(":")[1])

def _html_input():
    return (
        f'<p class="title">{title}</p>'
        '<div class="footer">'
        '<div class="address">'
        f'{address}'
        '</div>'
        '<div class="contact">'
        '<strong>Client</strong><br>'
        f'{_client()}<br>'
        '<strong>Repository</strong><br>'
        f'{repo}<br>'
        '<strong>Issue Number</strong><br>'
        f'#{number}'
        '</div>'
        '<div>'
        '<strong>Author</strong><br>'
        f'{author}<br>'
        '<strong>Created</strong><br>'
        f'{created}<br>'
        '<strong>Modified</strong><br>'
        f'{updated}'
        '</div>'
        '</div>\n\n'
    )

def _mdfile(markdown_input, css_file_name):
    with open(output_dir + '/' + str(number) + '.md', mode="w", encoding="utf-8") as markdown_file:
        # markdown_file.write(_mdinput())
        markdown_file.write(markdown_input)
    markdown_file.close()
    _convert(markdown_file.name, css_file_name)

def _cleanup():
    os.remove("body.md")
    os.remove(output_dir + '/' + str(number) + '.md')
    os.remove(output_dir + '/' + str(number) + '.html')
    if os.path.exists(output_dir + '/logo'):
        os.remove(output_dir + '/logo')

def log_error(error):
    if not os.path.isfile(output_dir + "error_log.txt"):
        # Log file does not exist, so write explanatory header  
        with open(output_dir + "error_log.txt", "a") as myfile:
            myfile.write("Errors reported for the following URLs, please check to ensure the generated PDFs are correct.")
    with open(output_dir + "error_log.txt", "a") as myfile:
        myfile.write("\n\n" + str(datetime.now()) + "\n" + error)
        myfile.close()
    return

# Create the output folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Move the logo to the output folder
if os.path.exists('logo'):
    os.rename('logo',output_dir + '/logo')

errors = []
print('Converting Github Issue to PDF')
try:
    _mdfile(markdown_input=body,css_file_name=css)
    # _cleanup()
except:
    log_error(number)

print('Find your exported PDF in ' +output_dir )

