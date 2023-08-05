# LinkedIn_Feed_Bot

Python package in-development that crawls your LinkedIn news feed in order to create a PDF with a weekly summary of your chosen most important topic. It uses Selenium as its workhorse. If you wish to contribute please visit the [Github repository](https://github.com/Martins6/LinkedIn_Feed_Bot).

Contributions are very much welcome! If you'd like to contribute open an issue or a pull request.

## Installation

You can install this package throught pip. Just run:

```{python}
pip install LinkedIn_Feed_Bot
```

## Usage

Here is the basic usage of the package. As the package grows with many applications, a wiki should be made.

```{python}
import secret # secret is a .py file that contains your LinkedIn's credentials.
from LinkedIn_Feed_Bot import LinkedInBot
from LinkedIn_Feed_Bot import md_writer
from LinkedIn_Feed_Bot import md_to_pdf

bot = LinkedInBot.bot('path\to\webdriver') # Currently, it is only supported Google Chrome browser.

bot.sign_in(secret.username, secret.password)

for i in range(10):
    bot.scroll_down()

df = bot.df_author_post()

md_writer.feed_template_md('test.md', df)

md_to_pdf.convert('test.md')
```