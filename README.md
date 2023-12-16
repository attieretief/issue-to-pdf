# issue-to-pdf
> GitHub Action to monitor and convert an issue into PDF specification within your repository.

What if you could automatically convert GitHub Issues into PDF specification files, allowing you to write using just a browser?

## Usage

Create a file `.github/workflows/issue-to-pdf.yml` (or any filename) in your repository.

```yml
on:
  issues:
    types:
      - labeled

jobs:
  issue-to-pdf:
    runs-on: ubuntu-latest
    name: issue-to-pdf
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
      - name: Make-pdf
        id: make-pdf
        uses: attieretief/issue-to-pdf@v1
        with:
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          address: "<strong>COMPANY</strong><br>Address1<br>Address2<br>Address3<br>Address4<br>homepage"
          logo: "templates/logo.png"
      - name: Commit
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: 'pdf from gh issue'
```

If you add a `publish` label to any of your issues, this workflow will be activated.

To automatically update the markdown file after making changes to the issue, update the yml file as follows:

```yml
on:
  issues:
    types:
      - labeled
      - edited
```

## How issue markdown is used

The markdown content of the first comment (body) of the issue is used to generate the PDF by styling it with the default or custom css.

The issue title is used as the main title of the PDF document.

- Each h1 header starts a new chapter with a cover page.
- Each h2 header starts a new page within a chapter.

To include a client name in the footer of the cover page, add a label sucb as "client: ABC Industries" to the issue.

## How It Works

For those unfamiliar with GitHub Actions, here's a breakdown of the process:

1. In this step, the repository is cloned. A personal access token must be provided as token to allow the workflow to commit and push changes to the remote.

```yml
- uses: actions/checkout@v3
  with:
    token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

1. In this step, the issue is transformed into a PDF file, located in its own folder. The token is also necessary here.

```yml
- uses: attieretief/issue-to-pdf@v1
  with:
    token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
    address: "<strong>COMPANY</strong><br>Address1<br>Address2<br>Address3<br>Address4<br>homepage"
    logo: "templates/logo.png"
```

3. In this step, changes are committed and pushed to the remote. For more information on customizing the commit, refer to [this](https://github.com/stefanzweifel/git-auto-commit-action).

```yml
- uses: stefanzweifel/git-auto-commit-action@v4
  with:
    commit_message: 'docs: update contents'
```

## Personal Access Token

Visit https://github.com/settings/tokens/new to create a new personal access token. Choose "Tokens (classic)" instead of "Fine-grained tokens".

## Options

```yml
- uses: attieretief/issue-to-pdf@v1
  with:
    # Required
    token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}

    # Company address to include on cover page of PDF document
    address: '<strong>COMPANY</strong><br>Address line 1<br>Address line 2<br>Address line 3<br>Address line 4<br>Company web address'

    # ----------------------------------
    # All parameters below are optional.
    # ----------------------------------

    # By default, `publish` label is required for the workflow to work.
    label: 'publish'

    # New files are located at `<project-root>/<dest>/<issue_number>/<issue_number>.pdf`. (default: 'PDFs')
    dest: 'PDFs'

    # logo image file in repository to include in PDF
    logo: 'logo'

    # css file to use for styling PDF
    css: 'templates/spec.css'
```
